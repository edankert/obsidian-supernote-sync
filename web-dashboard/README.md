# Obsidian-Supernote Sync Web Dashboard

A React-based web interface for the Obsidian-Supernote Sync tool.

## Features

- **Workflow Management**: View and run pre-defined workflows (Daily Notes, Research, World Building)
- **Quick Convert**: Manual file conversion panel for individual files
- **Status Display**: Real-time connection status with backend
- **Progress Tracking**: WebSocket-based progress updates during conversions

## Development

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The development server runs at `http://localhost:5173` and proxies API requests to `http://localhost:8765`.

### Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

The built files are output to `dist/`.

## Using with Python Backend

1. Start the Python backend:
   ```bash
   cd ..  # Go to project root
   obsidian-supernote serve
   ```

2. In another terminal, start the dashboard dev server:
   ```bash
   npm run dev
   ```

3. Open `http://localhost:5173` in your browser.

### Production Deployment

For production, serve the built dashboard through the Python backend:

```bash
# Build the dashboard
npm run build

# Start backend with dashboard
cd ..
obsidian-supernote serve --dashboard web-dashboard/dist
```

Then access the dashboard at `http://localhost:8765/dashboard`.

## Tech Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **WebSocket** - Real-time updates

## Project Structure

```
src/
├── api/           # API client for backend communication
│   └── client.ts
├── components/    # React components
│   ├── ConvertPanel.tsx
│   ├── ProgressIndicator.tsx
│   ├── StatusBar.tsx
│   ├── WorkflowCard.tsx
│   └── index.ts
├── hooks/         # React hooks
│   ├── useApi.ts
│   └── useWebSocket.ts
├── types/         # TypeScript type definitions
│   └── index.ts
├── App.tsx        # Main application component
├── main.tsx       # Entry point
└── index.css      # Global styles with Tailwind
```
