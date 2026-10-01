// Run against the documented local server. Requires the existing Playwright runtime.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const url = process.env.GUILATEX_TEST_URL || 'http://127.0.0.1:8777/';
const key = 'guilatex.web.draft.v1';

(async () => {
    const browser = await chromium.launch({ headless: true, channel: 'chrome' });
    const checks = [];
    const check = name => { checks.push(name); console.log(`PASS ${name}`); };
    try {
        const context = await browser.newContext({ acceptDownloads: true });
        const page = await context.newPage();
        await page.goto(url);
        const status = () => page.evaluate(() => getDraftStatus());
        const snapshot = () => page.evaluate(() => JSON.parse(JSON.stringify(model)));
        const unloadBlocked = () => page.evaluate(() => {
            const event = new Event('beforeunload', { cancelable: true });
            window.dispatchEvent(event);
            return event.defaultPrevented;
        });
        assert.equal((await status()).dirty, false);
        assert.equal((await status()).recovery_pending, false);
        assert.equal(await unloadBlocked(), false);
        check('initial clean, no draft, no unload warning');
        // Selection is UI-only and must not mark an otherwise clean document dirty.
        await page.locator('.text-element').first().click();
        assert.equal((await status()).dirty, false);
        await page.click('#insert-equation-button');
        assert.equal((await status()).dirty, true);
        assert.equal(await unloadBlocked(), true);
        assert(await page.evaluate(key => localStorage.getItem(key), key));
        check('selection clean; equation edit dirty + full draft + unload protection');
        await page.click('#undo-button');
        assert.equal((await status()).dirty, false);
        assert.equal(await unloadBlocked(), false);
        await page.click('#redo-button');
        assert.equal((await status()).dirty, true);
        check('undo to checkpoint clean; redo dirty');
        const downloadEvent = page.waitForEvent('download');
        await page.click('#save-button');
        const download = await downloadEvent;
        const saved = JSON.parse(fs.readFileSync(await download.path(), 'utf8'));
        assert.deepEqual(saved, await snapshot());
        assert.equal((await status()).dirty, false);
        assert.equal(await page.evaluate(key => localStorage.getItem(key), key), null);
        check('explicit JSON download unchanged; save clean and removes draft');
        await page.click('#insert-equation-button');
        await page.evaluate(() => {
            beginHistoryTransaction('draft fixture: image and group metadata');
            model.elements[0].groupId = 'recovery-group';
            model.elements[1].groupId = 'recovery-group';
            model.elements.push({ id: 'draft-image', type: 'image', x: 20, y: 25, width: 40, height: 45,
                imageDataUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aR1kAAAAASUVORK5CYII=',
                imageMimeType: 'image/png', imageNaturalWidth: 1, imageNaturalHeight: 1, selected: false });
            commitHistoryTransaction();
            renderElements();
            updateModelPreview();
        });
        const edited = await snapshot();
        page.once('dialog', dialog => dialog.dismiss());
        await page.click('#reset-button');
        assert.deepEqual(await snapshot(), edited);
        check('dirty Reset cancellation preserves document');
        // Reload in a new tab sharing storage avoids automation dismissing beforeunload.
        const recoveredPage = await context.newPage();
        await recoveredPage.goto(url);
        await recoveredPage.locator('#draft-recovery-dialog').waitFor({ state: 'visible' });
        assert.notDeepEqual(await recoveredPage.evaluate(() => model), edited);
        await recoveredPage.click('#recover-draft-button');
        assert.deepEqual(await recoveredPage.evaluate(() => model), edited);
        assert.equal(await recoveredPage.evaluate(() => getDraftStatus().dirty), true);
        check('explicit startup recovery restores full model and remains dirty');
        const discardPage = await context.newPage();
        await discardPage.goto(url);
        await discardPage.click('#discard-draft-button');
        assert.equal(await discardPage.evaluate(key => localStorage.getItem(key), key), null);
        assert.equal(await discardPage.evaluate(() => getDraftStatus().dirty), false);
        check('Discard removes draft without replacing initial model');
        page.once('dialog', dialog => dialog.accept());
        await page.setInputFiles('#file-input', {
            name: 'saved.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(saved))
        });
        await page.waitForFunction(() => !getDraftStatus().dirty);
        assert.deepEqual(await snapshot(), saved);
        check('successful project open establishes clean checkpoint');
        const ir = await page.evaluate(() => exportToIR());
        const tex = await page.evaluate(async ir => (await fetch('/api/export-latex', {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ model: ir })
        })).text(), ir);
        await page.setInputFiles('#latex-file-input', {
            name: 'current.tex', mimeType: 'application/x-tex', buffer: Buffer.from(tex)
        });
        await page.waitForFunction(() => getDraftStatus().dirty);
        assert.equal((await status()).dirty, true);
        check('successful conforming import is unsaved dirty project');
        const imported = await snapshot();
        assert(imported.elements.some(element => element.type === 'title'));
        assert(imported.elements.some(element => element.type === 'author'));
        const importDraft = await page.evaluate(key => JSON.parse(localStorage.getItem(key)), key);
        assert.deepEqual(importDraft.model, imported);
        const importRecoveryPage = await context.newPage();
        await importRecoveryPage.goto(url);
        await importRecoveryPage.locator('#draft-recovery-dialog').waitFor({ state: 'visible' });
        await importRecoveryPage.click('#recover-draft-button');
        assert.deepEqual(await importRecoveryPage.evaluate(() => model), imported);
        assert.equal(await importRecoveryPage.evaluate(() => getDraftStatus().dirty), true);
        const importSave = importRecoveryPage.waitForEvent('download');
        await importRecoveryPage.click('#save-button');
        const importDownload = await importSave;
        assert.deepEqual(JSON.parse(fs.readFileSync(await importDownload.path(), 'utf8')), imported);
        assert.equal(await importRecoveryPage.evaluate(() => getDraftStatus().dirty), false);
        assert.equal(await importRecoveryPage.evaluate(key => localStorage.getItem(key), key), null);
        check('marked conforming import title/author draft survives startup, recovers exactly, stays dirty until Save');
        page.once('dialog', dialog => dialog.accept());
        await page.click('#reset-button');
        assert.equal((await status()).dirty, true);
        await page.click('#undo-button');
        assert.equal((await status()).dirty, true);
        check('accepted Reset remains undoable and unsaved import has no false clean checkpoint');
        await context.close();

        for (const failure of ['quota', 'unavailable']) {
            const failing = await browser.newContext({ acceptDownloads: true });
            await failing.addInitScript(mode => {
                if (mode === 'quota') Storage.prototype.setItem = () => { throw new DOMException('full', 'QuotaExceededError'); };
                else Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('blocked', 'SecurityError'); } });
            }, failure);
            const p = await failing.newPage();
            await p.goto(url);
            const count = await p.evaluate(() => model.elements.length);
            await p.click('#insert-equation-button');
            assert.equal(await p.evaluate(() => model.elements.length), count + 1);
            assert(await p.evaluate(() => getDraftStatus().storage_error));
            assert(await p.locator('#draft-status').isVisible());
            const pending = p.waitForEvent('download');
            await p.click('#save-button');
            assert.equal((await pending).suggestedFilename(), 'guilatex_project.json');
            assert.equal(await p.evaluate(() => getDraftStatus().dirty), false);
            check(`${failure} storage failure visible; memory edit and JSON save work`);
            await failing.close();
        }
        if (process.env.GUILATEX_TEST_EVIDENCE) {
            fs.writeFileSync(path.resolve(process.env.GUILATEX_TEST_EVIDENCE), JSON.stringify({ checks, result: 'PASS' }, null, 2));
        }
        console.log(`${checks.length}/${checks.length} draft recovery checks PASS`);
    } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
