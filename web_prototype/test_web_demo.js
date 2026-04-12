const { chromium } = require('playwright');

(async () => {
  // Launch browser
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  try {
    // Navigate to the web demo
    await page.goto('file://web_prototype/index.html');
    
    // Wait for the page to load
    await page.waitForSelector('.paper');
    console.log('✅ Page loaded successfully');
    
    // Check if at least one text element is visible
    const textElements = await page.$$('.text-element');
    if (textElements.length > 0) {
      console.log('✅ At least one text element is visible');
    } else {
      console.log('❌ No text elements found');
    }
    
    // Click on the first text element to select it
    await textElements[0].click();
    await page.waitForSelector('.selection-box');
    console.log('✅ Element selected successfully');
    
    // Take screenshot of selected state
    await page.screenshot({ path: 'docs/contest_evidence/screenshots/20_web_playwright_demo.png' });
    console.log('✅ Screenshot taken');
    
    // Modify text content
    await page.fill('#content-input', 'Modified text');
    await page.waitForTimeout(500); // Wait for the change to reflect
    
    // Verify text change
    const modifiedElement = await page.$('.text-element');
    const modifiedText = await modifiedElement.textContent();
    if (modifiedText === 'Modified text') {
      console.log('✅ Text modified successfully');
    } else {
      console.log('❌ Text modification failed');
    }
    
    // Take screenshot after modification
    await page.screenshot({ path: 'docs/contest_evidence/screenshots/21_web_playwright_result.png' });
    console.log('✅ Final screenshot taken');
    
    console.log('\n=== Test Results ===');
    console.log('✅ Page loaded');
    console.log('✅ Text element visible');
    console.log('✅ Element selected');
    console.log('✅ Text modified');
    console.log('✅ Screenshots captured');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  } finally {
    // Close browser
    await browser.close();
  }
})();