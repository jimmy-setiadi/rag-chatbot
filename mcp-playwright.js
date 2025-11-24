#!/usr/bin/env node

/**
 * MCP Server for Playwright - Browser automation capabilities
 * Usage: npx @modelcontextprotocol/server-playwright
 */

const { spawn } = require('child_process');
const path = require('path');

// Start MCP Playwright server using npx
function startMCPPlaywrightServer() {
    console.log('Starting MCP Playwright Server...');
    
    const mcpProcess = spawn('npx', ['@modelcontextprotocol/server-playwright'], {
        stdio: 'inherit',
        shell: true,
        cwd: __dirname
    });

    mcpProcess.on('error', (error) => {
        console.error('Failed to start MCP Playwright server:', error);
    });

    mcpProcess.on('close', (code) => {
        console.log(`MCP Playwright server exited with code ${code}`);
    });

    // Handle graceful shutdown
    process.on('SIGINT', () => {
        console.log('\nShutting down MCP Playwright server...');
        mcpProcess.kill('SIGINT');
        process.exit(0);
    });

    return mcpProcess;
}

if (require.main === module) {
    startMCPPlaywrightServer();
}

module.exports = { startMCPPlaywrightServer };