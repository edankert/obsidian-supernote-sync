import type {
  StatusResponse,
  DependenciesResponse,
  ConversionResult,
  BatchConversionResult,
  Workflow,
  WorkflowRunResult,
  DeviceType,
} from '../types';

const API_BASE = '/api';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

// Status endpoints
export async function getStatus(): Promise<StatusResponse> {
  return fetchJson<StatusResponse>('/status');
}

export async function getDependencies(): Promise<DependenciesResponse> {
  return fetchJson<DependenciesResponse>('/status/dependencies');
}

export async function checkHealth(): Promise<{ status: string }> {
  return fetchJson<{ status: string }>('/health');
}

// Conversion endpoints
export interface ConvertMarkdownRequest {
  input_path: string;
  output_path: string;
  device?: DeviceType;
  realtime?: boolean;
  page_size?: string;
  margin?: string;
  font_size?: number;
  update_markdown?: boolean;
}

export async function convertMarkdownToNote(
  request: ConvertMarkdownRequest
): Promise<ConversionResult> {
  return fetchJson<ConversionResult>('/convert/md-to-note', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export interface ConvertNoteRequest {
  input_path: string;
  output_path: string;
  image_dir?: string;
}

export async function convertNoteToMarkdown(
  request: ConvertNoteRequest
): Promise<ConversionResult> {
  return fetchJson<ConversionResult>('/convert/note-to-md', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export interface ConvertPdfRequest {
  input_path: string;
  output_path: string;
  device?: DeviceType;
  realtime?: boolean;
}

export async function convertPdfToNote(request: ConvertPdfRequest): Promise<ConversionResult> {
  return fetchJson<ConversionResult>('/convert/pdf-to-note', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export interface ConvertPngRequest {
  input_path: string;
  output_path: string;
  device?: DeviceType;
  template_name?: string;
  realtime?: boolean;
}

export async function convertPngToNote(request: ConvertPngRequest): Promise<ConversionResult> {
  return fetchJson<ConversionResult>('/convert/png-to-note', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export interface BatchConvertRequest {
  input_paths: string[];
  output_dir: string;
  conversion_type: 'md-to-note' | 'note-to-md' | 'pdf-to-note' | 'png-to-note';
  device?: DeviceType;
  realtime?: boolean;
}

export async function batchConvert(request: BatchConvertRequest): Promise<BatchConversionResult> {
  return fetchJson<BatchConversionResult>('/convert/batch', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// Workflow endpoints
export async function listWorkflows(): Promise<Workflow[]> {
  return fetchJson<Workflow[]>('/workflows');
}

export async function getWorkflow(id: string): Promise<Workflow> {
  return fetchJson<Workflow>(`/workflows/${id}`);
}

export interface WorkflowRunRequest {
  input_paths?: string[];
  output_dir?: string;
  dry_run?: boolean;
}

export async function runWorkflow(id: string, request: WorkflowRunRequest = {}): Promise<WorkflowRunResult> {
  return fetchJson<WorkflowRunResult>(`/workflows/${id}/run`, {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// File browsing endpoints
export interface FileInfo {
  name: string;
  path: string;
  is_dir: boolean;
  size: number | null;
  extension: string | null;
}

export interface BrowseResponse {
  current_path: string;
  parent_path: string | null;
  items: FileInfo[];
}

export interface DriveInfo {
  path: string;
  name: string;
}

export async function browseFiles(path?: string, filterExt?: string): Promise<BrowseResponse> {
  const params = new URLSearchParams();
  if (path) params.set('path', path);
  if (filterExt) params.set('filter_ext', filterExt);
  const query = params.toString();
  return fetchJson<BrowseResponse>(`/browse${query ? `?${query}` : ''}`);
}

export async function listDrives(): Promise<DriveInfo[]> {
  return fetchJson<DriveInfo[]>('/drives');
}

// Native file dialog
export interface FileDialogRequest {
  mode: 'file' | 'directory';
  title?: string;
  initial_dir?: string;
  file_types?: [string, string][]; // [name, pattern] pairs, e.g., ["Markdown", "*.md"]
}

export interface FileDialogResponse {
  selected: boolean;
  path: string | null;
}

export async function openFileDialog(request: FileDialogRequest): Promise<FileDialogResponse> {
  return fetchJson<FileDialogResponse>('/file-dialog', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}
