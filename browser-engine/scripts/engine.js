const { chromium } = require('playwright');
const { stealth } = require('playwright-stealth');
const path = require('path');
const fs = require('fs');

class BrowserAutomation {
    constructor(sessionName = 'default') {
        this.sessionDir = path.join(__dirname, `../sessions/${sessionName}`);
        if (!fs.existsSync(this.sessionDir)) {
            fs.mkdirSync(this.sessionDir, { recursive: true });
        }
    }

    async init() {
        this.browserContext = await chromium.launchPersistentContext(this.sessionDir, {
            headless: false, // Set to true if you don't want to see it
            args: [
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--window-size=1280,720'
            ]
        });
        this.page = this.browserContext.pages()[0] || await this.browserContext.newPage();
        // await stealth(this.page);
    }

    async navigate(url) {
        await this.page.goto(url, { waitUntil: 'networkidle' });
        return await this.observe();
    }

    async observe() {
        const screenshotPath = path.join(__dirname, `../assets/observation_${Date.now()}.png`);
        await this.page.screenshot({ path: screenshotPath, fullPage: true });
        const content = await this.page.evaluate(() => document.body.innerText);
        return {
            url: this.page.url(),
            title: await this.page.title(),
            screenshot: screenshotPath,
            content: content.substring(0, 1500)
        };
    }

    async interact(type, selector, value = '') {
        try {
            if (type === 'click') {
                await this.page.click(selector);
            } else if (type === 'type') {
                await this.page.fill(selector, value);
            } else if (type === 'press') {
                await this.page.keyboard.press(value);
            } else if (type === 'solve_captcha') {
                // Future integration point for vision-based captcha solving
                console.log("Attempting vision-based captcha solve...");
            }
            await this.page.waitForTimeout(1000);
            return await this.observe();
        } catch (err) {
            return { status: 'error', message: err.message };
        }
    }

    async close() {
        await this.browserContext.close();
    }
}

module.exports = BrowserAutomation;
