/**
 * Concurrency limiter for Playwright browser instances
 */

const MAX_CONCURRENCY = parseInt(process.env.MAX_CONCURRENCY || '2', 10);

let currentConcurrency = 0;
const queue: Array<{
  resolve: () => void;
  reject: (err: Error) => void;
}> = [];

export interface ConcurrencySlot {
  release: () => void;
}

export async function acquireSlot(timeoutMs: number = 60000): Promise<ConcurrencySlot> {
  return new Promise((resolve, reject) => {
    const tryAcquire = () => {
      if (currentConcurrency < MAX_CONCURRENCY) {
        currentConcurrency++;
        resolve({
          release: () => {
            currentConcurrency--;
            // Process next in queue
            const next = queue.shift();
            if (next) {
              next.resolve();
            }
          }
        });
        return true;
      }
      return false;
    };

    // Try to acquire immediately
    if (tryAcquire()) {
      return;
    }

    // Set up timeout
    const timeoutId = setTimeout(() => {
      const idx = queue.findIndex(q => q.resolve === queueResolve);
      if (idx !== -1) {
        queue.splice(idx, 1);
      }
      reject(new Error('CONCURRENCY_TIMEOUT'));
    }, timeoutMs);

    // Queue resolve function
    const queueResolve = () => {
      clearTimeout(timeoutId);
      if (tryAcquire()) {
        return;
      }
      // Shouldn't happen, but re-queue if needed
      queue.push({ resolve: queueResolve, reject });
    };

    queue.push({ resolve: queueResolve, reject });
  });
}

export function getCurrentConcurrency(): number {
  return currentConcurrency;
}

export function getQueueLength(): number {
  return queue.length;
}

export function getMaxConcurrency(): number {
  return MAX_CONCURRENCY;
}
