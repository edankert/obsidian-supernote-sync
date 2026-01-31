import { requestUrl, RequestUrlParam } from "obsidian";

// API Response Types
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

export type DependenciesResponse = Record<string, DependencyStatus>;

export interface ConversionResult {
  success: boolean;
  input_path: string;
  output_path?: string;
  message?: string;
  error?: string;
}

export interface Workflow {
  id: string;
  name: string;
  description: string | null;
  note_type: "standard" | "realtime";
  device: string;
  steps: WorkflowStep[];
}

export interface WorkflowStep {
  type: string;
  action: string;
  config: Record<string, unknown>;
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

// Conversion request types
export interface MarkdownToNoteRequest {
  input_path: string;
  output_path: string;
  device?: string;
  realtime?: boolean;
}

export interface NoteToMarkdownRequest {
  input_path: string;
  output_path: string;
}

/**
 * API client for communicating with the Obsidian-Supernote Sync backend.
 */
export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = "http://127.0.0.1:8765") {
    this.baseUrl = baseUrl.replace(/\/$/, ""); // Remove trailing slash
  }

  /**
   * Update the base URL for API requests.
   */
  setBaseUrl(url: string): void {
    this.baseUrl = url.replace(/\/$/, "");
  }

  /**
   * Make a request to the API.
   */
  private async request<T>(
    endpoint: string,
    options: Partial<RequestUrlParam> = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const response = await requestUrl({
      url,
      method: options.method || "GET",
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      body: options.body,
      throw: false,
    });

    if (response.status >= 400) {
      const error = response.json?.detail || response.text || "Request failed";
      throw new Error(`API Error (${response.status}): ${error}`);
    }

    return response.json as T;
  }

  /**
   * Check if the backend is available.
   */
  async checkConnection(): Promise<boolean> {
    try {
      await this.getStatus();
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Get backend status and version info.
   */
  async getStatus(): Promise<StatusResponse> {
    return this.request<StatusResponse>("/status");
  }

  /**
   * Get dependency status (pandoc, supernotelib, etc).
   */
  async getDependencies(): Promise<DependenciesResponse> {
    return this.request<DependenciesResponse>("/status/dependencies");
  }

  /**
   * Convert a markdown file to .note format.
   */
  async convertMarkdownToNote(
    request: MarkdownToNoteRequest
  ): Promise<ConversionResult> {
    return this.request<ConversionResult>("/convert/md-to-note", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  /**
   * Convert a .note file to markdown.
   */
  async convertNoteToMarkdown(
    request: NoteToMarkdownRequest
  ): Promise<ConversionResult> {
    return this.request<ConversionResult>("/convert/note-to-md", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  /**
   * List available workflows.
   */
  async listWorkflows(): Promise<Workflow[]> {
    return this.request<Workflow[]>("/workflows");
  }

  /**
   * Run a workflow.
   */
  async runWorkflow(
    workflowId: string,
    options: { source_folder?: string; output_folder?: string; dry_run?: boolean } = {}
  ): Promise<WorkflowRunResult> {
    return this.request<WorkflowRunResult>(`/workflows/${workflowId}/run`, {
      method: "POST",
      body: JSON.stringify(options),
    });
  }

  /**
   * Open the web dashboard in the default browser.
   */
  getDashboardUrl(): string {
    return this.baseUrl;
  }
}
