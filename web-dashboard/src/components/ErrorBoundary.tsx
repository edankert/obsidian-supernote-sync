import { Component, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('React Error Boundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 max-w-lg w-full">
            <h1 className="text-xl font-bold text-red-600 dark:text-red-400 mb-4">
              Something went wrong
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              The dashboard encountered an error. This usually happens when the backend server is not running.
            </p>
            <div className="bg-gray-100 dark:bg-gray-700 rounded p-3 mb-4">
              <code className="text-sm text-gray-800 dark:text-gray-200 break-all">
                {this.state.error?.message || 'Unknown error'}
              </code>
            </div>
            <div className="space-y-2 text-sm text-gray-500 dark:text-gray-400">
              <p><strong>To fix this:</strong></p>
              <ol className="list-decimal list-inside space-y-1">
                <li>Make sure the Python backend is running:</li>
                <li className="ml-4">
                  <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                    obsidian-supernote serve
                  </code>
                </li>
                <li>Then refresh this page</li>
              </ol>
            </div>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-4 rounded-lg"
            >
              Refresh Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
