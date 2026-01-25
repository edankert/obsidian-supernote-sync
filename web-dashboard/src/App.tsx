import { StatusBar, WorkflowCard, ProgressIndicator, ConvertPanel } from './components';
import { useStatus, useDependencies, useWorkflows } from './hooks/useApi';
import { useWebSocket } from './hooks/useWebSocket';
import './index.css';

function App() {
  const { status } = useStatus();
  const { dependencies } = useDependencies();
  const { workflows, loading: workflowsLoading, error: workflowsError, runWorkflow } = useWorkflows();
  const { connectionStatus, currentProgress } = useWebSocket();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Status Bar */}
      <StatusBar
        connectionStatus={connectionStatus}
        status={status}
        dependencies={dependencies}
      />

      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Obsidian-Supernote Sync
          </h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Convert and sync files between Obsidian and Supernote
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Workflows Section */}
          <div className="lg:col-span-2">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
              Workflows
            </h2>

            {workflowsLoading ? (
              <div className="text-gray-500 dark:text-gray-400">Loading workflows...</div>
            ) : workflowsError ? (
              <div className="text-red-500 dark:text-red-400">{workflowsError}</div>
            ) : workflows.length === 0 ? (
              <div className="text-gray-500 dark:text-gray-400">
                No workflows configured. Add workflow YAML files to{' '}
                <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">
                  examples/configs/
                </code>
              </div>
            ) : (
              <div className="space-y-4">
                {workflows.map((workflow) => (
                  <WorkflowCard
                    key={workflow.id}
                    workflow={workflow}
                    onRun={runWorkflow}
                  />
                ))}
              </div>
            )}

            {/* Info Box */}
            <div className="mt-8 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <h3 className="font-medium text-blue-900 dark:text-blue-300 mb-2">
                About Workflows
              </h3>
              <p className="text-sm text-blue-700 dark:text-blue-400">
                Workflows automate the conversion process. Each workflow defines:
              </p>
              <ul className="mt-2 text-sm text-blue-700 dark:text-blue-400 list-disc list-inside space-y-1">
                <li>
                  <strong>Trigger:</strong> When to run (manual, on save, scheduled, or by tag)
                </li>
                <li>
                  <strong>Source:</strong> Where to find input files
                </li>
                <li>
                  <strong>Steps:</strong> Conversion operations to perform
                </li>
                <li>
                  <strong>Output:</strong> Where to save converted files
                </li>
              </ul>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            {/* Quick Convert */}
            <ConvertPanel />

            {/* Help */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
                Help
              </h2>
              <div className="space-y-3 text-sm text-gray-600 dark:text-gray-400">
                <p>
                  <strong>Getting Started:</strong> Run workflows to convert files
                  between Obsidian and Supernote.
                </p>
                <p>
                  <strong>Quick Convert:</strong> Use the panel above to convert
                  individual files without setting up a workflow.
                </p>
                <p>
                  <strong>API Docs:</strong>{' '}
                  <a
                    href="/api/docs"
                    target="_blank"
                    className="text-indigo-600 dark:text-indigo-400 hover:underline"
                  >
                    View interactive API documentation
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Progress Indicator */}
      <ProgressIndicator progress={currentProgress} />
    </div>
  );
}

export default App;
