/**
 * LinkedIn Job Fetcher using Playwright with Stealth
 */

import { chromium } from 'playwright-extra';
import { Browser, Page, BrowserContext } from 'playwright';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import { normalizeLinkedInUrl } from './normalizeUrl';
import { acquireSlot, ConcurrencySlot } from './concurrency';

// Apply stealth plugin to avoid detection
chromium.use(StealthPlugin());

const DEFAULT_TIMEOUT_MS = parseInt(process.env.DEFAULT_TIMEOUT_MS || '45000', 10);
const HEADLESS = process.env.HEADLESS !== 'false';
const MAX_DESCRIPTION_LENGTH = 60000;

// Blocked reasons
type BlockReason = 'LOGIN_REQUIRED' | 'CAPTCHA' | 'RATE_LIMIT' | 'SELECTOR_TIMEOUT' | 'UNKNOWN';

export interface FetchOptions {
  timeoutMs?: number;
  headless?: boolean;
}

export interface FetchSuccessResult {
  ok: true;
  blocked: false;
  jobId: string;
  canonicalUrl: string;
  title: string;
  company: string;
  location: string;
  descriptionText: string;
  applyUrl: string | null;
  debug: {
    finalUrl: string;
    httpStatus: number;
    timingsMs: {
      launch: number;
      goto: number;
      extract: number;
    };
  };
}

export interface FetchBlockedResult {
  ok: false;
  blocked: true;
  reason: BlockReason;
  jobId: string;
  canonicalUrl: string;
  applyUrl: string | null;
  debug: {
    finalUrl: string;
    httpStatus: number | null;
  };
}

export interface FetchErrorResult {
  ok: false;
  blocked: false;
  error: string;
  jobId?: string;
  canonicalUrl?: string;
}

export type FetchResult = FetchSuccessResult | FetchBlockedResult | FetchErrorResult;

// Realistic User-Agents (rotated randomly)
const USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15'
];

// Get random user agent
const getRandomUserAgent = () => USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];

// Random delay helper (makes behavior more human-like)
const randomDelay = (min: number, max: number) => Math.floor(Math.random() * (max - min + 1)) + min;

// Selectors for job data
const SELECTORS = {
  // Job title selectors (try multiple)
  title: [
    'h1.top-card-layout__title',
    'h1.topcard__title',
    'h1[class*="job-title"]',
    '.job-details-jobs-unified-top-card__job-title h1',
    'h1'
  ],
  // Company name
  company: [
    '.top-card-layout__card a.topcard__org-name-link',
    '.topcard__org-name-link',
    'a[data-tracking-control-name="public_jobs_topcard-org-name"]',
    '.job-details-jobs-unified-top-card__company-name a',
    '.job-details-jobs-unified-top-card__company-name'
  ],
  // Location
  location: [
    '.top-card-layout__card .topcard__flavor--bullet',
    '.topcard__flavor--bullet',
    '.job-details-jobs-unified-top-card__bullet',
    '.job-details-jobs-unified-top-card__primary-description-container span'
  ],
  // Job description
  description: [
    '.description__text',
    '.show-more-less-html__markup',
    '.job-details-jobs-unified-top-card__job-description',
    '[class*="description"] [class*="markup"]',
    '.jobs-description__content',
    'article'
  ],
  // "See more" / "Show more" buttons
  showMore: [
    'button.show-more-less-html__button',
    'button[aria-label*="more"]',
    'button[class*="show-more"]',
    '.show-more-less-html__button--more'
  ],
  // Apply button / URL
  applyButton: [
    'a.apply-button',
    'a[data-tracking-control-name*="apply"]',
    '.jobs-apply-button',
    'a[href*="apply"]'
  ]
};

// Login/block detection patterns
const BLOCK_PATTERNS = {
  loginUrls: ['/login', '/checkpoint', '/authwall', '/uas/login'],
  loginText: ['Sign in', 'Join now', 'Log in', 'Sign up'],
  captchaText: ['captcha', 'verify you', 'security verification', 'prove you'],
  rateLimitText: ['too many requests', 'rate limit', 'slow down']
};

/**
 * Main fetch function
 */
export async function fetchLinkedInJob(rawUrl: string, options: FetchOptions = {}): Promise<FetchResult> {
  const timeoutMs = options.timeoutMs || DEFAULT_TIMEOUT_MS;
  const headless = options.headless !== undefined ? options.headless : HEADLESS;

  // Normalize URL
  const normalized = normalizeLinkedInUrl(rawUrl);
  if (!normalized.ok || !normalized.jobId || !normalized.canonicalUrl) {
    return {
      ok: false,
      blocked: false,
      error: normalized.error || 'INVALID_URL'
    };
  }

  const { jobId, canonicalUrl } = normalized;
  let slot: ConcurrencySlot | null = null;
  let browser: Browser | null = null;
  let context: BrowserContext | null = null;

  const timings = {
    launch: 0,
    goto: 0,
    extract: 0
  };

  try {
    // Acquire concurrency slot
    slot = await acquireSlot(timeoutMs);

    // Launch browser
    const launchStart = Date.now();
    browser = await chromium.launch({
      headless,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu',
        '--no-first-run',
        '--no-zygote',
        '--single-process'
      ]
    });
    timings.launch = Date.now() - launchStart;

    // Create context with realistic settings
    context = await browser.newContext({
      userAgent: getRandomUserAgent(),
      viewport: { width: 1366 + randomDelay(-100, 100), height: 768 + randomDelay(-50, 50) },
      locale: 'en-US',
      timezoneId: 'America/New_York',
      deviceScaleFactor: 1,
      hasTouch: false,
      isMobile: false,
      javaScriptEnabled: true
    });

    // Add random initial delay to seem more human
    await new Promise(resolve => setTimeout(resolve, randomDelay(500, 1500)));

    const page = await context.newPage();

    // Block images, fonts, media for speed
    await page.route('**/*', (route) => {
      const resourceType = route.request().resourceType();
      if (['image', 'font', 'media', 'stylesheet'].includes(resourceType)) {
        route.abort();
      } else {
        route.continue();
      }
    });

    // Navigate to job page
    const gotoStart = Date.now();
    let response;
    try {
      response = await page.goto(canonicalUrl, {
        waitUntil: 'domcontentloaded',
        timeout: timeoutMs
      });
    } catch (err) {
      timings.goto = Date.now() - gotoStart;
      return {
        ok: false,
        blocked: true,
        reason: 'SELECTOR_TIMEOUT',
        jobId,
        canonicalUrl,
        applyUrl: null,
        debug: {
          finalUrl: page.url(),
          httpStatus: null
        }
      };
    }
    timings.goto = Date.now() - gotoStart;

    const httpStatus = response?.status() || null;
    const finalUrl = page.url();

    // Check for blocks
    const blockResult = await detectBlock(page, finalUrl);
    if (blockResult.blocked) {
      const applyUrl = await tryExtractApplyUrl(page);
      return {
        ok: false,
        blocked: true,
        reason: blockResult.reason,
        jobId,
        canonicalUrl,
        applyUrl,
        debug: {
          finalUrl,
          httpStatus
        }
      };
    }

    // Extract job data
    const extractStart = Date.now();
    const jobData = await extractJobData(page, timeoutMs);
    timings.extract = Date.now() - extractStart;

    if (!jobData.descriptionText) {
      // Description not found - likely blocked
      const applyUrl = await tryExtractApplyUrl(page);
      return {
        ok: false,
        blocked: true,
        reason: 'SELECTOR_TIMEOUT',
        jobId,
        canonicalUrl,
        applyUrl,
        debug: {
          finalUrl,
          httpStatus
        }
      };
    }

    return {
      ok: true,
      blocked: false,
      jobId,
      canonicalUrl,
      title: jobData.title,
      company: jobData.company,
      location: jobData.location,
      descriptionText: jobData.descriptionText,
      applyUrl: jobData.applyUrl,
      debug: {
        finalUrl,
        httpStatus: httpStatus || 200,
        timingsMs: timings
      }
    };

  } catch (err) {
    const error = err instanceof Error ? err.message : String(err);
    console.error(`[fetchLinkedIn] Error for jobId=${jobId}: ${error}`);
    return {
      ok: false,
      blocked: false,
      error,
      jobId,
      canonicalUrl
    };
  } finally {
    if (context) await context.close().catch(() => {});
    if (browser) await browser.close().catch(() => {});
    if (slot) slot.release();
  }
}

/**
 * Detect if page is blocked (login, captcha, rate limit)
 */
async function detectBlock(page: Page, currentUrl: string): Promise<{ blocked: boolean; reason: BlockReason }> {
  // Check URL for login redirects
  for (const pattern of BLOCK_PATTERNS.loginUrls) {
    if (currentUrl.includes(pattern)) {
      return { blocked: true, reason: 'LOGIN_REQUIRED' };
    }
  }

  // Check page content for block indicators
  const pageText = await page.evaluate(() => document.body?.innerText || '').catch(() => '');
  const pageTextLower = pageText.toLowerCase();

  // Check for CAPTCHA
  for (const pattern of BLOCK_PATTERNS.captchaText) {
    if (pageTextLower.includes(pattern.toLowerCase())) {
      return { blocked: true, reason: 'CAPTCHA' };
    }
  }

  // Check for rate limit
  for (const pattern of BLOCK_PATTERNS.rateLimitText) {
    if (pageTextLower.includes(pattern.toLowerCase())) {
      return { blocked: true, reason: 'RATE_LIMIT' };
    }
  }

  // Check for login prompts in main content area
  const mainContent = await page.$eval('main, [role="main"], .main-content', el => el?.textContent || '').catch(() => '');
  for (const pattern of BLOCK_PATTERNS.loginText) {
    if (mainContent.includes(pattern)) {
      // Could be a sign-in prompt blocking content
      // Check if there's actual job content too
      const hasJobContent = await page.$('.description__text, .show-more-less-html__markup, article').catch(() => null);
      if (!hasJobContent) {
        return { blocked: true, reason: 'LOGIN_REQUIRED' };
      }
    }
  }

  return { blocked: false, reason: 'UNKNOWN' };
}

/**
 * Extract job data from page
 */
async function extractJobData(page: Page, timeoutMs: number): Promise<{
  title: string;
  company: string;
  location: string;
  descriptionText: string;
  applyUrl: string | null;
}> {
  // Wait a bit for dynamic content (randomized to seem more human)
  await page.waitForTimeout(randomDelay(1500, 3000));

  // Try to click "Show more" button if present
  await tryClickShowMore(page);

  // Extract title
  const title = await trySelectors(page, SELECTORS.title) || 'Unknown Title';

  // Extract company
  const company = await trySelectors(page, SELECTORS.company) || 'Unknown Company';

  // Extract location
  const location = await trySelectors(page, SELECTORS.location) || '';

  // Extract description - try selectors, then fallback to main content
  let descriptionText = await trySelectorsForDescription(page, SELECTORS.description);

  if (!descriptionText) {
    // Fallback: try to get main article content
    descriptionText = await page.$eval('article, main, [role="main"]', el => el?.textContent || '').catch(() => '');
  }

  // Clean description text
  descriptionText = cleanDescriptionText(descriptionText);

  // Extract apply URL
  const applyUrl = await tryExtractApplyUrl(page);

  return {
    title: title.trim(),
    company: company.trim(),
    location: location.trim(),
    descriptionText,
    applyUrl
  };
}

/**
 * Try to click "Show more" button to expand description
 */
async function tryClickShowMore(page: Page): Promise<void> {
  for (const selector of SELECTORS.showMore) {
    try {
      const button = await page.$(selector);
      if (button) {
        await button.click();
        await page.waitForTimeout(500);
        return;
      }
    } catch {
      // Continue to next selector
    }
  }
}

/**
 * Try multiple selectors and return first matching text
 */
async function trySelectors(page: Page, selectors: string[]): Promise<string | null> {
  for (const selector of selectors) {
    try {
      const text = await page.$eval(selector, el => el?.textContent || '');
      if (text && text.trim()) {
        return text.trim();
      }
    } catch {
      // Continue to next selector
    }
  }
  return null;
}

/**
 * Try selectors specifically for description (preserves some structure)
 */
async function trySelectorsForDescription(page: Page, selectors: string[]): Promise<string> {
  for (const selector of selectors) {
    try {
      const text = await page.$eval(selector, el => {
        if (!el) return '';
        // Get text with line breaks preserved
        const clone = el.cloneNode(true) as HTMLElement;
        // Replace br tags with newlines
        clone.querySelectorAll('br').forEach(br => br.replaceWith('\n'));
        // Replace block elements with newlines
        clone.querySelectorAll('p, div, li').forEach(block => {
          block.prepend(document.createTextNode('\n'));
        });
        return clone.textContent || '';
      });
      if (text && text.trim().length > 50) {
        return text;
      }
    } catch {
      // Continue to next selector
    }
  }
  return '';
}

/**
 * Try to extract apply URL
 */
async function tryExtractApplyUrl(page: Page): Promise<string | null> {
  for (const selector of SELECTORS.applyButton) {
    try {
      const href = await page.$eval(selector, el => (el as HTMLAnchorElement).href || '');
      if (href && href.startsWith('http')) {
        return href;
      }
    } catch {
      // Continue to next selector
    }
  }
  return null;
}

/**
 * Clean description text
 */
function cleanDescriptionText(text: string): string {
  if (!text) return '';

  // Preserve line breaks but collapse excessive whitespace
  let cleaned = text
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .replace(/[ \t]+/g, ' ')           // Collapse horizontal whitespace
    .replace(/\n[ \t]+/g, '\n')        // Remove leading whitespace on lines
    .replace(/[ \t]+\n/g, '\n')        // Remove trailing whitespace on lines
    .replace(/\n{3,}/g, '\n\n')        // Max 2 consecutive newlines
    .trim();

  // Truncate if too long
  if (cleaned.length > MAX_DESCRIPTION_LENGTH) {
    cleaned = cleaned.substring(0, MAX_DESCRIPTION_LENGTH) + '\n...[TRUNCATED]...';
  }

  return cleaned;
}
