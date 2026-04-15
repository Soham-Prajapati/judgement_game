const { chromium } = require('playwright');
const { stealth } = require('playwright-stealth');
const path = require('path');
const fs = require('fs');

async function run() {
    const args = process.argv.slice(2);
    const command = args[0];
    const targetUrl = args[1];
    const actionData = args[2] ? JSON.parse(args[2]) : {};

    // Persistent user data directory to maintain sessions
    const userDataDir = path.join(__dirname, '../assets/user_data');
    if (!fs.existsSync(userDataDir)) {
        fs.mkdirSync(userDataDir, { recursive: true });
    }

    const browserContext = await chromium.launchPersistentContext(userDataDir, {
        headless: actionData.headless !== false,
        args: [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-setuid-sandbox'
        ]
    });

    // Add stealth plugin to all pages
    const page = browserContext.pages()[0] || await browserContext.newPage();
    // await stealth(page); // Some versions might need this differently

    try {
        if (command === 'navigate') {
            await page.goto(targetUrl, { waitUntil: 'networkidle' });
            const screenshotPath = path.join(__dirname, '../assets/last_screen.png');
            await page.screenshot({ path: screenshotPath, fullPage: true });
            console.log(JSON.stringify({
                status: 'success',
                screenshot: screenshotPath,
                url: page.url(),
                title: await page.title()
            }));
        } else if (command === 'action') {
            // actionData: { type: 'click'|'type'|'select', selector: '...', value: '...' }
            if (actionData.type === 'click') {
                await page.click(actionData.selector);
            } else if (actionData.type === 'type') {
                await page.fill(actionData.selector, actionData.value);
            } else if (actionData.type === 'press') {
                await page.keyboard.press(actionData.value);
            }
            
            await page.waitForTimeout(1000); // Wait for potential updates
            const screenshotPath = path.join(__dirname, '../assets/last_screen.png');
            await page.screenshot({ path: screenshotPath, fullPage: true });
            console.log(JSON.stringify({
                status: 'success',
                screenshot: screenshotPath,
                url: page.url()
            }));
        } else if (command === 'scrape') {
            const content = await page.evaluate(() => document.body.innerText);
            console.log(JSON.stringify({
                status: 'success',
                content: content.substring(0, 2000) // Truncate for safety
            }));
        }
    } catch (err) {
        console.error(JSON.stringify({
            status: 'error',
            message: err.message
        }));
    } finally {
        await browserContext.close();
    }
}

run();
