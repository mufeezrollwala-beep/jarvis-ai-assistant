# Quick Start Guide - Jarvis Dashboard

## TL;DR

```bash
# Launch the dashboard with demo data
python scripts/run_ui.py --mock
```

That's it! The dashboard will open with a stunning Iron Man-inspired interface showing simulated activity.

## 30-Second Demo

1. **Launch**: `python scripts/run_ui.py --mock`
2. **Wait 2 seconds**: Mock data starts populating
3. **Observe**: 
   - Conversations appearing (left panel)
   - Tasks updating (center panel)
   - Metrics displaying (top right)
   - Memory items adding (bottom right)
   - Waveform animating (bottom)
4. **Try controls**:
   - Click "High Contrast" (top bar)
   - Click "A+" to increase font size
   - Click "A-" to decrease font size

## What You'll See

```
┌─────────────────────────────────────────────────────────────────┐
│  [J] J.A.R.V.I.S SYSTEM  │  Status  │  [Controls]  │  12:34:56  │ ← Top Bar
├──────────────┬──────────────┬──────────────────────────────────┤
│              │              │  ┌────────────┬────────────┐      │
│ Conversation │   Task       │  │    CPU     │   Memory   │      │
│     Feed     │   Status     │  │   45.2%    │   62.8%    │      │
│              │              │  ├────────────┼────────────┤      │
│ User: Hello  │ Task_001     │  │    Disk    │  Network   │      │
│ Jarvis: Hi   │ [Running]    │  │   55.0%    │  ↓1024 MB  │      │
│              │              │  └────────────┴────────────┘      │
│              │ Task_002     ├──────────────────────────────────┤
│              │ [Completed]  │  Memory Snippets                 │
│              │              │  • User Preference: ...          │
│              │              │  • Last Command: ...             │
└──────────────┴──────────────┴──────────────────────────────────┘
│                    Audio Waveform Visualizer                     │
│  ╱╲   ╱╲                                            [LIVE] ●     │
└─────────────────────────────────────────────────────────────────┘
```

## Command Options

### Basic Usage
```bash
python scripts/run_ui.py
```
Launches with real system metrics (no mock data).

### Mock Data Mode
```bash
python scripts/run_ui.py --mock
```
Launches with simulated data for development/demo.

### Headless Mode
```bash
python scripts/run_ui.py --headless
```
Launches without display (for testing/CI/CD).

### Combined
```bash
python scripts/run_ui.py --mock --headless
```
Mock data + headless (useful for automated testing).

### Help
```bash
python scripts/run_ui.py --help
```
Shows all available options.

## Keyboard/Mouse Actions

### Top Bar Controls
- **High Contrast Button**: Toggle between normal and high contrast themes
- **A- Button**: Decrease font size (minimum 50%)
- **A+ Button**: Increase font size (maximum 200%)

### Panel Interactions
- **Scroll**: Use mouse wheel in any panel to scroll through history
- **Window Resize**: Drag window edges to resize (minimum 1280x720)

## What Each Panel Shows

### 📱 Conversation Feed (Left)
Real-time chat between user and Jarvis.
- **User messages**: Cyan color
- **Jarvis responses**: Green color
- **Auto-scroll**: New messages appear at bottom

### 📋 Task Status (Center)
Live task monitoring with status indicators.
- **Pending**: Blue badge
- **Running**: Orange badge (pulsing)
- **Completed**: Green badge

### 📊 System Metrics (Top Right)
Real-time system performance.
- **CPU**: Processor usage
- **Memory**: RAM usage
- **Disk**: Storage usage
- **Network**: Download speed

### 🧠 Memory Snippets (Bottom Right)
Key-value memory storage.
- Shows recent memory items
- Useful for preferences and notes
- Chronologically ordered

### 🎵 Waveform Visualizer (Bottom)
Audio visualization.
- Real-time waveform display
- Shows voice activity
- "LIVE" indicator pulses

## Accessibility Features

### High Contrast Mode
**Purpose**: Better visibility for visually impaired users

**How to use**: Click "High Contrast" button in top bar

**Changes**:
- Background: Black
- Text: White
- Accents: Yellow
- Higher contrast ratios

### Font Scaling
**Purpose**: Adjust text size for readability

**How to use**: 
- Click "A-" to decrease (50% minimum)
- Click "A+" to increase (200% maximum)

**Effect**: All text scales proportionally

## Troubleshooting

### Issue: Window doesn't appear
**Solution**: Try headless mode to check for errors
```bash
python scripts/run_ui.py --mock --headless
```

### Issue: "Module not found" error
**Solution**: Activate virtual environment
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Issue: No data showing
**Solution**: Use mock mode
```bash
python scripts/run_ui.py --mock
```

### Issue: Qt platform error
**Solution**: Install system dependencies (see INSTALL.md)
```bash
sudo apt-get install -y libgl1 libegl1 libglib2.0-0
```

## Testing

### Run Unit Tests
```bash
python scripts/test_ui.py
```
Expected output: "All tests passed!"

### Quick Verification
```bash
python scripts/run_ui.py --help
```
Should show usage information.

## Next Steps

After trying the quick start:

1. **Read Features**: Check `DASHBOARD_FEATURES.md` for complete feature list
2. **Integration**: See `INTEGRATION_GUIDE.md` to connect with voice assistant
3. **Installation**: Read `INSTALL.md` for production setup
4. **Architecture**: See `ARCHITECTURE.md` for technical details

## Tips

💡 **Best for Demo**: Use `--mock` flag to show all features  
💡 **Best for Dev**: Run without flags to see real metrics  
💡 **Best for Testing**: Use `--headless` for automated tests  
💡 **Accessibility**: Try high contrast mode in bright environments  
💡 **Readability**: Adjust font size to your preference  

## Getting Help

- **Error Messages**: Check console output for details
- **Installation Issues**: See `INSTALL.md`
- **Integration Questions**: See `INTEGRATION_GUIDE.md`
- **Feature Questions**: See `DASHBOARD_FEATURES.md`

## Five-Minute Tour

1. **Launch**: `python scripts/run_ui.py --mock`
2. **Wait 10 seconds**: Let data populate
3. **Click "High Contrast"**: See theme change
4. **Click "A+"** three times: See fonts scale up
5. **Click "A-"** three times: See fonts scale down
6. **Watch animations**: Notice pulsing, fading, sliding effects
7. **Observe waveform**: See it animate continuously
8. **Check all panels**: Verify data in each section
9. **Scroll panels**: Test scrolling in longer lists
10. **Close window**: Application exits cleanly

**Total time**: 5 minutes to see all major features! ✨

---

**Ready to explore?** Just run:
```bash
python scripts/run_ui.py --mock
```

**Enjoy your Jarvis interface!** 🚀
