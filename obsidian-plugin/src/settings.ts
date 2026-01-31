import { App, PluginSettingTab, Setting } from "obsidian";
import type SupernoteSyncPlugin from "./main";

export interface SupernoteSyncSettings {
  backendUrl: string;
  defaultDevice: "A5X2" | "A5X" | "A6X2" | "A6X";
  defaultRealtime: boolean;
  defaultOutputFolder: string;
  showRibbonIcon: boolean;
  autoCheckConnection: boolean;
}

export const DEFAULT_SETTINGS: SupernoteSyncSettings = {
  backendUrl: "http://127.0.0.1:8765",
  defaultDevice: "A5X2",
  defaultRealtime: false,
  defaultOutputFolder: "",
  showRibbonIcon: true,
  autoCheckConnection: true,
};

export const DEVICES = [
  { id: "A5X2", name: "Manta (A5X2)", resolution: "1920 x 2560" },
  { id: "A5X", name: "A5X", resolution: "1404 x 1872" },
  { id: "A6X2", name: "Nomad (A6X2)", resolution: "1404 x 1872" },
  { id: "A6X", name: "A6X", resolution: "1404 x 1872" },
] as const;

export class SupernoteSyncSettingTab extends PluginSettingTab {
  plugin: SupernoteSyncPlugin;

  constructor(app: App, plugin: SupernoteSyncPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    // Connection section
    containerEl.createEl("h2", { text: "Connection" });

    new Setting(containerEl)
      .setName("Backend URL")
      .setDesc("URL of the Supernote Sync backend server")
      .addText((text) =>
        text
          .setPlaceholder("http://127.0.0.1:8765")
          .setValue(this.plugin.settings.backendUrl)
          .onChange(async (value) => {
            this.plugin.settings.backendUrl = value;
            await this.plugin.saveSettings();
            this.plugin.apiClient.setBaseUrl(value);
          })
      );

    new Setting(containerEl)
      .setName("Test connection")
      .setDesc("Check if the backend server is running")
      .addButton((button) =>
        button.setButtonText("Test").onClick(async () => {
          button.setDisabled(true);
          button.setButtonText("Testing...");
          try {
            const connected = await this.plugin.apiClient.checkConnection();
            if (connected) {
              const status = await this.plugin.apiClient.getStatus();
              button.setButtonText(`Connected (v${status.version})`);
            } else {
              button.setButtonText("Failed");
            }
          } catch (e) {
            button.setButtonText("Error");
            console.error("Connection test failed:", e);
          }
          setTimeout(() => {
            button.setDisabled(false);
            button.setButtonText("Test");
          }, 2000);
        })
      );

    new Setting(containerEl)
      .setName("Auto-check connection")
      .setDesc("Automatically check backend connection on startup")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.autoCheckConnection)
          .onChange(async (value) => {
            this.plugin.settings.autoCheckConnection = value;
            await this.plugin.saveSettings();
          })
      );

    // Conversion defaults section
    containerEl.createEl("h2", { text: "Conversion Defaults" });

    new Setting(containerEl)
      .setName("Default device")
      .setDesc("Supernote device model for conversions")
      .addDropdown((dropdown) => {
        DEVICES.forEach((device) => {
          dropdown.addOption(device.id, `${device.name} (${device.resolution})`);
        });
        dropdown.setValue(this.plugin.settings.defaultDevice);
        dropdown.onChange(async (value) => {
          this.plugin.settings.defaultDevice = value as SupernoteSyncSettings["defaultDevice"];
          await this.plugin.saveSettings();
        });
      });

    new Setting(containerEl)
      .setName("Enable Realtime by default")
      .setDesc("Enable Realtime handwriting recognition for new conversions")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.defaultRealtime)
          .onChange(async (value) => {
            this.plugin.settings.defaultRealtime = value;
            await this.plugin.saveSettings();
          })
      );

    new Setting(containerEl)
      .setName("Default output folder")
      .setDesc("Default folder for converted files (leave empty for same folder as input)")
      .addText((text) =>
        text
          .setPlaceholder("output/supernote")
          .setValue(this.plugin.settings.defaultOutputFolder)
          .onChange(async (value) => {
            this.plugin.settings.defaultOutputFolder = value;
            await this.plugin.saveSettings();
          })
      );

    // UI section
    containerEl.createEl("h2", { text: "Interface" });

    new Setting(containerEl)
      .setName("Show ribbon icon")
      .setDesc("Show the Supernote icon in the left ribbon")
      .addToggle((toggle) =>
        toggle
          .setValue(this.plugin.settings.showRibbonIcon)
          .onChange(async (value) => {
            this.plugin.settings.showRibbonIcon = value;
            await this.plugin.saveSettings();
            this.plugin.updateRibbonIcon();
          })
      );

    // Actions section
    containerEl.createEl("h2", { text: "Actions" });

    new Setting(containerEl)
      .setName("Open Dashboard")
      .setDesc("Open the Supernote Sync web dashboard in your browser")
      .addButton((button) =>
        button.setButtonText("Open").onClick(() => {
          window.open(this.plugin.apiClient.getDashboardUrl());
        })
      );
  }
}
