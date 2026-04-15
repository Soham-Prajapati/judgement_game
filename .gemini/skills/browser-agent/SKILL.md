---
name: browser-agent
description: Access the internet, perform logins, retrieve API keys, and solve CAPTCHAs using Playwright.
---

# Browser Agent

## Overview

This skill allows Gemini CLI to interact with the web directly. It uses Playwright to navigate, click, type, and scrape content. It is designed to handle complex workflows like logging into dashboards (Supabase, GitHub) to retrieve API keys or configure settings while you focus on other tasks.

**Security Warning:** This tool can access sensitive information. Never log or share credentials. Use a persistent browser session to avoid repeated logins.

## Capabilities

### 1. Navigate & Observe
Use this to go to a URL and get a screenshot + page overview.
- **Trigger:** "Go to [URL]", "Open [URL]"
- **Action:** Run `node scripts/browser_controller.js navigate [URL]`
- **Validation:** `read_file` the screenshot at `assets/last_screen.png` to understand the page state.

### 2. Interact
Perform actions like clicking buttons or typing into forms.
- **Trigger:** "Click the login button", "Type my email into the username field"
- **Action:** Run `node scripts/browser_controller.js action [URL] '{"type": "click", "selector": "[SELECTOR]"}'`
- **Tip:** Use CSS selectors or text-based selectors supported by Playwright.

### 3. Solve CAPTCHA
If a CAPTCHA is detected in the screenshot:
- **Action:** Take a high-res screenshot of the CAPTCHA area.
- **Analysis:** Use the internal vision model to read the characters or identify the correct images.
- **Execution:** Use the `action` command to type the solution or click the specified coordinates.

### 4. Extract API Keys
- **Trigger:** "Get my Supabase keys", "Find the OpenAI API key"
- **Process:**
  1. Navigate to the platform's dashboard.
  2. Handle login (if needed, use credentials from `.env` or ask user for MFA).
  3. Navigate to the API/Settings section.
  4. Scrape the keys and save them to `.env` or the requested file.

## Usage Workflow

1. **Activation:** The user asks to do something on the web.
2. **Navigation:** Go to the target site.
3. **Loop:**
   - Screenshot -> `read_file` -> Analyze.
   - If blocked by login -> Try to log in.
   - If blocked by CAPTCHA -> Solve it.
   - Perform the target action.
4. **Completion:** Report the result (e.g., "API Key saved to .env").

## Persistence
All session data (cookies, local storage) is stored in `assets/user_data`. This means you only need to log in once for most sites.

---

**Rules:**
- ALWAYS check the screenshot before taking an action.
- NEVER output raw API keys in the chat unless specifically asked.
- If MFA is required and not automated, ASK the user for the code.
