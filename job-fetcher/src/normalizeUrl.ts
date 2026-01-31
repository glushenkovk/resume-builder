/**
 * URL normalization for LinkedIn job URLs
 * Canonicalizes to: https://www.linkedin.com/jobs/view/<jobId>/
 */

export interface NormalizeResult {
  ok: boolean;
  jobId?: string;
  canonicalUrl?: string;
  error?: string;
}

export function normalizeLinkedInUrl(rawUrl: string): NormalizeResult {
  if (!rawUrl || typeof rawUrl !== 'string') {
    return { ok: false, error: 'INVALID_URL' };
  }

  let url: URL;
  try {
    // Handle URLs without protocol
    const urlStr = rawUrl.trim();
    url = new URL(urlStr.startsWith('http') ? urlStr : `https://${urlStr}`);
  } catch {
    return { ok: false, error: 'INVALID_URL' };
  }

  // Validate hostname includes linkedin.com
  const hostname = url.hostname.toLowerCase();
  if (!hostname.includes('linkedin.com')) {
    return { ok: false, error: 'NOT_LINKEDIN_URL' };
  }

  // Extract jobId from path
  // Patterns:
  // /jobs/view/1234567890
  // /jobs/view/1234567890/
  // /jobs/view/1234567890?tracking=...
  const pathMatch = url.pathname.match(/\/jobs\/view\/(\d+)/);

  if (!pathMatch || !pathMatch[1]) {
    return { ok: false, error: 'INVALID_URL' };
  }

  const jobId = pathMatch[1];
  const canonicalUrl = `https://www.linkedin.com/jobs/view/${jobId}/`;

  return {
    ok: true,
    jobId,
    canonicalUrl
  };
}
