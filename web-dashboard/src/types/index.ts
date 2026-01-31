// API Types

export interface StatusResponse {
  status: string;
  version: string;
  timestamp: string;
  uptime_seconds: number | null;
}

export interface DependencyStatus {
  name: string;
  available: boolean;
  version: string | null;
  path: string | null;
}

// Backend returns dict[str, DependencyStatus]
export type DependenciesResponse = Record<string, DependencyStatus>;

export interface ConversionResult {
  success: boolean;
  input_path: string;
  output_path?: string;
  message?: string;
  error?: string;
}

export interface BatchConversionResult {
  total: number;
  successful: number;
  failed: number;
  results: ConversionResult[];
}

// Workflow Types

export interface WorkflowStep {
  type: string;
  action: string;
  config: Record<string, unknown>;
}

export interface Workflow {
  id: string;
  name: string;
  description: string | null;
  note_type: 'standard' | 'realtime';
  device: string;
  steps: WorkflowStep[];
  created_at?: string;
  updated_at?: string;
}

export interface WorkflowRunResult {
  workflow_id: string;
  success: boolean;
  files_processed: number;
  files_succeeded: number;
  files_failed: number;
  errors: string[];
  output_files: string[];
  dry_run: boolean;
}

// WebSocket Event Types

export type EventType =
  | 'connected'
  | 'disconnected'
  | 'conversion_started'
  | 'conversion_progress'
  | 'conversion_complete'
  | 'conversion_error'
  | 'batch_started'
  | 'batch_progress'
  | 'batch_complete'
  | 'workflow_started'
  | 'workflow_step'
  | 'workflow_complete'
  | 'workflow_error';

export interface ProgressEvent {
  type: EventType;
  conversion_type?: string;
  input_path?: string;
  output_path?: string;
  percent?: number;
  message?: string;
  error?: string;
  total?: number;
  current?: number;
  workflow_id?: string;
  step?: number;
}

// UI State Types

export interface ConnectionStatus {
  connected: boolean;
  backend_available: boolean;
  last_check: Date | null;
}

export type DeviceType = 'A5X2' | 'A5X' | 'A6X2' | 'A6X';

export const DEVICES: { id: DeviceType; name: string; resolution: string }[] = [
  { id: 'A5X2', name: 'Manta (A5X2)', resolution: '1920 x 2560' },
  { id: 'A5X', name: 'A5X', resolution: '1404 x 1872' },
  { id: 'A6X2', name: 'Nomad (A6X2)', resolution: '1404 x 1872' },
  { id: 'A6X', name: 'A6X', resolution: '1404 x 1872' },
];
