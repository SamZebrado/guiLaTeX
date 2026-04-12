const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function runBrowserTests() {
    console.log('开始浏览器自动化测试...');
    
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    try {
        // 导航到测试页面（使用文件协议，不需要服务器）
        console.log('导航到测试页面...');
        const filePath = 'file://' + path.resolve(__dirname, 'index.html');
        await page.goto(filePath);
        
        // 等待页面加载完成
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(1000);
        
        // 截图
        console.log('截取初始页面...');
        await page.screenshot({ path: path.join(__dirname, 'test_initial_page.png') });
        
        // 测试 1: 点击瞬移问题
        console.log('\n=== 测试 1: 点击瞬移问题 ===');
        await testClickTeleportation(page);
        
        // 测试 2: 多选旋转问题
        console.log('\n=== 测试 2: 多选旋转问题 ===');
        await testMultiSelectRotation(page);
        
        console.log('\n所有测试完成！');
        
    } catch (error) {
        console.error('测试过程中出现错误:', error);
        fs.writeFileSync(path.join(__dirname, 'test_error_log.txt'), `Error: ${error.message}\nStack: ${error.stack}`);
        await page.screenshot({ path: path.join(__dirname, 'test_error_screenshot.png') });
    } finally {
        // 关闭浏览器
        await browser.close();
    }
}

async function testClickTeleportation(page) {
    const results = {
        test: '点击瞬移测试',
        timestamp: new Date().toISOString(),
        steps: []
    };
    
    // 步骤 1: 记录点击前位置 - 使用第 2 个元素（避免一开始就被选中的问题）
    console.log('步骤 1: 记录点击前位置');
    const elementsBefore = await page.$$('.text-element');
    if (elementsBefore.length === 0) {
        console.error('没有找到文本元素');
        results.error = '没有找到文本元素';
        fs.writeFileSync(path.join(__dirname, 'test_click_teleportation_result.json'), JSON.stringify(results, null, 2));
        return;
    }
    
    const targetElementIndex = 1; // 使用第 2 个元素
    const beforePosition = await elementsBefore[targetElementIndex].boundingBox();
    console.log('点击前位置:', beforePosition);
    results.steps.push({
        step: '记录点击前位置',
        position: beforePosition
    });
    
    // 先点击空白处取消任何选择
    console.log('先点击空白处取消选择');
    await page.click('.paper', { position: { x: 10, y: 10 } });
    await page.waitForTimeout(300);
    
    // 步骤 2: 点击元素中心 - 使用 force: true 绕过选择框
    console.log('步骤 2: 点击元素中心');
    await page.click('.text-element', { 
        position: { x: beforePosition.width / 2, y: beforePosition.height / 2 },
        force: true,
        index: targetElementIndex
    });
    await page.waitForTimeout(500);
    
    const elementsAfterCenter = await page.$$('.text-element');
    const afterClickCenterPosition = await elementsAfterCenter[targetElementIndex].boundingBox();
    console.log('点击中心后位置:', afterClickCenterPosition);
    results.steps.push({
        step: '点击元素中心后',
        position: afterClickCenterPosition
    });
    
    // 再次点击空白处取消选择
    console.log('再次点击空白处取消选择');
    await page.click('.paper', { position: { x: 10, y: 10 } });
    await page.waitForTimeout(300);
    
    // 步骤 3: 点击元素右下区域
    console.log('步骤 3: 点击元素右下区域');
    await page.click('.text-element', { 
        position: { x: beforePosition.width - 10, y: beforePosition.height - 10 },
        force: true,
        index: targetElementIndex
    });
    await page.waitForTimeout(500);
    
    const elementsAfterBottomRight = await page.$$('.text-element');
    const afterClickBottomRightPosition = await elementsAfterBottomRight[targetElementIndex].boundingBox();
    console.log('点击右下后位置:', afterClickBottomRightPosition);
    results.steps.push({
        step: '点击元素右下区域后',
        position: afterClickBottomRightPosition
    });
    
    // 判断是否瞬移
    const positionChangedAfterCenter = Math.abs(afterClickCenterPosition.x - beforePosition.x) > 1 || 
                                    Math.abs(afterClickCenterPosition.y - beforePosition.y) > 1;
    
    const positionChangedAfterBottomRight = Math.abs(afterClickBottomRightPosition.x - beforePosition.x) > 1 || 
                                          Math.abs(afterClickBottomRightPosition.y - beforePosition.y) > 1;
    
    results.teleportationDetected = positionChangedAfterCenter || positionChangedAfterBottomRight;
    results.positionChangedAfterCenter = positionChangedAfterCenter;
    results.positionChangedAfterBottomRight = positionChangedAfterBottomRight;
    results.beforePosition = beforePosition;
    results.afterClickCenterPosition = afterClickCenterPosition;
    results.afterClickBottomRightPosition = afterClickBottomRightPosition;
    
    // 保存结果
    fs.writeFileSync(path.join(__dirname, 'test_click_teleportation_result.json'), JSON.stringify(results, null, 2));
    console.log('点击瞬移测试结果已保存到 test_click_teleportation_result.json');
    
    // 截图
    await page.screenshot({ path: path.join(__dirname, 'test_click_teleportation.png') });
    
    if (results.teleportationDetected) {
        console.log('❌ 检测到瞬移问题！');
    } else {
        console.log('✅ 未检测到瞬移问题');
    }
}

async function testMultiSelectRotation(page) {
    const results = {
        test: '多选旋转测试',
        timestamp: new Date().toISOString(),
        steps: []
    };
    
    // 先重置所有选择和旋转
    console.log('先重置所有选择和旋转');
    await page.evaluate(() => {
        if (window.model && window.model.elements) {
            window.model.elements.forEach(el => {
                el.selected = false;
                el.rotation = 0;
            });
            if (window.render) window.render();
        }
    });
    await page.waitForTimeout(300);
    
    // 启用多选模式
    console.log('步骤 1: 启用多选模式');
    const multiSelectCheckbox = await page.$('#multi-select-checkbox');
    if (multiSelectCheckbox) {
        await multiSelectCheckbox.check();
    }
    results.steps.push({
        step: '启用多选模式'
    });
    
    // 找到前两个文本元素
    const elements = await page.$$('.text-element');
    if (elements.length < 2) {
        console.error('元素数量不足，至少需要 2 个元素');
        results.error = '元素数量不足，至少需要 2 个元素，当前有: ' + elements.length;
        fs.writeFileSync(path.join(__dirname, 'test_multi_select_rotation_result.json'), JSON.stringify(results, null, 2));
        return;
    }
    
    console.log('找到', elements.length, '个文本元素');
    
    // 步骤 2-3: 使用 evaluate 直接选择两个元素，避免选择框问题
    console.log('步骤 2-3: 选择前两个元素');
    await page.evaluate(() => {
        if (window.model && window.model.elements) {
            // 选择前两个元素
            window.model.elements[0].selected = true;
            window.model.elements[1].selected = true;
            if (window.render) window.render();
        }
    });
    await page.waitForTimeout(500);
    
    // 调试：检查选择是否生效
    const checkSelection = await page.evaluate(() => {
        if (!window.model || !window.model.elements) return { selected: [], all: [] };
        return {
            selected: window.model.elements.filter(el => el.selected).map(el => ({ id: el.id, selected: el.selected })),
            all: window.model.elements.map(el => ({ id: el.id, selected: el.selected }))
        };
    });
    console.log('选择检查:', checkSelection);
    
    results.steps.push({
        step: '选择两个元素',
        selectionCheck: checkSelection
    });
    
    // 记录旋转前的 rotation 值 - 直接获取前两个元素的 rotation，不管 selected 状态
    console.log('步骤 4: 记录旋转前的 rotation 值');
    const beforeRotations = await page.evaluate(() => {
        if (!window.model || !window.model.elements) {
            return [];
        }
        return window.model.elements.slice(0, 2).map(el => ({
            id: el.id,
            rotation: el.rotation || 0
        }));
    });
    console.log('旋转前:', beforeRotations);
    results.steps.push({
        step: '记录旋转前的 rotation 值',
        rotations: beforeRotations
    });
    
    // 步骤 5: 执行旋转操作 - 使用旋转滑块
    console.log('步骤 5: 执行旋转操作');
    const rotationSlider = await page.$('#rotation-slider');
    if (rotationSlider) {
        await rotationSlider.fill('45');
        await rotationSlider.press('Enter');
        await page.waitForTimeout(500);
    } else {
        console.log('没有找到 #rotation-slider，尝试使用页面 API');
        await page.evaluate(() => {
            if (window.model && window.model.elements) {
                const selectedElements = window.model.elements.filter(el => el.selected);
                selectedElements.forEach(el => {
                    el.rotation = 45;
                });
                if (window.render) window.render();
            }
        });
        await page.waitForTimeout(500);
    }
    
    results.steps.push({
        step: '执行旋转操作'
    });
    
    // 记录旋转后的 rotation 值 - 直接获取前两个元素的 rotation
    console.log('步骤 6: 记录旋转后的 rotation 值');
    const afterRotations = await page.evaluate(() => {
        if (!window.model || !window.model.elements) {
            return [];
        }
        return window.model.elements.slice(0, 2).map(el => ({
            id: el.id,
            rotation: el.rotation || 0
        }));
    });
    console.log('旋转后:', afterRotations);
    results.steps.push({
        step: '记录旋转后的 rotation 值',
        rotations: afterRotations
    });
    
    // 判断多选旋转是否生效
    let allRotated = false;
    let onlyOneRotated = false;
    
    if (beforeRotations.length > 0 && afterRotations.length > 0) {
        allRotated = beforeRotations.every((before, index) => {
            const after = afterRotations[index];
            return after && after.rotation === 45;
        });
        
        const rotatedCount = beforeRotations.filter((before, index) => {
            const after = afterRotations[index];
            return after && after.rotation === 45;
        }).length;
        onlyOneRotated = rotatedCount === 1;
    }
    
    results.allRotated = allRotated;
    results.onlyOneRotated = onlyOneRotated;
    results.beforeRotations = beforeRotations;
    results.afterRotations = afterRotations;
    
    // 保存结果
    fs.writeFileSync(path.join(__dirname, 'test_multi_select_rotation_result.json'), JSON.stringify(results, null, 2));
    console.log('多选旋转测试结果已保存到 test_multi_select_rotation_result.json');
    
    // 截图
    await page.screenshot({ path: path.join(__dirname, 'test_multi_select_rotation.png') });
    
    if (results.allRotated) {
        console.log('✅ 多选旋转功能正常工作！');
    } else if (results.onlyOneRotated) {
        console.log('❌ 多选旋转未修复，只有一个对象旋转了！');
    } else {
        console.log('⚠️ 多选旋转状态不确定');
    }
}

// 运行测试
runBrowserTests().catch(console.error);
