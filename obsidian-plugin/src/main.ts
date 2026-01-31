import {
  App,
  Menu,
  Notice,
  Plugin,
  TFile,
  TFolder,
  addIcon,
} from "obsidian";
import { ApiClient } from "./api-client";
import {
  SupernoteSyncSettings,
  SupernoteSyncSettingTab,
  DEFAULT_SETTINGS,
} from "./settings";

// Custom Supernote icon (stylized pen/tablet)
const SUPERNOTE_ICON = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="currentColor">
  <rect x="15" y="10" width="70" height="80" rx="5" ry="5" stroke="currentColor" stroke-width="4" fill="none"/>
  <line x1="25" y1="25" x2="75" y2="25" stroke="currentColor" stroke-width="3"/>
  <line x1="25" y1="40" x2="65" y2="40" stroke="currentColor" stroke-width="3"/>
  <line x1="25" y1="55" x2="70" y2="55" stroke="currentColor" stroke-width="3"/>
  <path d="M60 65 L75 80 L78 77 L63 62 Z" fill="currentColor"/>
  <path d="M78 77 L82 73 L67 58 L63 62 Z" fill="currentColor"/>
</svg>`;

export default class SupernoteSyncPlugin extends Plugin {
  settings: SupernoteSyncSettings = DEFAULT_SETTINGS;
  apiClient: ApiClient = new ApiClient();
  private ribbonIconEl: HTMLElement | null = null;
  private statusBarEl: HTMLElement | null = null;
  private connected: boolean = false;

  async onload() {
    await this.loadSettings();

    // Register custom icon
    addIcon("supernote", SUPERNOTE_ICON);

    // Initialize API client with saved URL
    this.apiClient.setBaseUrl(this.settings.backendUrl);

    // Add ribbon icon
    this.updateRibbonIcon();

    // Add status bar item
    this.statusBarEl = this.addStatusBarItem();
    this.updateStatusBar("Checking...");

    // Register commands
    this.registerCommands();

    // Register file menu items
    this.registerFileMenuItems();

    // Add settings tab
    this.addSettingTab(new SupernoteSyncSettingTab(this.app, this));

    // Check connection on startup
    if (this.settings.autoCheckConnection) {
      this.checkConnection();
    }
  }

  onunload() {
    // Cleanup
  }

  /**
   * Load plugin settings from storage.
   */
  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  /**
   * Save plugin settings to storage.
   */
  async saveSettings() {
    await this.saveData(this.settings);
  }

  /**
   * Update the ribbon icon visibility.
   */
  updateRibbonIcon() {
    // Remove existing icon if present
    if (this.ribbonIconEl) {
      this.ribbonIconEl.remove();
      this.ribbonIconEl = null;
    }

    // Add icon if enabled
    if (this.settings.showRibbonIcon) {
      this.ribbonIconEl = this.addRibbonIcon(
        "supernote",
        "Supernote Sync",
        (evt: MouseEvent) => {
          this.showRibbonMenu(evt);
        }
      );
    }
  }

  /**
   * Show the ribbon icon context menu.
   */
  private showRibbonMenu(evt: MouseEvent) {
    const menu = new Menu();

    menu.addItem((item) =>
      item
        .setTitle("Convert current file")
        .setIcon("file-output")
        .onClick(() => this.convertCurrentFile())
    );

    menu.addItem((item) =>
      item
        .setTitle("Open Dashboard")
        .setIcon("external-link")
        .onClick(() => this.openDashboard())
    );

    menu.addSeparator();

    menu.addItem((item) =>
      item
        .setTitle("Check connection")
        .setIcon("refresh-cw")
        .onClick(() => this.checkConnection())
    );

    menu.addItem((item) =>
      item
        .setTitle("Settings")
        .setIcon("settings")
        .onClick(() => {
          // Open settings tab
          const setting = (this.app as any).setting;
          setting.open();
          setting.openTabById("supernote-sync");
        })
    );

    menu.showAtMouseEvent(evt);
  }

  /**
   * Register plugin commands.
   */
  private registerCommands() {
    // Convert current file to .note
    this.addCommand({
      id: "convert-to-note",
      name: "Convert current file to Supernote",
      checkCallback: (checking: boolean) => {
        const file = this.app.workspace.getActiveFile();
        if (file && file.extension === "md") {
          if (!checking) {
            this.convertCurrentFile();
          }
          return true;
        }
        return false;
      },
    });

    // Open dashboard
    this.addCommand({
      id: "open-dashboard",
      name: "Open Supernote Sync Dashboard",
      callback: () => this.openDashboard(),
    });

    // Check connection
    this.addCommand({
      id: "check-connection",
      name: "Check backend connection",
      callback: () => this.checkConnection(),
    });

    // Convert file with dialog
    this.addCommand({
      id: "convert-with-options",
      name: "Convert file with options...",
      callback: () => this.convertWithOptions(),
    });
  }

  /**
   * Register file menu context items.
   */
  private registerFileMenuItems() {
    // File menu (right-click on file)
    this.registerEvent(
      this.app.workspace.on("file-menu", (menu, file) => {
        if (file instanceof TFile && file.extension === "md") {
          menu.addItem((item) => {
            item
              .setTitle("Convert to Supernote")
              .setIcon("supernote")
              .onClick(() => this.convertFile(file));
          });
        }
      })
    );

    // Editor menu (right-click in editor)
    this.registerEvent(
      this.app.workspace.on("editor-menu", (menu, editor, view) => {
        const file = view.file;
        if (file && file.extension === "md") {
          menu.addItem((item) => {
            item
              .setTitle("Convert to Supernote")
              .setIcon("supernote")
              .onClick(() => this.convertFile(file));
          });
        }
      })
    );
  }

  /**
   * Update the status bar text.
   */
  private updateStatusBar(text: string) {
    if (this.statusBarEl) {
      this.statusBarEl.setText(`Supernote: ${text}`);
    }
  }

  /**
   * Check connection to the backend.
   */
  async checkConnection() {
    this.updateStatusBar("Checking...");
    try {
      const isConnected = await this.apiClient.checkConnection();
      this.connected = isConnected;
      if (isConnected) {
        const status = await this.apiClient.getStatus();
        this.updateStatusBar(`Connected (v${status.version})`);
      } else {
        this.updateStatusBar("Disconnected");
      }
    } catch (e) {
      this.connected = false;
      this.updateStatusBar("Error");
      console.error("Connection check failed:", e);
    }
  }

  /**
   * Open the web dashboard.
   */
  openDashboard() {
    window.open(this.apiClient.getDashboardUrl());
  }

  /**
   * Convert the currently active file.
   */
  async convertCurrentFile() {
    const file = this.app.workspace.getActiveFile();
    if (!file) {
      new Notice("No file is currently open");
      return;
    }
    if (file.extension !== "md") {
      new Notice("Current file is not a markdown file");
      return;
    }
    await this.convertFile(file);
  }

  /**
   * Convert a specific file to .note format.
   */
  async convertFile(file: TFile) {
    if (!this.connected) {
      const isConnected = await this.apiClient.checkConnection();
      if (!isConnected) {
        new Notice("Backend not connected. Please start the server.");
        return;
      }
      this.connected = true;
    }

    // Get the vault path
    const vaultPath = (this.app.vault.adapter as any).basePath;
    const inputPath = `${vaultPath}/${file.path}`;

    // Determine output path
    let outputPath: string;
    if (this.settings.defaultOutputFolder) {
      const outputFolder = this.settings.defaultOutputFolder;
      const fileName = file.basename + ".note";
      outputPath = `${vaultPath}/${outputFolder}/${fileName}`;
    } else {
      outputPath = inputPath.replace(/\.md$/, ".note");
    }

    new Notice(`Converting ${file.name}...`);

    try {
      const result = await this.apiClient.convertMarkdownToNote({
        input_path: inputPath,
        output_path: outputPath,
        device: this.settings.defaultDevice,
        realtime: this.settings.defaultRealtime,
      });

      if (result.success) {
        new Notice(`Converted: ${file.name} → ${file.basename}.note`);
      } else {
        new Notice(`Conversion failed: ${result.error || result.message}`);
      }
    } catch (e) {
      const message = e instanceof Error ? e.message : "Unknown error";
      new Notice(`Conversion error: ${message}`);
      console.error("Conversion failed:", e);
    }
  }

  /**
   * Convert with options dialog (opens dashboard).
   */
  convertWithOptions() {
    // For now, just open the dashboard which has the full UI
    new Notice("Opening dashboard for advanced options...");
    this.openDashboard();
  }
}
