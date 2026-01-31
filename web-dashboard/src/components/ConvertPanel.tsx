import { useState } from 'react';
import { DEVICES, type DeviceType } from '../types';
import * as api from '../api/client';

type ConversionType = 'md-to-note' | 'note-to-md' | 'pdf-to-note' | 'png-to-note';

const CONVERSION_TYPES: { id: ConversionType; label: string; inputExt: string; outputExt: string }[] = [
  { id: 'md-to-note', label: 'Markdown to .note', inputExt: '.md', outputExt: '.note' },
  { id: 'note-to-md', label: '.note to Markdown', inputExt: '.note', outputExt: '.md' },
  { id: 'pdf-to-note', label: 'PDF to .note', inputExt: '.pdf', outputExt: '.note' },
  { id: 'png-to-note', label: 'PNG to .note', inputExt: '.png', outputExt: '.note' },
];

export function ConvertPanel() {
  const [conversionType, setConversionType] = useState<ConversionType>('md-to-note');
  const [inputPath, setInputPath] = useState('');
  const [outputPath, setOutputPath] = useState('');
  const [device, setDevice] = useState<DeviceType>('A5X2');
  const [realtime, setRealtime] = useState(false);
  const [converting, setConverting] = useState(false);
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null);

  const [browsing, setBrowsing] = useState(false);

  const selectedType = CONVERSION_TYPES.find((t) => t.id === conversionType)!;
  const showDeviceOptions = conversionType !== 'note-to-md';

  const handleConvert = async () => {
    if (!inputPath || !outputPath) {
      setResult({ success: false, message: 'Please enter input and output paths' });
      return;
    }

    setConverting(true);
    setResult(null);

    try {
      let response;
      switch (conversionType) {
        case 'md-to-note':
          response = await api.convertMarkdownToNote({
            input_path: inputPath,
            output_path: outputPath,
            device,
            realtime,
          });
          break;
        case 'note-to-md':
          response = await api.convertNoteToMarkdown({
            input_path: inputPath,
            output_path: outputPath,
          });
          break;
        case 'pdf-to-note':
          response = await api.convertPdfToNote({
            input_path: inputPath,
            output_path: outputPath,
            device,
            realtime,
          });
          break;
        case 'png-to-note':
          response = await api.convertPngToNote({
            input_path: inputPath,
            output_path: outputPath,
            device,
            realtime,
          });
          break;
      }

      setResult({
        success: response.success,
        message: response.message || response.error || 'Conversion complete',
      });
    } catch (e) {
      setResult({
        success: false,
        message: e instanceof Error ? e.message : 'Conversion failed',
      });
    } finally {
      setConverting(false);
    }
  };

  const openInputBrowser = async () => {
    setBrowsing(true);
    try {
      // Map extension to file type filter
      const fileTypes: [string, string][] = [];
      if (selectedType.inputExt === '.md') {
        fileTypes.push(['Markdown', '*.md']);
      } else if (selectedType.inputExt === '.note') {
        fileTypes.push(['Supernote', '*.note']);
      } else if (selectedType.inputExt === '.pdf') {
        fileTypes.push(['PDF', '*.pdf']);
      } else if (selectedType.inputExt === '.png') {
        fileTypes.push(['PNG Image', '*.png']);
      }

      const result = await api.openFileDialog({
        mode: 'file',
        title: `Select ${selectedType.inputExt} File`,
        file_types: fileTypes,
      });

      if (result.selected && result.path) {
        setInputPath(result.path);
        // Auto-suggest output path based on input
        if (!outputPath) {
          const inputName = result.path.replace(/\.[^/.]+$/, ''); // Remove extension
          setOutputPath(inputName + selectedType.outputExt);
        }
      }
    } catch (e) {
      console.error('Failed to open file dialog:', e);
    } finally {
      setBrowsing(false);
    }
  };

  const openOutputBrowser = async () => {
    setBrowsing(true);
    try {
      const result = await api.openFileDialog({
        mode: 'directory',
        title: 'Select Output Directory',
      });

      if (result.selected && result.path) {
        // If input path is set, suggest filename based on it
        if (inputPath) {
          const inputName = inputPath.split(/[/\\]/).pop()?.replace(/\.[^/.]+$/, '') || 'output';
          setOutputPath(`${result.path}/${inputName}${selectedType.outputExt}`);
        } else {
          setOutputPath(result.path);
        }
      }
    } catch (e) {
      console.error('Failed to open file dialog:', e);
    } finally {
      setBrowsing(false);
    }
  };

  return (
    <>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
          Quick Convert
        </h2>

        <div className="space-y-4">
          {/* Conversion Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Conversion Type
            </label>
            <select
              value={conversionType}
              onChange={(e) => setConversionType(e.target.value as ConversionType)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              {CONVERSION_TYPES.map((type) => (
                <option key={type.id} value={type.id}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          {/* Input Path */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Input File ({selectedType.inputExt})
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={inputPath}
                onChange={(e) => setInputPath(e.target.value)}
                placeholder={`Select or enter path to ${selectedType.inputExt} file`}
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm"
              />
              <button
                onClick={openInputBrowser}
                disabled={browsing}
                className="px-3 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
                title="Browse files"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
              </button>
            </div>
          </div>

          {/* Output Path */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Output File ({selectedType.outputExt})
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={outputPath}
                onChange={(e) => setOutputPath(e.target.value)}
                placeholder="Auto-filled from input, or browse to select"
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm"
              />
              <button
                onClick={openOutputBrowser}
                disabled={browsing}
                className="px-3 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
                title="Browse directory"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
              </button>
            </div>
          </div>

          {/* Device Selection (for to-note conversions) */}
          {showDeviceOptions && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Device
                </label>
                <select
                  value={device}
                  onChange={(e) => setDevice(e.target.value as DeviceType)}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                >
                  {DEVICES.map((d) => (
                    <option key={d.id} value={d.id}>
                      {d.name} ({d.resolution})
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="realtime"
                  checked={realtime}
                  onChange={(e) => setRealtime(e.target.checked)}
                  className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                />
                <label
                  htmlFor="realtime"
                  className="text-sm text-gray-700 dark:text-gray-300"
                >
                  Enable Realtime handwriting recognition
                </label>
              </div>
            </>
          )}

          {/* Convert Button */}
          <button
            onClick={handleConvert}
            disabled={converting}
            className={`w-full py-2 px-4 rounded-lg font-medium text-white transition-colors ${
              converting
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-indigo-600 hover:bg-indigo-700'
            }`}
          >
            {converting ? 'Converting...' : 'Convert'}
          </button>

          {/* Result */}
          {result && (
            <div
              className={`p-3 rounded-lg text-sm ${
                result.success
                  ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300'
                  : 'bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300'
              }`}
            >
              {result.message}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
