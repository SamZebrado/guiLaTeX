const { chromium } = require('playwright');

async function runBrowserTests() {
    console.log('开始浏览器自动化测试...');
    
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    try {
        // 导航到测试页面
        await page.goto('http://localhost:8007/web_prototype/index.html');
        
        // 等待页面加载完成
        await page.waitForLoadState('networkidle');
        
        // 测试 1: 点击瞬移问题
        console.log('\n测试 1: 点击瞬移问题');
        await testClickTeleportation(page);
        
        // 测试 2: 多选旋转功能
        console.log('\n测试 2: 多选旋转功能');
        await testMultiSelectRotation(page);
        
        console.log('\n所有测试完成！');
        
    } catch (error) {
        console.error('测试过程中出现错误:', error);
    } finally {
        // 关闭浏览器
        await browser.close();
    }
}

async function testClickTeleportation(page) {
    // 获取第一个元素
    const elements = await page.$$('.text-element');
    if (elements.length === 0) {
        console.error('没有找到文本元素');
        return;
    }
    
    const firstElement = elements[0];
    
    // 记录点击前位置
    const beforePosition = await firstElement.boundingBox();
    console.log('点击前位置:', beforePosition);
    
    // 点击元素中心
    await firstElement.click({ position: { x: beforePosition.width / 2, y: beforePosition.height / 2 } });
    
    // 等待一下
    await page.waitForTimeout(500);
    
    // 记录点击后位置
    const afterClickCenterPosition = await firstElement.boundingBox();
    console.log('点击中心后位置:', afterClickCenterPosition);
    
    // 点击元素右下区域
    await firstElement.click({ position: { x: beforePosition.width - 10, y: beforePosition.height - 10 } });
    
    // 等待一下
    await page.waitForTimeout(500);
    
    // 记录点击后位置
    const afterClickBottomRightPosition = await firstElement.boundingBox();
    console.log('点击右下后位置:', afterClickBottomRightPosition);
    
    // 计算位置变化
    const positionChangedAfterCenter = Math.abs(afterClickCenterPosition.x - beforePosition.x) > 1 || 
                                    Math.abs(afterClickCenterPosition.y - beforePosition.y) > 1;
    
    const positionChangedAfterBottomRight = Math.abs(afterClickBottomRightPosition.x - beforePosition.x) > 1 || 
                                          Math.abs(afterClickBottomRightPosition.y - beforePosition.y) > 1;
    
    console.log('点击中心后位置是否变化:', positionChangedAfterCenter);
    console.log('点击右下后位置是否变化:', positionChangedAfterBottomRight);
    
    // 保存测试结果
    const clickTestResult = {
        test: '点击瞬移测试',
        beforePosition: beforePosition,
        afterClickCenterPosition: afterClickCenterPosition,
        afterClickBottomRightPosition: afterClickBottomRightPosition,
        positionChangedAfterCenter: positionChangedAfterCenter,
        positionChangedAfterBottomRight: positionChangedAfterBottomRight,
        passed: !positionChangedAfterCenter && !positionChangedAfterBottomRight
    };
    
    // 保存结果到文件
    const fs = require('fs');
    fs.writeFileSync('test_click_teleportation_result.json', JSON.stringify(clickTestResult, null, 2));
    console.log('点击瞬移测试结果已保存到 test_click_teleportation_result.json');
    
    // 截图
    await page.screenshot({ path: 'test_click_teleportation_screenshot.png' });
    console.log('点击瞬移测试截图已保存到 test_click_teleportation_screenshot.png');
}

async function testMultiSelectRotation(page) {
    // 启用多选模式
    await page.check('#multi-select-checkbox');
    
    // 获取前两个元素
    const elements = await page.$$('.text-element');
    if (elements.length < 2) {
        console.error('元素数量不足，至少需要 2 个元素');
        return;
    }
    
    const element1 = elements[0];
    const element2 = elements[1];
    
    // 点击选择第一个元素
    await element1.click();
    
    // 等待一下
    await page.waitForTimeout(300);
    
    // 点击选择第二个元素
    await element2.click();
    
    // 等待一下
    await page.waitForTimeout(300);
    
    // 记录旋转前角度
    const rotationSliderBefore = await page.inputValue('#rotation-slider');
    console.log('旋转前角度:', rotationSliderBefore);
    
    // 调整旋转角度
    await page.fill('#rotation-slider', '45');
    await page.press('#rotation-slider', 'Enter');
    
    // 等待一下
    await page.waitForTimeout(500);
    
    // 记录旋转后角度
    const rotationSliderAfter = await page.inputValue('#rotation-slider');
    console.log('旋转后角度:', rotationSliderAfter);
    
    // 保存测试结果
    const rotationTestResult = {
        test: '多选旋转测试',
        rotationBefore: rotationSliderBefore,
        rotationAfter: rotationSliderAfter,
        rotationChanged: rotationSliderAfter !== rotationSliderBefore,
        passed: rotationSliderAfter === '45'
    };
    
    // 保存结果到文件
    const fs = require('fs');
    fs.writeFileSync('test_multi_select_rotation_result.json', JSON.stringify(rotationTestResult, null, 2));
    console.log('多选旋转测试结果已保存到 test_multi_select_rotation_result.json');
    
    // 截图
    await page.screenshot({ path: 'test_multi_select_rotation_screenshot.png' });
    console.log('多选旋转测试截图已保存到 test_multi_select_rotation_screenshot.png');
}

// 运行测试
runBrowserTests();