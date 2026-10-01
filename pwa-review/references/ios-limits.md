---
description: "iOS/Safari PWA limits and error handling. Read when the target is mobile, installed, or iOS-relevant."
connections: [checklist, report-template]
---

# iOS limits and fetch errors

## Error Handling

### Manifest Not Found
- Score Category 1 (Manifest Compliance) as 0/20
- Score Category 2 (Advanced Manifest) as 0/13
- Add CRITICAL issue: "No manifest.json found"
- Continue with remaining categories

### Service Worker Not Found
- Score Category 3 (Service Worker & Caching) as 0/33
- Score Category 4 (Offline Capability) as 0/24
- Reduce Category 5 (Installability) by 2 points
- Add CRITICAL issue: "No service worker registered"
- Continue with remaining categories

### CORS/Fetch Failures
- Note which resource couldn't be fetched
- Score affected categories as 0
- Add WARNING: "Could not fetch [resource] - CORS or access issue"
- Analyze whatever resources were successfully retrieved

### Invalid JSON (Manifest)
- Score manifest categories as 0
- Add CRITICAL issue: "manifest.json contains invalid JSON"
- Continue with HTML and SW analysis

---

## iOS/Safari Limitations to Note

When generating the report, include these platform-specific notes if relevant:

### Installation & Capabilities
- iOS Safari: `beforeinstallprompt` event not supported (users must manually "Add to Home Screen")
- iOS Safari: Push notifications require iOS 16.4+ and explicit user permission
- iOS Safari: Storage limited to ~50MB (may be evicted under storage pressure)
- iOS Safari: No persistent storage API
- Safari: Service worker scope limitations more strict

### Real-Time Connections
- iOS PWAs are frozen when backgrounded — WebSocket connections die silently (close code 1005)
- When user returns to the app, socket.io's limited reconnection attempts may already be exhausted
- `visibilitychange` event is the reliable signal for detecting return from background on both iOS and Android
- After reconnection, server-side room memberships are lost — must re-join rooms on every `connect` event
- SPA component state is destroyed on navigation — persist critical IDs (active conversation, selected tab) to localStorage

### Safe Area & Display (Critical for PWA Mode)
- **Notch/Dynamic Island**: Without `viewport-fit=cover` in viewport meta, `env(safe-area-inset-*)` won't work
- **Fixed Headers**: Must use `padding-top: env(safe-area-inset-top)` to avoid content being hidden behind notch
- **Fixed Bottom Elements**: Must use `padding-bottom: env(safe-area-inset-bottom)` for home indicator area
- **Status Bar**: `apple-mobile-web-app-status-bar-style` can be `default`, `black`, or `black-translucent`
- PWA mode on iOS shows no browser chrome - safe area handling is essential

### Touch Events & Interactions
- `onClick` handlers may not fire reliably on some iOS versions in PWA mode
- Add `onTouchEnd` as backup for critical buttons (install, update, submit actions)
- Use `touch-manipulation` CSS to eliminate 300ms tap delay and prevent double-tap zoom
- Use `cursor: pointer` CSS on interactive elements - iOS Safari requires this to recognize elements as clickable
- Use `-webkit-tap-highlight-color: transparent` for clean visual feedback
- Use `-webkit-user-select: none` on interactive elements to prevent text selection

### Splash Screens
- iOS requires `<link rel="apple-touch-startup-image">` with media queries for each device size
- Without splash screens, iOS shows blank white screen during PWA launch
- Each iPhone/iPad dimension needs its own splash image (portrait and landscape)

### Z-Index & Stacking Context (Critical)
- **backdrop-filter creates new stacking context**: Headers with `backdrop-blur` or `backdrop-filter` create isolated stacking contexts in iOS Safari. Elements with higher z-index values may still appear BEHIND these elements.
- **Fix**: Add `transform: translate3d(0,0,0)` to elements that need to appear above backdrop-filter elements. This forces GPU layer rendering and fixes stacking order.
- Toast/notification components must have high z-index (e.g., `z-[9999]`) AND `transform: translate3d(0,0,0)` to appear above blurred headers
- iOS Safari has stricter stacking context behavior than Chrome/Firefox

**Example fix for notifications above blurred headers:**
```css
.notification {
  position: fixed;
  z-index: 9999;
  transform: translate3d(0,0,0); /* Forces GPU layer, fixes iOS stacking */
}
```

---

