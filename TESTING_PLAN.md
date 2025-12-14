# MiniKit Integration - Testing Plan

## Overview
This document outlines the testing procedures for the MiniKit SDK v2.8 integration updates.

## Test Environments

### 1. Localhost Development Mode
**URL:** `http://localhost:8000/`

#### Test Cases:

**TC1.1: Friends Mode (Free Access)**
- URL: `http://localhost:8000/?mode=friends`
- Expected: Card reveals without payment prompt
- Steps:
  1. Open URL in browser
  2. Click on the card
  3. Verify card reveals immediately
  4. Check console for "Modo Amigos: Pago omitido" log
- ✅ Pass Criteria: No payment dialog, card reveals successfully

**TC1.2: Dev Mode Payment Simulation**
- URL: `http://localhost:8000/`
- Expected: Payment simulation dialog appears
- Steps:
  1. Open URL in browser
  2. Click on the card
  3. Confirm payment in simulation dialog
  4. Verify card reveals
- ✅ Pass Criteria: Simulation dialog shows "Simular pago de 1.11 WLD", card reveals on confirm

**TC1.3: AI Synthesis Dev Mode**
- URL: `http://localhost:8000/`
- Expected: AI synthesis simulation works
- Steps:
  1. Reveal a card (using TC1.2)
  2. Click the AI synthesis button (✦)
  3. Confirm payment simulation (2.22 WLD)
  4. Verify synthesis appears
- ✅ Pass Criteria: AI synthesis dialog and result display correctly

### 2. World App Simulator

**TC2.1: SDK Detection Test**
- URL: Open `test_minikit.html` in simulator
- Expected: Diagnostic information displayed
- Steps:
  1. Open test_minikit.html in World App simulator
  2. Check logs on page load
  3. Click "TESTEAR CONEXIÓN" button
  4. Review diagnostic output
- ✅ Pass Criteria: 
  - `typeof MiniKit: object`
  - `MiniKit existe en window: ✅`
  - `MiniKit.commands existe: ✅` (or reinstall succeeds)

**TC2.2: Card Reveal Flow**
- URL: Open main app in simulator
- Expected: Payment flow works in simulator
- Steps:
  1. Open index.html in simulator
  2. Click on the card
  3. Complete payment flow
  4. Verify card reveals
- ✅ Pass Criteria: No console errors, payment prompt appears, card reveals

**TC2.3: Commands Availability Check**
- Expected: App handles missing commands gracefully
- Steps:
  1. Monitor console logs during app initialization
  2. Check for "Commands missing. Forcing install()" message
  3. Verify reinstallation succeeds
- ✅ Pass Criteria: If commands initially missing, reinstallation makes them available

### 3. Production World App

**TC3.1: Real Card Reveal Payment (1.11 WLD)**
- URL: Production URL in World App
- Expected: Real WLD payment for card reveal
- Steps:
  1. Open app in World App
  2. Click on card
  3. Review payment details (1.11 WLD to wallet)
  4. Complete payment
  5. Verify card reveals
  6. Check wallet for deduction
- ✅ Pass Criteria: 
  - Payment prompt shows correct amount (1.11 WLD)
  - Payment completes successfully
  - Card reveals after payment
  - Transaction appears in wallet history

**TC3.2: Real AI Synthesis Payment (2.22 WLD)**
- URL: Production URL in World App
- Expected: Real WLD payment for AI synthesis
- Steps:
  1. Complete TC3.1 first
  2. Click AI synthesis button (✦)
  3. Review payment details (2.22 WLD)
  4. Complete payment
  5. Verify synthesis generates and displays
  6. Check wallet for deduction
- ✅ Pass Criteria:
  - Payment prompt shows correct amount (2.22 WLD)
  - Payment completes successfully
  - AI synthesis displays
  - Transaction appears in wallet history

**TC3.3: Payment Confirmation**
- Expected: Funds arrive at destination wallet
- Steps:
  1. After completing TC3.1 and TC3.2
  2. Check destination wallet: `0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6`
  3. Verify transactions received (1.11 + 2.22 = 3.33 WLD)
- ✅ Pass Criteria: Both payments visible in destination wallet

## Error Handling Tests

### E1: No MiniKit Available
- Scenario: Open app in regular browser (not World App)
- Expected: User-friendly error message
- Steps:
  1. Open app in Chrome/Safari/Firefox
  2. Try to reveal card
- ✅ Pass Criteria: Alert displays i18n message "Please open this app from World App"

### E2: Commands Missing After Reinstall
- Scenario: Commands unavailable even after install attempt
- Expected: Clear error message
- Steps:
  1. Simulate environment where commands fail to load
  2. Attempt payment
- ✅ Pass Criteria: Alert displays appropriate error, logs diagnostic info

### E3: Payment Cancellation
- Scenario: User cancels payment
- Expected: Card remains unrevealed, no error
- Steps:
  1. Click card
  2. Cancel payment in World App
- ✅ Pass Criteria: Card stays hidden, no crash, can retry

## Console Log Verification

Expected console outputs:

### On Successful Load:
```
MiniKit install ok [result]
```

### On Payment Attempt:
```
✅ MiniKit Object disponible
```

### If Commands Missing:
```
🔄 Commands missing. Forcing install()...
```

### On Friends Mode:
```
Modo Amigos: Pago omitido.
```

## Browser Compatibility

Test in the following browsers (localhost only):
- [ ] Chrome/Chromium
- [ ] Safari
- [ ] Firefox
- [ ] Edge

## Performance Checks

- [ ] SDK loads within 2 seconds
- [ ] Install completes within 1 second
- [ ] Payment flow completes within 5 seconds
- [ ] No memory leaks during multiple card reveals
- [ ] Responsive UI on mobile viewports

## Regression Tests

Ensure existing functionality still works:
- [ ] Language switching (ES/EN/PT)
- [ ] Card animations
- [ ] Modal displays
- [ ] AI synthesis (with payment)
- [ ] Wallpaper color changes
- [ ] Responsive design

## Security Checks

- [ ] No API keys or secrets in client code
- [ ] Wallet address matches expected: `0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6`
- [ ] HTTPS enforced on production
- [ ] No XSS vulnerabilities in user-facing messages
- [ ] Payment amounts cannot be manipulated client-side

## Pre-Deployment Checklist

Before deploying to production:
- [ ] All localhost tests pass (TC1.x)
- [ ] All simulator tests pass (TC2.x)
- [ ] Wallet address whitelisted in Developer Portal
- [ ] Documentation updated
- [ ] No console errors in any environment
- [ ] Code review completed
- [ ] Security scan completed

## Post-Deployment Verification

After deploying to production:
- [ ] Test TC3.1 with small amount
- [ ] Test TC3.2 with small amount
- [ ] Verify funds received (TC3.3)
- [ ] Monitor error logs for 24 hours
- [ ] Collect user feedback

## Rollback Plan

If critical issues are found:
1. Revert to previous version: `git revert HEAD~6..HEAD`
2. Redeploy previous working version
3. Notify users of temporary downtime
4. Investigate and fix issues
5. Re-test before re-deploying

## Known Limitations

1. **Simulator Quirks**: World App simulator may have partial SDK injection. The app handles this gracefully with reinstallation.
2. **Localhost Limitations**: Real payments cannot be tested on localhost; use dev mode simulation only.
3. **Network Delays**: SDK loading may take longer on slow connections; fallback timeout is 100ms.

## Success Criteria

This integration is considered successful when:
- ✅ All TC1.x tests pass (localhost)
- ✅ All TC2.x tests pass (simulator)
- ✅ All TC3.x tests pass (production)
- ✅ All E1-E3 error handling tests pass
- ✅ No critical console errors
- ✅ Funds received at destination wallet
- ✅ User feedback is positive

## Contact for Issues

If tests fail or issues are found:
- Review console logs first
- Check `MINIKIT_INTEGRATION_SUMMARY.md` for technical details
- Review `world_integration.md` for setup requirements
- Ensure wallet is whitelisted in Developer Portal
