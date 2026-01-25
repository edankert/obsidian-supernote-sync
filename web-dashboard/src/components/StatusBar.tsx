import type { ConnectionStatus, StatusResponse, DependenciesResponse } from '../types';

interface StatusBarProps {
  connectionStatus: ConnectionStatus;
  status: StatusResponse | null;
  dependencies: DependenciesResponse | null;
}

export function StatusBar({ connectionStatus, status, dependencies }: StatusBarProps) {
  const isConnected = connectionStatus.connected && connectionStatus.backend_available;

  return (
    <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          {/* Connection Status */}
          <div className="flex items-center gap-2">
            <div
              className={`w-2 h-2 rounded-full ${
                isConnected ? 'bg-green-500' : 'bg-red-500'
              }`}
            />
            <span className="text-sm text-gray-600 dark:text-gray-300">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {/* Version */}
          {status && (
            <span className="text-sm text-gray-500 dark:text-gray-400">
              v{status.version}
            </span>
          )}

          {/* Dependencies */}
          {dependencies && (
            <div className="flex items-center gap-1">
              {Object.entries(dependencies).map(([name, dep]) => (
                <span
                  key={name}
                  className={`text-xs px-2 py-0.5 rounded ${
                    dep.available
                      ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300'
                      : 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300'
                  }`}
                  title={dep.version || ''}
                >
                  {name}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Uptime */}
        {status?.uptime_seconds != null && (
          <span className="text-xs text-gray-400">
            Uptime: {formatUptime(status.uptime_seconds)}
          </span>
        )}
      </div>
    </div>
  );
}

function formatUptime(seconds: number): string {
  if (seconds < 60) return `${Math.floor(seconds)}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ${Math.floor((seconds % 3600) / 60)}m`;
  return `${Math.floor(seconds / 86400)}d ${Math.floor((seconds % 86400) / 3600)}h`;
}
