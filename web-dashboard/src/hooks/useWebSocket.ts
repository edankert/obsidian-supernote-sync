import { useEffect, useRef, useState, useCallback } from 'react';
import type { ProgressEvent, ConnectionStatus } from '../types';

const WS_URL = `ws://${window.location.hostname}:8765/events`;

export function useWebSocket() {
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({
    connected: false,
    backend_available: false,
    last_check: null,
  });
  const [events, setEvents] = useState<ProgressEvent[]>([]);
  const [currentProgress, setCurrentProgress] = useState<ProgressEvent | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    try {
      const ws = new WebSocket(WS_URL);

      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus({
          connected: true,
          backend_available: true,
          last_check: new Date(),
        });
      };

      ws.onmessage = (event) => {
        try {
          const data: ProgressEvent = JSON.parse(event.data);
          setEvents((prev) => [...prev.slice(-99), data]); // Keep last 100 events

          // Update current progress for active conversions
          if (
            data.type === 'conversion_started' ||
            data.type === 'conversion_progress' ||
            data.type === 'batch_started' ||
            data.type === 'batch_progress' ||
            data.type === 'workflow_started' ||
            data.type === 'workflow_step'
          ) {
            setCurrentProgress(data);
          } else if (
            data.type === 'conversion_complete' ||
            data.type === 'conversion_error' ||
            data.type === 'batch_complete' ||
            data.type === 'workflow_complete' ||
            data.type === 'workflow_error'
          ) {
            setCurrentProgress(null);
          }
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnectionStatus((prev) => ({
          ...prev,
          connected: false,
          last_check: new Date(),
        }));

        // Attempt to reconnect after 5 seconds
        reconnectTimeoutRef.current = window.setTimeout(() => {
          connect();
        }, 5000);
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus((prev) => ({
          ...prev,
          connected: false,
          backend_available: false,
          last_check: new Date(),
        }));
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
      setConnectionStatus({
        connected: false,
        backend_available: false,
        last_check: new Date(),
      });
    }
  }, []);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const clearEvents = useCallback(() => {
    setEvents([]);
  }, []);

  useEffect(() => {
    connect();
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    connectionStatus,
    events,
    currentProgress,
    clearEvents,
    reconnect: connect,
  };
}
