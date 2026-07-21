export function Skeleton({ className = "" }: { className?: string }) {
  return (
    <div className={`animate-pulse rounded-md bg-slate-200 ${className}`} />
  );
}

export function StatCardSkeleton() {
  return (
    <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
      {[...Array(4)].map((_, i) => (
        <div key={i} className="rounded-xl border bg-card p-5 space-y-3">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-8 w-16" />
          <Skeleton className="h-3 w-20" />
        </div>
      ))}
    </div>
  );
}

export function ChartSkeleton() {
  return (
    <div className="rounded-xl border bg-card p-6 space-y-4">
      <Skeleton className="h-5 w-40" />
      <Skeleton className="h-56 w-full" />
    </div>
  );
}

export function TweetCardSkeleton() {
  return (
    <div className="rounded-xl border bg-card p-5 space-y-3">
      <div className="flex justify-between items-start">
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-6 w-20 rounded-full" />
      </div>
      <Skeleton className="h-4 w-1/2" />
      <Skeleton className="h-3 w-24" />
    </div>
  );
}

export function AnalyzerResultSkeleton() {
  return (
    <div className="w-full max-w-2xl mx-auto mt-6 rounded-xl border bg-card p-6 space-y-4">
      <div className="flex justify-between items-center">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="h-7 w-24 rounded-full" />
      </div>
      <Skeleton className="h-4 w-28" />
      {[...Array(3)].map((_, i) => (
        <div key={i} className="space-y-1">
          <div className="flex justify-between">
            <Skeleton className="h-3 w-20" />
            <Skeleton className="h-3 w-8" />
          </div>
          <Skeleton className="h-2 w-full rounded-full" />
        </div>
      ))}
    </div>
  );
}
