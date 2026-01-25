import { useState, useEffect, useCallback } from 'react';
import * as api from '../api/client';
import type { StatusResponse, DependenciesResponse, Workflow } from '../types';

export function useStatus() {
  const [status, setStatus] = useState<StatusResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getStatus();
      setStatus(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to fetch status');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
    // Refresh every 30 seconds
    const interval = setInterval(refresh, 30000);
    return () => clearInterval(interval);
  }, [refresh]);

  return { status, loading, error, refresh };
}

export function useDependencies() {
  const [dependencies, setDependencies] = useState<DependenciesResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getDependencies();
      setDependencies(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to fetch dependencies');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { dependencies, loading, error, refresh };
}

export function useWorkflows() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.listWorkflows();
      setWorkflows(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to fetch workflows');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const runWorkflow = useCallback(async (id: string) => {
    try {
      const result = await api.runWorkflow(id);
      return result;
    } catch (e) {
      throw e instanceof Error ? e : new Error('Failed to run workflow');
    }
  }, []);

  return { workflows, loading, error, refresh, runWorkflow };
}
