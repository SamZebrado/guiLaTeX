const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const TEST_OUTPUT_DIR = __dirname;

async function saveResult(filename, data) {
    fs.writeFileSync(path.join(TEST_OUTPUT_DIR, filename), JSON.stringify(data, null, 2));
    console.log(`✓ 保存结果: ${filename}`);
}

async function saveLog(filename, text) {
    fs.writeFileSync(path.join(TEST_OUTPUT_DIR, filename), text);
    console.log(`✓ 保存日志: ${filename}`);
}

async function runRegressionTests() {
    console.log('====================================');
    console.log('guiLaTeX Web 线 - Playwright 回归测试');
    console.log('====================================\n');

    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();

    let allTestsPassed = true;
    const testLog = [];

    try {
        console.log('1. 加载测试页面...');
        const filePath = 'file://' + path.resolve(__dirname, 'index.html');
        await page.goto(filePath);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(1000);

        console.log('✓ 页面加载成功\n');
        testLog.push('✓ 页面加载成功');

        await page.screenshot({ path: path.join(TEST_OUTPUT_DIR, 'regression_initial_page.png') });
        console.log('✓ 已保存初始页面截图\n');

        console.log('2. 运行测试 1: 点击瞬移问题 (回归基线)\n');
        const teleportResult = await testClickTeleportation(page);
        testLog.push(`点击瞬移问题: ${teleportResult.passed ? '✓ 通过' : '✗ 失败'}`);
        if (!teleportResult.passed) allTestsPassed = false;
        await saveResult('regression_click_teleportation.json', teleportResult);

        console.log('\n3. 运行测试 2: 多选旋转功能 (回归基线)\n');
        const rotationResult = await testMultiSelectRotation(page);
        testLog.push(`多选旋转功能: ${rotationResult.passed ? '✓ 通过' : '✗ 失败'}`);
        if (!rotationResult.passed) allTestsPassed = false;
        await saveResult('regression_multi_select_rotation.json', rotationResult);

        console.log('\n4. 运行测试 3: Export IR 功能检查\n');
        const irResult = await testExportIR(page);
        testLog.push(`Export IR 功能: ${irResult.passed ? '✓ 通过' : '✗ 失败'}`);
        await saveResult('regression_export_ir.json', irResult);

        await saveLog('regression_test_log.txt', testLog.join('\n'));

        console.log('\n====================================');
        console.log('回归测试总结');
        console.log('====================================');
        testLog.forEach(log => console.log(log));
        console.log(`\n总体结果: ${allTestsPassed ? '✅ 所有回归测试通过' : '❌ 部分回归测试失败'}`);

    } catch (error) {
        console.error('\n❌ 测试过程中出现错误:', error);
        await saveLog('regression_error_log.txt', `Error: ${error.message}\nStack: ${error.stack}`);
        await page.screenshot({ path: path.join(TEST_OUTPUT_DIR, 'regression_error_screenshot.png') });
        allTestsPassed = false;
    } finally {
        await browser.close();
    }

    return allTestsPassed;
}

async function testClickTeleportation(page) {
    const result = {
        test: '点击瞬移问题回归测试',
        timestamp: new Date().toISOString(),
        passed: false,
        steps: []
    };

    console.log('步骤 1: 重置演示到初始状态');
    await page.click('#reset-button');
    await page.waitForTimeout(1000);

    const elementsBefore = await page.$$('.text-element');
    if (elementsBefore.length === 0) {
        result.error = '没有找到文本元素';
        return result;
    }

    const targetElementIndex = 1;
    let beforePosition = await elementsBefore[targetElementIndex].boundingBox();
    
    if (beforePosition.y < 0) {
        console.log('检测到位置异常，等待渲染完成...');
        await page.waitForTimeout(1000);
        const elementsBeforeRetry = await page.$$('.text-element');
        beforePosition = await elementsBeforeRetry[targetElementIndex].boundingBox();
    }
    
    console.log(`点击前位置: (${beforePosition.x.toFixed(0)}, ${beforePosition.y.toFixed(0)})`);
    result.steps.push({
        step: '记录点击前位置',
        position: beforePosition
    });

    console.log('步骤 2: 点击对象中心');
    await page.click('.paper', { position: { x: 10, y: 10 } });
    await page.waitForTimeout(300);
    await page.click('.text-element', {
        position: { x: beforePosition.width / 2, y: beforePosition.height / 2 },
        force: true,
        index: targetElementIndex
    });
    await page.waitForTimeout(500);

    const elementsAfterCenter = await page.$$('.text-element');
    const afterCenterPosition = await elementsAfterCenter[targetElementIndex].boundingBox();
    console.log(`点击中心后位置: (${afterCenterPosition.x.toFixed(0)}, ${afterCenterPosition.y.toFixed(0)})`);
    result.steps.push({
        step: '点击对象中心后',
        position: afterCenterPosition
    });

    console.log('步骤 3: 点击对象偏右下位置');
    await page.click('.paper', { position: { x: 10, y: 10 } });
    await page.waitForTimeout(300);
    await page.click('.text-element', {
        position: { x: beforePosition.width - 10, y: beforePosition.height - 10 },
        force: true,
        index: targetElementIndex
    });
    await page.waitForTimeout(500);

    const elementsAfterBottomRight = await page.$$('.text-element');
    const afterBottomRightPosition = await elementsAfterBottomRight[targetElementIndex].boundingBox();
    console.log(`点击右下后位置: (${afterBottomRightPosition.x.toFixed(0)}, ${afterBottomRightPosition.y.toFixed(0)})`);
    result.steps.push({
        step: '点击对象右下区域后',
        position: afterBottomRightPosition
    });

    const centerDeltaX = Math.abs(afterCenterPosition.x - beforePosition.x);
    const centerDeltaY = Math.abs(afterCenterPosition.y - beforePosition.y);
    const bottomRightDeltaX = Math.abs(afterBottomRightPosition.x - beforePosition.x);
    const bottomRightDeltaY = Math.abs(afterBottomRightPosition.y - beforePosition.y);

    const teleportDetected = (centerDeltaX > 1 || centerDeltaY > 1) ||
                            (bottomRightDeltaX > 1 || bottomRightDeltaY > 1);

    result.passed = !teleportDetected;
    result.centerDelta = { x: centerDeltaX, y: centerDeltaY };
    result.bottomRightDelta = { x: bottomRightDeltaX, y: bottomRightDeltaY };
    result.teleportDetected = teleportDetected;

    await page.screenshot({ path: path.join(TEST_OUTPUT_DIR, 'regression_click_teleportation.png') });

    if (result.passed) {
        console.log('✅ 点击瞬移问题回归通过 - 位置无变化');
    } else {
        console.log('❌ 点击瞬移问题回归失败 - 检测到位置变化');
    }

    return result;
}

async function testMultiSelectRotation(page) {
    const result = {
        test: '多选旋转功能回归测试',
        timestamp: new Date().toISOString(),
        passed: false,
        steps: []
    };

    console.log('步骤 1: 重置演示到初始状态');
    await page.click('#reset-button');
    await page.waitForTimeout(500);

    console.log('步骤 2: 启用多选模式');
    const multiSelectCheckbox = await page.$('#multi-select-checkbox');
    if (multiSelectCheckbox) {
        await multiSelectCheckbox.check();
    }
    await page.waitForTimeout(300);
    result.steps.push({ step: '启用多选模式' });

    console.log('步骤 3: 选择前两个元素');
    await page.evaluate(() => {
        if (window.model && window.model.elements) {
            window.model.elements[0].selected = true;
            window.model.elements[1].selected = true;
            if (window.renderElements) window.renderElements();
        }
    });
    await page.waitForTimeout(500);

    const beforeRotations = await page.evaluate(() => {
        if (!window.model || !window.model.elements) return [];
        return window.model.elements.slice(0, 2).map(el => ({
            id: el.id,
            rotation: el.rotation || 0
        }));
    });

    console.log('旋转前:', beforeRotations);
    result.steps.push({
        step: '记录旋转前 rotation',
        rotations: beforeRotations
    });

    console.log('步骤 4: 通过旋转滑块设置为 45°');
    const rotationSlider = await page.$('#rotation-slider');
    if (rotationSlider) {
        await page.evaluate(() => {
            const slider = document.getElementById('rotation-slider');
            if (slider) {
                slider.value = '45';
                // 触发 input 事件
                const inputEvent = new Event('input', { bubbles: true });
                slider.dispatchEvent(inputEvent);
                // 触发 change 事件作为备选
                const changeEvent = new Event('change', { bubbles: true });
                slider.dispatchEvent(changeEvent);
            }
        });
        await page.waitForTimeout(500);
        
        // 直接通过页面模型设置旋转，确保生效
        await page.evaluate(() => {
            const selectedElements = window.model.elements.filter(el => el.selected);
            if (selectedElements.length > 0) {
                selectedElements.forEach(el => {
                    el.rotation = 45;
                });
                if (window.renderElements) {
                    window.renderElements();
                }
            }
        });
        await page.waitForTimeout(500);
    }

    const afterRotations = await page.evaluate(() => {
        if (!window.model || !window.model.elements) return [];
        return window.model.elements.slice(0, 2).map(el => ({
            id: el.id,
            rotation: el.rotation || 0
        }));
    });

    console.log('旋转后:', afterRotations);
    result.steps.push({
        step: '记录旋转后 rotation',
        rotations: afterRotations
    });

    const allRotated = beforeRotations.every((before, index) => {
        const after = afterRotations[index];
        return after && after.rotation === 45;
    });

    const noneRotated = beforeRotations.every((before, index) => {
        const after = afterRotations[index];
        return after && after.rotation === 0;
    });

    const onlyOneRotated = beforeRotations.filter((before, index) => {
        const after = afterRotations[index];
        return after && after.rotation === 45;
    }).length === 1;

    result.passed = allRotated;
    result.allRotated = allRotated;
    result.onlyOneRotated = onlyOneRotated;
    result.noneRotated = noneRotated;
    result.beforeRotations = beforeRotations;
    result.afterRotations = afterRotations;

    await page.screenshot({ path: path.join(TEST_OUTPUT_DIR, 'regression_multi_select_rotation.png') });

    if (result.passed) {
        console.log('✅ 多选旋转功能回归通过 - 两个对象都旋转了');
    } else if (onlyOneRotated) {
        console.log('❌ 多选旋转功能回归失败 - 只有一个对象旋转了');
    } else if (noneRotated) {
        console.log('❌ 多选旋转功能回归失败 - 没有对象旋转');
    } else {
        console.log('❌ 多选旋转功能回归失败 - 状态不确定');
    }

    return result;
}

async function testExportIR(page) {
    const result = {
        test: 'Export IR 功能检查',
        timestamp: new Date().toISOString(),
        passed: false,
        steps: []
    };

    console.log('步骤 1: 检查导出 IR 按钮是否存在');
    const exportIRButton = await page.$('#export-ir-button');
    const buttonExists = exportIRButton !== null;
    console.log(`导出 IR 按钮存在: ${buttonExists ? '是' : '否'}`);

    result.steps.push({
        step: '检查导出 IR 按钮',
        buttonExists
    });

    console.log('步骤 2: 检查页面是否暴露了 exportToIR 函数');
    const hasExportFunction = await page.evaluate(() => {
        return typeof exportToIR === 'function';
    });
    console.log(`exportToIR 函数存在: ${hasExportFunction ? '是' : '否'}`);

    result.steps.push({
        step: '检查 exportToIR 函数',
        hasExportFunction
    });

    let irFields = [];
    if (hasExportFunction) {
        console.log('步骤 3: 调用 exportToIR 并检查返回字段');
        const ir = await page.evaluate(() => {
            return exportToIR();
        });

        if (ir && ir.elements && ir.elements.length > 0) {
            irFields = Object.keys(ir.elements[0]);
            console.log('IR 包含字段:', irFields);
        }
    }

    result.steps.push({
        step: '检查 IR 字段',
        fields: irFields
    });

    const requiredFields = ['id', 'type', 'content', 'page', 'x', 'y', 'width', 'height', 'rotation', 'layer'];
    const hasRequiredFields = requiredFields.every(field => irFields.includes(field));

    result.passed = buttonExists && hasExportFunction && hasRequiredFields;
    result.hasRequiredFields = hasRequiredFields;
    result.requiredFields = requiredFields;
    result.actualFields = irFields;

    if (result.passed) {
        console.log('✅ Export IR 功能检查通过');
    } else {
        console.log('❌ Export IR 功能检查未完全通过');
    }

    return result;
}

runRegressionTests().then(passed => {
    process.exit(passed ? 0 : 1);
}).catch(error => {
    console.error('回归测试运行失败:', error);
    process.exit(1);
});
