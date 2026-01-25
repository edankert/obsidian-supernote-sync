import type { ProgressEvent } from '../types';

interface ProgressIndicatorProps {
  progress: ProgressEvent | null;
}

export function ProgressIndicator({ progress }: ProgressIndicatorProps) {
  if (!progress) return null;

  const percent = progress.percent ?? 0;
  const message = progress.message || getDefaultMessage(progress);

  return (
    <div className="fixed bottom-4 right-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-4 min-w-[300px] z-50">
      <div className="flex items-center gap-3 mb-2">
        <svg className="animate-spin h-5 w-5 text-indigo-600" viewBox="0 0 24 24">
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
            fill="none"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
        <span className="font-medium text-gray-900 dark:text-gray-100">
          {getTitle(progress)}
        </span>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-2">
        <div
          className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${Math.min(100, Math.max(0, percent * 100))}%` }}
        />
      </div>

      {/* Message */}
      <p className="text-sm text-gray-500 dark:text-gray-400 truncate">{message}</p>

      {/* File info */}
      {progress.input_path && (
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1 truncate">
          {progress.input_path}
        </p>
      )}

      {/* Batch progress */}
      {progress.total !== undefined && progress.current !== undefined && (
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
          File {progress.current + 1} of {progress.total}
        </p>
      )}
    </div>
  );
}

function getTitle(progress: ProgressEvent): string {
  switch (progress.type) {
    case 'conversion_started':
    case 'conversion_progress':
      return `Converting ${progress.conversion_type || 'file'}`;
    case 'batch_started':
    case 'batch_progress':
      return 'Batch conversion';
    case 'workflow_started':
    case 'workflow_step':
      return 'Running workflow';
    default:
      return 'Processing';
  }
}

function getDefaultMessage(progress: ProgressEvent): string {
  switch (progress.type) {
    case 'conversion_started':
      return 'Starting conversion...';
    case 'batch_started':
      return 'Starting batch conversion...';
    case 'workflow_started':
      return 'Starting workflow...';
    case 'workflow_step':
      return `Step ${progress.step || 0}`;
    default:
      return 'Processing...';
  }
}
