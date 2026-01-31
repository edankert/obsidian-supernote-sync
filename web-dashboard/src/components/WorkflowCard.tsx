import { useState } from 'react';
import type { Workflow, WorkflowRunResult } from '../types';

interface WorkflowCardProps {
  workflow: Workflow;
  onRun: (id: string) => Promise<WorkflowRunResult>;
}

const WORKFLOW_ICONS: Record<string, string> = {
  'daily-notes': '📅',
  'research-notes': '📚',
  'world-building': '🌍',
  default: '⚡',
};

export function WorkflowCard({ workflow, onRun }: WorkflowCardProps) {
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const icon = WORKFLOW_ICONS[workflow.id] || WORKFLOW_ICONS.default;

  const handleRun = async () => {
    setRunning(true);
    setError(null);
    try {
      await onRun(workflow.id);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to run workflow');
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        <span className="text-3xl">{icon}</span>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-gray-900 dark:text-gray-100">
            {workflow.name}
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {workflow.description}
          </p>

          {/* Workflow Details */}
          <div className="mt-3 flex flex-wrap gap-2 text-xs">
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">
              Type: {workflow.note_type}
            </span>
            {workflow.device && (
              <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded">
                Device: {workflow.device}
              </span>
            )}
            <span className="px-2 py-1 bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 rounded">
              {workflow.steps.length} step{workflow.steps.length !== 1 ? 's' : ''}
            </span>
          </div>

          {/* Error message */}
          {error && (
            <div className="mt-2 text-sm text-red-600 dark:text-red-400">
              {error}
            </div>
          )}
        </div>

        {/* Run button */}
        <button
          onClick={handleRun}
          disabled={running}
          className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
            running
              ? 'bg-gray-200 dark:bg-gray-700 text-gray-400 cursor-not-allowed'
              : 'bg-indigo-600 hover:bg-indigo-700 text-white'
          }`}
        >
          {running ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
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
              Running
            </span>
          ) : (
            'Run'
          )}
        </button>
      </div>
    </div>
  );
}
