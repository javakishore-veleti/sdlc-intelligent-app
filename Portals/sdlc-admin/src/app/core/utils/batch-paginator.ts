import { Observable } from 'rxjs';

/**
 * Loads rows from the server in fixed-size batches (default 100) and paginates the
 * loaded rows on the client (default 10 per page). When the user advances past the
 * loaded rows and the server may hold more, the next batch is fetched automatically.
 */
export class BatchPaginator<T> {
  loaded: T[] = [];
  currentPage = 1;
  hasMoreServer = true;
  loading = false;
  error = '';

  constructor(
    private readonly fetcher: (skip: number, limit: number) => Observable<T[]>,
    private readonly pageSize = 10,
    private readonly batchSize = 100,
  ) {}

  get totalClientPages(): number {
    return Math.max(1, Math.ceil(this.loaded.length / this.pageSize));
  }

  get pageItems(): T[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.loaded.slice(start, start + this.pageSize);
  }

  get canPrev(): boolean {
    return this.currentPage > 1;
  }

  get canNext(): boolean {
    return this.currentPage < this.totalClientPages || this.hasMoreServer;
  }

  init(): void {
    this.fetchNextBatch();
  }

  next(): void {
    if (this.currentPage < this.totalClientPages) {
      this.currentPage += 1;
    } else if (this.hasMoreServer) {
      this.fetchNextBatch(() => {
        this.currentPage += 1;
      });
    }
  }

  prev(): void {
    if (this.canPrev) {
      this.currentPage -= 1;
    }
  }

  private fetchNextBatch(after?: () => void): void {
    if (this.loading || !this.hasMoreServer) {
      after?.();
      return;
    }
    this.loading = true;
    this.error = '';
    this.fetcher(this.loaded.length, this.batchSize).subscribe({
      next: (rows) => {
        this.loaded = [...this.loaded, ...rows];
        if (rows.length < this.batchSize) {
          this.hasMoreServer = false;
        }
        this.loading = false;
        after?.();
      },
      error: () => {
        this.error = 'Failed to load data. Is Master-Data-Service running?';
        this.loading = false;
      },
    });
  }
}
