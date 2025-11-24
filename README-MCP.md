# MCP Playwright Server Setup

This project includes an MCP (Model Context Protocol) server for Playwright browser automation.

## Quick Start

### Option 1: Direct npx command
```bash
npx @modelcontextprotocol/server-playwright
```

### Option 2: Using npm scripts
```bash
npm install
npm run mcp
```

### Option 3: Using provided scripts

**Windows:**
```cmd
start-mcp-playwright.bat
```

**Unix/Linux/macOS:**
```bash
chmod +x start-mcp-playwright.sh
./start-mcp-playwright.sh
```

## What is MCP Playwright Server?

The MCP Playwright server provides browser automation capabilities through the Model Context Protocol, allowing AI assistants to:

- Navigate web pages
- Click elements
- Fill forms
- Take screenshots
- Extract page content
- Interact with web applications

## Integration with RAG Chatbot

The MCP Playwright server can be used alongside the RAG chatbot to:

1. **Automated Testing**: Test the web interface programmatically
2. **Content Extraction**: Extract content from web pages for indexing
3. **User Interaction Simulation**: Simulate user workflows
4. **Screenshot Generation**: Capture UI states for documentation

## Usage Examples

Once the MCP server is running, it can be connected to compatible AI assistants that support the Model Context Protocol for browser automation tasks.

## Requirements

- Node.js (latest LTS version recommended)
- Internet connection (for npx to download packages)
- Compatible AI assistant with MCP support

## Troubleshooting

If you encounter issues:

1. Ensure Node.js is installed: `node --version`
2. Check internet connection for package downloads
3. Try clearing npm cache: `npm cache clean --force`
4. Reinstall dependencies: `rm -rf node_modules && npm install`