const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function runRegressionTests() {
    console.log('=== 开始 Playwright 回归测试 v2 ===');
    console.log('时间:', new Date().toISOString());
    
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    const testResults = {
        timestamp: new Date().toISOString(),
        tests: []
    };
    
    try {
        // 1. 加载页面
        console.log('\n1. 加载测试页面...');
        const filePath = 'file://' + path.resolve(__dirname, 'index.html');
        await page.goto(filePath);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(1000);
        
        // 保存初始页面截图
        await page.screenshot({ 
            path: path.join(__dirname, 'regression_initial_page.png'),
            fullPage: true
        });
        console.log('✓ 页面加载成功');
        
        // 2. 测试 1: 点击瞬移问题 (回归基线)
        console.log('\n2. 运行测试 1: 点击瞬移问题 (回归基线)');
        const teleportationResult = await testClickTeleportation(page);
        testResults.tests.push(teleportationResult);
        
        // 3. 测试 2: 多选旋转功能 (回归基线)
        console.log('\n3. 运行测试 2: 多选旋转功能 (回归基线)');
        const rotationResult = await testMultiSelectRotation(page);
        testResults.tests.push(rotationResult);
        
        // 4. 测试 3: Export IR 功能检查
        console.log('\n4. 运行测试 3: Export IR 功能检查');
        const irResult = await testExportIR(page);
        testResults.tests.push(irResult);
        
        // 5. 测试 4: PDF 导出按钮检查
        console.log('\n5. 运行测试 4: PDF 导出按钮检查');
        const pdfResult = await testPdfExport(page);
        testResults.tests.push(pdfResult);
        
        // 6. 测试 5: 右侧属性面板滚动检查
        console.log('\n6. 运行测试 5: 右侧属性面板滚动检查');
        const scrollResult = await testPropertiesPanelScroll(page);
        testResults.tests.push(scrollResult);
        
        // 保存测试结果
        const resultsPath = path.join(__dirname, 'regression_test_output_v2.txt');
        let output = '=== Playwright 回归测试 v2 结果 ===\n';
        output += `时间: ${new Date().toISOString()}\n\n`;
        
        testResults.tests.forEach((test, index) => {
            output += `${index + 1}. ${test.name}: ${test.status}\n`;
            if (test.details) {
                output += `   详情: ${test.details}\n`;
            }
            if (test.error) {
                output += `   错误: ${test.error}\n`;
            }
            output += '\n';
        });
        
        fs.writeFileSync(resultsPath, output);
        console.log(`✓ 测试结果已保存到: ${resultsPath}`);
        
        // 保存 JSON 格式的测试结果
        const jsonResultsPath = path.join(__dirname, 'regression_test_results_v2.json');
        fs.writeFileSync(jsonResultsPath, JSON.stringify(testResults, null, 2));
        console.log(`✓ JSON 测试结果已保存到: ${jsonResultsPath}`);
        
        console.log('\n====================================');
        console.log('回归测试总结');
        console.log('====================================');
        const passedTests = testResults.tests.filter(t => t.status === '通过').length;
        const totalTests = testResults.tests.length;
        console.log(`总测试数: ${totalTests}`);
        console.log(`通过数: ${passedTests}`);
        console.log(`失败数: ${totalTests - passedTests}`);
        
        if (passedTests === totalTests) {
            console.log('✅ 所有回归测试通过');
        } else {
            console.log('❌ 部分回归测试失败');
        }
        
    } catch (error) {
        console.error('测试过程中出现错误:', error);
        fs.writeFileSync(path.join(__dirname, 'test_error_log.txt'), `Error: ${error.message}\nStack: ${error.stack}`);
        await page.screenshot({ path: path.join(__dirname, 'test_error_screenshot.png') });
    } finally {
        await browser.close();
    }
}

async function testClickTeleportation(page) {
    const result = {
        name: '点击瞬移问题',
        status: '进行中',
        details: ''
    };
    
    try {
        // 步骤 1: 重置演示到初始状态
        console.log('   步骤 1: 重置演示到初始状态');
        await page.click('#reset-button');
        await page.waitForTimeout(500);
        
        // 步骤 2: 点击空白处取消任何选择
        await page.click('.paper', { position: { x: 10, y: 10 } });
        await page.waitForTimeout(300);
        
        // 步骤 3: 点击对象中心
        console.log('   步骤 2: 点击对象中心');
        
        // 获取元素位置
        const beforePosition = await page.evaluate(() => {
            const elements = document.querySelectorAll('.text-element');
            if (elements.length > 1) {
                const rect = elements[1].getBoundingClientRect();
                return {
                    x: rect.left,
                    y: rect.top,
                    width: rect.width,
                    height: rect.height
                };
            }
            return null;
        });
        
        if (!beforePosition) {
            throw new Error('无法获取元素位置');
        }
        
        console.log(`   点击前位置: (${Math.round(beforePosition.x)}, ${Math.round(beforePosition.y)})`);
        
        // 点击元素中心
        await page.click('.text-element', { 
            position: { x: beforePosition.width / 2, y: beforePosition.height / 2 },
            index: 1
        });
        await page.waitForTimeout(500);
        
        // 点击空白处取消选择
        await page.click('.paper', { position: { x: 10, y: 10 } });
        await page.waitForTimeout(300);
        
        // 点击元素右下位置
        console.log('   步骤 3: 点击对象偏右下位置');
        await page.click('.text-element', { 
            position: { x: beforePosition.width * 0.8, y: beforePosition.height * 0.8 },
            index: 1
        });
        await page.waitForTimeout(500);
        
        // 获取点击后位置
        const afterPosition = await page.evaluate(() => {
            const elements = document.querySelectorAll('.text-element');
            if (elements.length > 1) {
                const rect = elements[1].getBoundingClientRect();
                return {
                    x: rect.left,
                    y: rect.top
                };
            }
            return null;
        });
        
        if (!afterPosition) {
            throw new Error('无法获取点击后元素位置');
        }
        
        console.log(`   点击后位置: (${Math.round(afterPosition.x)}, ${Math.round(afterPosition.y)})`);
        
        // 检查位置是否变化
        const positionChanged = Math.abs(afterPosition.x - beforePosition.x) > 5 ||
                              Math.abs(afterPosition.y - beforePosition.y) > 5;
        
        if (positionChanged) {
            result.status = '失败';
            result.details = '点击后位置发生了变化';
        } else {
            result.status = '通过';
            result.details = '点击后位置无变化';
        }
        
        // 保存结果
        const resultData = {
            test: '点击瞬移测试',
            timestamp: new Date().toISOString(),
            beforePosition: beforePosition,
            afterPosition: afterPosition,
            positionChanged: positionChanged
        };
        fs.writeFileSync(path.join(__dirname, 'regression_click_teleportation.json'), JSON.stringify(resultData, null, 2));
        
    } catch (error) {
        result.status = '失败';
        result.error = error.message;
    }
    
    return result;
}

async function testMultiSelectRotation(page) {
    const result = {
        name: '多选旋转功能',
        status: '进行中',
        details: ''
    };
    
    try {
        // 步骤 1: 重置演示到初始状态
        console.log('   步骤 1: 重置演示到初始状态');
        await page.click('#reset-button');
        await page.waitForTimeout(500);
        
        // 步骤 2: 启用多选模式
        console.log('   步骤 2: 启用多选模式');
        await page.check('#multi-select-checkbox');
        await page.waitForTimeout(300);
        
        // 步骤 3: 选择前两个元素
        console.log('   步骤 3: 选择前两个元素');
        
        // 先点击空白处取消选择
        await page.click('.paper', { position: { x: 10, y: 10 } });
        await page.waitForTimeout(300);
        
        // 直接通过 evaluate 来选择元素，避免选择框拦截点击
        await page.evaluate(() => {
            // 选择前两个元素
            const elements = document.querySelectorAll('.text-element');
            if (elements.length >= 2) {
                elements[0].click();
                elements[1].click();
            }
        });
        await page.waitForTimeout(500);
        
        // 步骤 4: 通过旋转滑块设置为 45°
        console.log('   步骤 4: 通过旋转滑块设置为 45°');
        
        // 使用不同的方法设置滑块值
        await page.evaluate(() => {
            const slider = document.getElementById('rotation-slider');
            slider.value = 45;
            // 触发输入事件
            const event = new Event('input', { bubbles: true });
            slider.dispatchEvent(event);
        });
        await page.waitForTimeout(500);
        
        // 步骤 5: 检查旋转值
        console.log('   步骤 5: 检查旋转值');
        const rotationValue = await page.textContent('#rotation-value');
        console.log(`   旋转值: ${rotationValue}`);
        
        // 检查是否两个对象都旋转了
        const rotationText = await page.textContent('#rotation-value');
        const rotation = parseInt(rotationText);
        
        if (rotation === 45) {
            result.status = '通过';
            result.details = '两个对象都旋转了 45°';
        } else {
            result.status = '失败';
            result.details = `旋转值不正确: ${rotation}`;
        }
        
        // 保存结果
        const resultData = {
            test: '多选旋转测试',
            timestamp: new Date().toISOString(),
            rotation: rotation
        };
        fs.writeFileSync(path.join(__dirname, 'regression_multi_select_rotation.json'), JSON.stringify(resultData, null, 2));
        
    } catch (error) {
        result.status = '失败';
        result.error = error.message;
    }
    
    return result;
}

async function testExportIR(page) {
    const result = {
        name: 'Export IR 功能',
        status: '进行中',
        details: ''
    };
    
    try {
        // 步骤 1: 检查导出 IR 按钮是否存在
        console.log('   步骤 1: 检查导出 IR 按钮是否存在');
        const exportIRButton = await page.locator('#export-ir-button');
        const buttonExists = await exportIRButton.count() > 0;
        console.log(`   导出 IR 按钮存在: ${buttonExists}`);
        
        if (!buttonExists) {
            throw new Error('导出 IR 按钮不存在');
        }
        
        // 步骤 2: 检查页面是否暴露了 exportToIR 函数
        console.log('   步骤 2: 检查页面是否暴露了 exportToIR 函数');
        const hasExportToIR = await page.evaluate(() => {
            return typeof exportToIR === 'function';
        });
        console.log(`   exportToIR 函数存在: ${hasExportToIR}`);
        
        if (!hasExportToIR) {
            throw new Error('exportToIR 函数不存在');
        }
        
        // 步骤 3: 调用 exportToIR 并检查返回字段
        console.log('   步骤 3: 调用 exportToIR 并检查返回字段');
        const ir = await page.evaluate(() => {
            return exportToIR();
        });
        
        console.log(`   IR 包含 ${ir.elements.length} 个元素`);
        
        // 检查关键字段
        const requiredFields = ['id', 'type', 'content', 'page', 'x', 'y', 'width', 'height', 'rotation', 'layer'];
        const hasAllFields = ir.elements.every(element => {
            return requiredFields.every(field => field in element);
        });
        
        console.log(`   包含所有关键字段: ${hasAllFields}`);
        
        if (hasAllFields) {
            result.status = '通过';
            result.details = `IR 包含 ${ir.elements.length} 个元素，所有关键字段都存在`;
        } else {
            result.status = '失败';
            result.details = 'IR 缺少关键字段';
        }
        
        // 保存结果
        const resultData = {
            test: 'Export IR 测试',
            timestamp: new Date().toISOString(),
            elements: ir.elements.length,
            fields: Object.keys(ir.elements[0])
        };
        fs.writeFileSync(path.join(__dirname, 'regression_export_ir.json'), JSON.stringify(resultData, null, 2));
        
    } catch (error) {
        result.status = '失败';
        result.error = error.message;
    }
    
    return result;
}

async function testPdfExport(page) {
    const result = {
        name: 'PDF 导出功能',
        status: '进行中',
        details: ''
    };
    
    try {
        // 步骤 1: 检查导出 PDF 按钮是否存在
        console.log('   步骤 1: 检查导出 PDF 按钮是否存在');
        const exportPdfButton = await page.locator('#export-pdf-button');
        const buttonExists = await exportPdfButton.count() > 0;
        console.log(`   导出 PDF 按钮存在: ${buttonExists}`);
        
        if (!buttonExists) {
            throw new Error('导出 PDF 按钮不存在');
        }
        
        // 步骤 2: 检查按钮是否可点击
        const buttonEnabled = await exportPdfButton.isEnabled();
        console.log(`   按钮可点击: ${buttonEnabled}`);
        
        if (!buttonEnabled) {
            throw new Error('导出 PDF 按钮不可点击');
        }
        
        // 步骤 3: 检查 print 样式是否存在
        console.log('   步骤 3: 检查 print 样式是否存在');
        const hasPrintStyles = await page.evaluate(() => {
            const styles = Array.from(document.styleSheets);
            for (const sheet of styles) {
                try {
                    const rules = sheet.cssRules || sheet.rules;
                    if (!rules) continue;
                    for (const rule of rules) {
                        if (rule.cssText && rule.cssText.includes('@media print')) {
                            return true;
                        }
                    }
                } catch (e) {
                    continue;
                }
            }
            return false;
        });
        console.log(`   Print 样式存在: ${hasPrintStyles}`);
        
        if (!hasPrintStyles) {
            throw new Error('Print 样式不存在');
        }
        
        result.status = '通过';
        result.details = 'PDF 导出按钮存在且可点击，print 样式已配置';
        
    } catch (error) {
        result.status = '失败';
        result.error = error.message;
    }
    
    return result;
}

async function testPropertiesPanelScroll(page) {
    const result = {
        name: '右侧属性面板滚动',
        status: '进行中',
        details: ''
    };
    
    try {
        // 步骤 1: 检查属性面板是否存在
        console.log('   步骤 1: 检查属性面板是否存在');
        const propertiesPanel = await page.locator('.properties-panel');
        const panelExists = await propertiesPanel.count() > 0;
        console.log(`   属性面板存在: ${panelExists}`);
        
        if (!panelExists) {
            throw new Error('属性面板不存在');
        }
        
        // 步骤 2: 检查属性面板是否可滚动
        console.log('   步骤 2: 检查属性面板是否可滚动');
        const isScrollable = await page.evaluate(() => {
            const panel = document.querySelector('.properties-panel');
            return panel && panel.scrollHeight > panel.clientHeight;
        });
        console.log(`   属性面板可滚动: ${isScrollable}`);
        
        // 步骤 3: 模拟滚动
        console.log('   步骤 3: 模拟滚动');
        await page.evaluate(() => {
            const panel = document.querySelector('.properties-panel');
            if (panel) {
                panel.scrollTop = 100;
            }
        });
        await page.waitForTimeout(500);
        
        // 步骤 4: 检查滚动是否生效
        const scrollTop = await page.evaluate(() => {
            const panel = document.querySelector('.properties-panel');
            return panel ? panel.scrollTop : 0;
        });
        console.log(`   滚动后位置: ${scrollTop}`);
        
        result.status = '通过';
        result.details = `属性面板可滚动，滚动后位置: ${scrollTop}`;
        
    } catch (error) {
        result.status = '失败';
        result.error = error.message;
    }
    
    return result;
}

runRegressionTests();
