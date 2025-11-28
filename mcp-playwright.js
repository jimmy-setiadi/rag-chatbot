#!/usr/bin/env node

/**
 * Simple MCP-style Playwright Server
 * Provides browser automation capabilities
 */

const { chromium } = require('playwright');
const readline = require('readline');

class PlaywrightMCPServer {
    constructor() {
        this.browser = null;
        this.page = null;
        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
    }

    async start() {
        console.log('🎭 MCP Playwright Server Starting...');
        console.log('Available commands:');
        console.log('  open <url>     - Open a webpage');
        console.log('  screenshot     - Take a screenshot');
        console.log('  click <selector> - Click an element');
        console.log('  type <selector> <text> - Type text');
        console.log('  content        - Get page content');
        console.log('  close          - Close browser');
        console.log('  help           - Show this help');
        console.log('  exit           - Exit server');
        console.log('');

        this.rl.on('line', async (input) => {
            await this.handleCommand(input.trim());
        });

        this.rl.on('close', () => {
            this.cleanup();
        });
    }

    async handleCommand(command) {
        const parts = command.split(' ');
        const cmd = parts[0].toLowerCase();

        try {
            switch (cmd) {
                case 'open':
                    await this.openPage(parts[1]);
                    break;
                case 'screenshot':
                    await this.takeScreenshot();
                    break;
                case 'click':
                    await this.clickElement(parts[1]);
                    break;
                case 'type':
                    await this.typeText(parts[1], parts.slice(2).join(' '));
                    break;
                case 'content':
                    await this.getContent();
                    break;
                case 'close':
                    await this.closeBrowser();
                    break;
                case 'help':
                    this.showHelp();
                    break;
                case 'exit':
                    this.rl.close();
                    break;
                default:
                    console.log('❌ Unknown command. Type "help" for available commands.');
            }
        } catch (error) {
            console.log(`❌ Error: ${error.message}`);
        }
    }

    async ensureBrowser() {
        if (!this.browser) {
            console.log('🚀 Launching browser...');
            this.browser = await chromium.launch({ headless: false });
            this.page = await this.browser.newPage();
        }
    }

    async openPage(url) {
        if (!url) {
            console.log('❌ Please provide a URL');
            return;
        }
        await this.ensureBrowser();
        console.log(`🌐 Opening ${url}...`);
        await this.page.goto(url);
        console.log('✅ Page loaded successfully');
    }

    async takeScreenshot() {
        if (!this.page) {
            console.log('❌ No page open. Use "open <url>" first.');
            return;
        }
        const filename = `screenshot-${Date.now()}.png`;
        await this.page.screenshot({ path: filename });
        console.log(`📸 Screenshot saved as ${filename}`);
    }

    async clickElement(selector) {
        if (!selector) {
            console.log('❌ Please provide a CSS selector');
            return;
        }
        if (!this.page) {
            console.log('❌ No page open. Use "open <url>" first.');
            return;
        }
        await this.page.click(selector);
        console.log(`🖱️ Clicked element: ${selector}`);
    }

    async typeText(selector, text) {
        if (!selector || !text) {
            console.log('❌ Please provide selector and text');
            return;
        }
        if (!this.page) {
            console.log('❌ No page open. Use "open <url>" first.');
            return;
        }
        await this.page.fill(selector, text);
        console.log(`⌨️ Typed "${text}" into ${selector}`);
    }

    async getContent() {
        if (!this.page) {
            console.log('❌ No page open. Use "open <url>" first.');
            return;
        }
        const title = await this.page.title();
        const url = this.page.url();
        console.log(`📄 Page Title: ${title}`);
        console.log(`🔗 URL: ${url}`);
    }

    async closeBrowser() {
        if (this.browser) {
            await this.browser.close();
            this.browser = null;
            this.page = null;
            console.log('🔒 Browser closed');
        } else {
            console.log('❌ No browser to close');
        }
    }

    showHelp() {
        console.log('\n📖 Available commands:');
        console.log('  open <url>     - Open a webpage');
        console.log('  screenshot     - Take a screenshot');
        console.log('  click <selector> - Click an element');
        console.log('  type <selector> <text> - Type text');
        console.log('  content        - Get page content');
        console.log('  close          - Close browser');
        console.log('  help           - Show this help');
        console.log('  exit           - Exit server\n');
    }

    async cleanup() {
        if (this.browser) {
            await this.browser.close();
        }
        console.log('\n👋 MCP Playwright Server stopped');
        process.exit(0);
    }
}

if (require.main === module) {
    const server = new PlaywrightMCPServer();
    server.start().catch(console.error);
}

module.exports = { PlaywrightMCPServer };