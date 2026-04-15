const BrowserAutomation = require('./engine');
const fs = require('fs');
const path = require('path');

async function main() {
    const args = process.argv.slice(2);
    const [command, target, actionData] = args;
    const session = actionData ? JSON.parse(actionData).session || 'default' : 'default';

    const automation = new BrowserAutomation(session);
    await automation.init();

    try {
        if (command === 'navigate') {
            const result = await automation.navigate(target);
            console.log(JSON.stringify(result, null, 2));
        } else if (command === 'interact') {
            const data = JSON.parse(actionData);
            const result = await automation.interact(data.type, data.selector, data.value);
            console.log(JSON.stringify(result, null, 2));
        } else if (command === 'solve_captcha') {
            // This would be the vision integration point
            const state = await automation.observe();
            console.log(JSON.stringify({ status: 'needs_vision', screenshot: state.screenshot }));
        }
    } catch (err) {
        console.error(JSON.stringify({ status: 'error', message: err.message }));
    } finally {
        await automation.close();
    }
}

main();
