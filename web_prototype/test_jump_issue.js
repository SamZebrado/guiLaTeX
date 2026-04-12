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
    
    // Get the first text element
    const textElement = await page.$('.text-element');
    if (!textElement) {
      console.log('❌ No text elements found');
      return;
    }
    
    // Get initial position
    const initialBox = await textElement.boundingBox();
    console.log('✅ Initial position:', initialBox);
    
    // Click on the element to select it
    await textElement.click();
    await page.waitForSelector('.selection-box');
    console.log('✅ Element selected successfully');
    
    // Get position after selection
    const afterBox = await textElement.boundingBox();
    console.log('✅ Position after selection:', afterBox);
    
    // Calculate position difference
    const diffX = Math.abs(afterBox.x - initialBox.x);
    const diffY = Math.abs(afterBox.y - initialBox.y);
    console.log('✅ Position difference - X:', diffX, 'Y:', diffY);
    
    // Determine if jump issue is fixed
    const threshold = 2; // Allow small floating point differences
    if (diffX < threshold && diffY < threshold) {
      console.log('✅ SUCCESS: Jump issue is fixed! Position remains stable.');
    } else {
      console.log('❌ FAIL: Jump issue still exists! Position changed significantly.');
    }
    
    // Take screenshot after selection
    await page.screenshot({ path: 'docs/contest_evidence/screenshots/20_web_playwright_demo.png' });
    console.log('✅ Screenshot taken');
    
    // Write results to file
    const fs = require('fs');
    const results = {
      initialPosition: initialBox,
      afterPosition: afterBox,
      difference: { x: diffX, y: diffY },
      fixed: (diffX < threshold && diffY < threshold),
      timestamp: new Date().toISOString()
    };
    
    fs.writeFileSync(
      'docs/contest_evidence/screenshots/22_web_jump_check.txt',
      JSON.stringify(results, null, 2)
    );
    console.log('✅ Results written to file');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
    
    // Write error to file
    const fs = require('fs');
    fs.writeFileSync(
      'docs/contest_evidence/screenshots/22_web_jump_check.txt',
      `Error: ${error.message}\nStack: ${error.stack}`
    );
  } finally {
    // Close browser
    await browser.close();
  }
})();