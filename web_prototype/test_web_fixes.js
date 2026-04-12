// Test script for web prototype fixes
// Run this in browser console to test core functionality

console.log('=== Web Prototype Fixes Test ===');

// Test 1: Click teleportation fix
console.log('\n1. Testing click teleportation fix...');

// Test 2: Multi-select functionality
console.log('\n2. Testing multi-select functionality...');

// Test 3: Rotation handle visibility
console.log('\n3. Testing rotation handle visibility...');

// Test 4: Font list cleanup
console.log('\n4. Testing font list cleanup...');

// Test 5: Font stack information
console.log('\n5. Testing font stack information...');

// Helper functions for testing
function testClickTeleportation() {
    // Get first text element
    const firstElement = document.querySelector('.text-element');
    if (firstElement) {
        const initialRect = firstElement.getBoundingClientRect();
        console.log('Initial element position:', {
            x: initialRect.left,
            y: initialRect.top,
            width: initialRect.width,
            height: initialRect.height
        });
        
        // Simulate click
        const clickEvent = new MouseEvent('click', {
            bubbles: true,
            cancelable: true,
            clientX: initialRect.left + 10,
            clientY: initialRect.top + 10
        });
        firstElement.dispatchEvent(clickEvent);
        
        const afterClickRect = firstElement.getBoundingClientRect();
        console.log('After click element position:', {
            x: afterClickRect.left,
            y: afterClickRect.top,
            width: afterClickRect.width,
            height: afterClickRect.height
        });
        
        // Check if position changed significantly
        const positionChanged = Math.abs(initialRect.left - afterClickRect.left) > 10 ||
                               Math.abs(initialRect.top - afterClickRect.top) > 10;
        
        console.log('Click teleportation fix:', positionChanged ? 'FAILED - Position changed significantly' : 'PASSED - Position stable');
        return !positionChanged;
    } else {
        console.log('No elements found for click teleportation test');
        return false;
    }
}

function testMultiSelect() {
    // Enable multi-select mode
    const multiSelectCheckbox = document.getElementById('multi-select-checkbox');
    if (multiSelectCheckbox) {
        multiSelectCheckbox.checked = true;
        
        // Get all text elements
        const elements = document.querySelectorAll('.text-element');
        if (elements.length >= 2) {
            // Click first two elements
            const clickEvent1 = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                clientX: elements[0].getBoundingClientRect().left + 10,
                clientY: elements[0].getBoundingClientRect().top + 10
            });
            elements[0].dispatchEvent(clickEvent1);
            
            const clickEvent2 = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                clientX: elements[1].getBoundingClientRect().left + 10,
                clientY: elements[1].getBoundingClientRect().top + 10
            });
            elements[1].dispatchEvent(clickEvent2);
            
            // Check if both are selected
            const selectedElements = model.elements.filter(el => el.selected);
            console.log('Multi-select test:', selectedElements.length >= 2 ? 'PASSED - Multiple elements selected' : 'FAILED - Less than 2 elements selected');
            return selectedElements.length >= 2;
        } else {
            console.log('Not enough elements for multi-select test');
            return false;
        }
    } else {
        console.log('Multi-select checkbox not found');
        return false;
    }
}

function testRotationHandle() {
    // Get first text element
    const firstElement = document.querySelector('.text-element');
    if (firstElement) {
        // Click to select
        const clickEvent = new MouseEvent('click', {
            bubbles: true,
            cancelable: true,
            clientX: firstElement.getBoundingClientRect().left + 10,
            clientY: firstElement.getBoundingClientRect().top + 10
        });
        firstElement.dispatchEvent(clickEvent);
        
        // Check for rotation handle
        const rotationHandle = document.querySelector('.rotate-handle');
        console.log('Rotation handle test:', rotationHandle ? 'PASSED - Rotation handle visible' : 'FAILED - Rotation handle not found');
        return rotationHandle !== null;
    } else {
        console.log('No elements found for rotation handle test');
        return false;
    }
}

function testFontList() {
    // Check Chinese font select
    const chineseFontSelect = document.getElementById('chinese-font-select');
    const englishFontSelect = document.getElementById('english-font-select');
    
    if (chineseFontSelect && englishFontSelect) {
        const chineseOptions = Array.from(chineseFontSelect.options).map(option => option.value);
        const englishOptions = Array.from(englishFontSelect.options).map(option => option.value);
        
        console.log('Chinese font options:', chineseOptions);
        console.log('English font options:', englishOptions);
        
        // Check for unauthorized fonts
        const unauthorizedFonts = ['Microsoft YaHei', 'Arial'];
        const hasUnauthorizedFonts = chineseOptions.some(font => unauthorizedFonts.includes(font)) ||
                                   englishOptions.some(font => unauthorizedFonts.includes(font));
        
        console.log('Font list cleanup test:', hasUnauthorizedFonts ? 'FAILED - Contains unauthorized fonts' : 'PASSED - Only open source fonts');
        return !hasUnauthorizedFonts;
    } else {
        console.log('Font select elements not found');
        return false;
    }
}

function testFontStack() {
    // Check debug info for font stack
    const debugFontStack = document.getElementById('debug-font-stack');
    const debugComputedFont = document.getElementById('debug-computed-font');
    
    if (debugFontStack && debugComputedFont) {
        console.log('Font stack:', debugFontStack.textContent);
        console.log('Computed font:', debugComputedFont.textContent);
        
        const hasFontStack = debugFontStack.textContent.includes('字体栈:');
        const hasComputedFont = debugComputedFont.textContent.includes('计算字体:');
        
        console.log('Font stack information test:', (hasFontStack && hasComputedFont) ? 'PASSED - Font stack information present' : 'FAILED - Font stack information missing');
        return hasFontStack && hasComputedFont;
    } else {
        console.log('Debug font elements not found');
        return false;
    }
}

// Run all tests
console.log('\n=== Running All Tests ===');

const test1Result = testClickTeleportation();
const test2Result = testMultiSelect();
const test3Result = testRotationHandle();
const test4Result = testFontList();
const test5Result = testFontStack();

console.log('\n=== Test Results Summary ===');
console.log('1. Click teleportation fix:', test1Result ? 'PASSED' : 'FAILED');
console.log('2. Multi-select functionality:', test2Result ? 'PASSED' : 'FAILED');
console.log('3. Rotation handle visibility:', test3Result ? 'PASSED' : 'FAILED');
console.log('4. Font list cleanup:', test4Result ? 'PASSED' : 'FAILED');
console.log('5. Font stack information:', test5Result ? 'PASSED' : 'FAILED');

const allTestsPassed = test1Result && test2Result && test3Result && test4Result && test5Result;
console.log('\n=== Overall Result ===');
console.log('All tests passed:', allTestsPassed ? 'YES' : 'NO');

if (allTestsPassed) {
    console.log('🎉 All fixes have been successfully implemented!');
} else {
    console.log('⚠️  Some tests failed. Please review the implementation.');
}
