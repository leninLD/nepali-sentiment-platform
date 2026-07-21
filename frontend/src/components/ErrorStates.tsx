import { AlertTriangle, WifiOff, SearchX, CloudOff } from "lucide-react";
import type { ReactNode } from "react";

interface ErrorStateProps {
  icon?: ReactNode;
  title: string;
  message: string;
  action?: ReactNode;
}

export function ErrorState({ icon, title, message, action }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center space-y-4">
      <div className="text-slate-400">{icon ?? <AlertTriangle className="w-12 h-12" />}</div>
      <h3 className="text-lg font-semibold text-slate-700">{title}</h3>
      <p className="text-sm text-muted-foreground max-w-sm">{message}</p>
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
}

export function NitterDownError({ onRetry }: { onRetry?: () => void }) {
  return (
    <ErrorState
      icon={<WifiOff className="w-12 h-12" />}
      title="All Nitter instances are down"
      message="No live Nitter instance was reachable. This is a temporary outage. Please try again in a few minutes."
      action={onRetry && (
        <button onClick={onRetry} className="text-sm font-medium text-blue-600 hover:underline">
          Try again
        </button>
      )}
    />
  );
}

export function NoTweetsFoundError({ keyword }: { keyword?: string }) {
  return (
    <ErrorState
      icon={<SearchX className="w-12 h-12" />}
      title="No Nepali tweets found"
      message={`No Nepali-script tweets were collected${keyword ? ` for "${keyword}"` : ""}. Try a different keyword, or wait for more tweets to be posted.`}
    />
  );
}

export function EmptyWordCloudError() {
  return (
    <ErrorState
      icon={<CloudOff className="w-10 h-10" />}
      title="Not enough words"
      message="Too few tweets in this category to generate a meaningful word cloud. Try scraping more tweets or switching to the 'All' view."
    />
  );
}

export function ApiError({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-4 flex gap-3 items-start">
      <AlertTriangle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-red-700">Something went wrong</p>
        <p className="text-sm text-red-600 mt-0.5">{message}</p>
        {onRetry && (
          <button onClick={onRetry} className="text-sm font-medium text-red-700 hover:underline mt-1">
            Try again →
          </button>
        )}
      </div>
    </div>
  );
}
