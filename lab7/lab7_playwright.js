// playwright-extra is a drop-in replacement for playwright,
// it augments the installed playwright with plugin functionality
import { chromium } from 'playwright-extra';

// Load the stealth plugin and use defaults (all tricks to hide playwright usage)
// Note: playwright-extra is compatible with most puppeteer-extra plugins
import stealth from 'puppeteer-extra-plugin-stealth';

// Add the plugin to Playwright (any number of plugins can be added)
chromium.use(stealth());

// That's it. The rest is Playwright usage as normal 😊
chromium.launch({ headless: true }).then(async (browser) => {
  const page = await browser.newPage();

  console.log('Testing the stealth plugin..');
  try {
    await page.goto('https://dcard.tw', { waitUntil: 'networkidle'  });
  } catch(Error) {
  }

  console.log('All done, check the page content. ✨');
  console.log(await page.content());
  await browser.close();
});
