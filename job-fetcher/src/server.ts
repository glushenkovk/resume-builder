/**
 * Job Fetcher Express Server
 */

import express, { Request, Response, NextFunction } from 'express';
import { fetchLinkedInJob, FetchOptions } from './fetchLinkedIn';
import { checkRateLimit, getRateLimitHeaders } from './rateLimit';
import { getCurrentConcurrency, getQueueLength, getMaxConcurrency } from './concurrency';

const app = express();
const PORT = parseInt(process.env.PORT || '3000', 10);
const REQUEST_TIMEOUT_MS = parseInt(process.env.REQUEST_TIMEOUT_MS || '120000', 10);

// Middleware
app.use(express.json({ limit: '1mb' }));

// Request timeout middleware
app.use((req: Request, res: Response, next: NextFunction) => {
  res.setTimeout(REQUEST_TIMEOUT_MS, () => {
    if (!res.headersSent) {
      res.status(408).json({
        ok: false,
        error: 'REQUEST_TIMEOUT'
      });
    }
  });
  next();
});

// Log requests (minimal)
app.use((req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} ${res.statusCode} ${duration}ms`);
  });
  next();
});

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  res.json({
    ok: true,
    concurrency: {
      current: getCurrentConcurrency(),
      max: getMaxConcurrency(),
      queued: getQueueLength()
    }
  });
});

// Fetch endpoint
app.post('/fetch', async (req: Request, res: Response) => {
  const clientIp = req.ip || req.socket.remoteAddress || 'unknown';

  // Rate limit check
  const rateLimitResult = checkRateLimit(clientIp);
  const rateLimitHeaders = getRateLimitHeaders(rateLimitResult);

  // Set rate limit headers
  Object.entries(rateLimitHeaders).forEach(([key, value]) => {
    res.setHeader(key, value);
  });

  if (!rateLimitResult.allowed) {
    res.status(429).json({
      ok: false,
      error: 'RATE_LIMIT_EXCEEDED',
      retryAfter: Math.ceil((rateLimitResult.resetAt - Date.now()) / 1000)
    });
    return;
  }

  // Validate request body
  const { url, options = {} } = req.body as { url?: string; options?: FetchOptions };

  if (!url || typeof url !== 'string') {
    res.status(400).json({
      ok: false,
      error: 'INVALID_URL',
      message: 'Request body must include a "url" field with a LinkedIn job URL'
    });
    return;
  }

  // Log start (without full URL for privacy)
  const jobIdMatch = url.match(/\/jobs\/view\/(\d+)/);
  const jobIdLog = jobIdMatch ? jobIdMatch[1] : 'unknown';
  console.log(`[fetch] Starting fetch for jobId=${jobIdLog}`);

  try {
    const result = await fetchLinkedInJob(url, options);

    // Log result (minimal)
    if (result.ok && !result.blocked) {
      console.log(`[fetch] Success for jobId=${jobIdLog}`);
    } else if ('blocked' in result && result.blocked) {
      console.log(`[fetch] Blocked for jobId=${jobIdLog}: ${result.reason}`);
    } else {
      console.log(`[fetch] Error for jobId=${jobIdLog}: ${'error' in result ? result.error : 'unknown'}`);
    }

    res.json(result);
  } catch (err) {
    const error = err instanceof Error ? err.message : String(err);
    console.error(`[fetch] Unexpected error for jobId=${jobIdLog}: ${error}`);
    res.status(500).json({
      ok: false,
      error: 'INTERNAL_ERROR',
      message: error
    });
  }
});

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({
    ok: false,
    error: 'NOT_FOUND',
    message: `Endpoint ${req.method} ${req.path} not found`
  });
});

// Error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('[server] Unhandled error:', err);
  if (!res.headersSent) {
    res.status(500).json({
      ok: false,
      error: 'INTERNAL_ERROR',
      message: err.message
    });
  }
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`[server] Job Fetcher listening on port ${PORT}`);
  console.log(`[server] Config: HEADLESS=${process.env.HEADLESS !== 'false'}, MAX_CONCURRENCY=${getMaxConcurrency()}`);
});
