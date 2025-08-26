# PC Gesture Controls

> NOTE: webcam video display is disabled for the multithreaded version. If you wish to use this, pull/clone a version prior to multithreading. 

Webcam‑based hand gesture mouse controller. Move your palm to move the cursor. Pinch gestures trigger mouse buttons:

- Thumb + Index pinch (tips closer than ~5% of frame width) => Left mouse button (hold while pinched)
- Thumb + Pinky pinch => Right mouse button (hold while pinched)

Built with MediaPipe Hands for landmark detection and PyAutoGUI for OS‑level mouse control.

## Features
- Real‑time single‑hand tracking (up to 30 FPS depending on your webcam / CPU)
- Smooth cursor movement based on average palm landmark position
- Click & right‑click by natural pinch gestures (continuous hold while pinched)
- Optional on‑screen visualization (landmarks + palm marker)
- Simple, extensible codebase (three Python files)

## Project Structure
```
main.py          # Entry point: wires gesture tracking to the mouse controller
controller.py    # Cursor movement + (left/right) click state handling (PyAutoGUI)
gestures.py      # MediaPipe Hands wrapper + gesture detection logic
```

## Requirements
- Python 3.10+ (tested with 3.11)
- Webcam
- Windows, macOS, or Linux (instructions below use PowerShell for Windows)

Python packages:
- mediapipe
- opencv-python
- numpy
- pyautogui

## Installation (Windows PowerShell)
There are two dependency sets:

1. Minimal (recommended) – only what the app actually needs: use `requirements-min.txt`
2. Full lock snapshot – everything currently in the dev environment (many transitive / unused libs) in `requirements.txt`

```powershell
# 1. Clone repo (or download sources) and enter folder
# git clone https://github.com/EDiasAlberto/PCGestureControls.git
# cd PCGestureControls

# 2. Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Upgrade pip (optional)
python -m pip install --upgrade pip

# 4a. Install ONLY required runtime deps (lean)
pip install -r requirements-min.txt

# 4b. (Alternative) Reproduce full original environment
# pip install -r requirements.txt
```

PyAutoGUI may pull in Pillow automatically; if missing: `pip install pillow`.

## Running
```powershell
python main.py
```
Press ESC in the visualization window (if enabled) or Ctrl+C in the terminal to exit.

By default `main.py` disables the PyAutoGUI failsafe (moving mouse to a screen corner will NOT auto‑abort). If your cursor becomes hard to control, press ESC (if window open) or re‑enable failsafe manually.

## Gestures
| Gesture | Action |
|---------|--------|
| Thumb + Index pinch | Left mouse button down (released when unpinched) |
| Thumb + Pinky pinch | Right mouse button down (released when unpinched) |

Pinch threshold is a normalized landmark distance < 0.05. Adjust this in `gestures.py` if you experience accidental clicks.

## Configuration
`GestureTracking(positionHandler, camera_index=0, detection_confidence=0.5, tracking_confidence=0.5)` in `gestures.py`:
- `camera_index`: Change if you have multiple webcams (0 = default)
- `detection_confidence`, `tracking_confidence`: Raise (e.g. 0.7) for fewer false positives (slightly slower)
- Visualization: Pass `True` to `gestures.run(True)` in `main.py` to enable landmark drawing & palm marker

## How It Works
1. OpenCV captures frames from the selected webcam.
2. MediaPipe Hands returns 21 normalized landmarks for the detected hand.
3. Palm position = mean of selected MCP & wrist landmarks → mapped to screen coordinates (x inverted for natural mirroring).
4. Distances (Euclidean in normalized space) between Thumb tip (4) & Index tip (8), and Thumb tip & Pinky tip (20) determine pinch states.
5. `Controller` (PyAutoGUI) moves cursor and manages idempotent mouseDown/mouseUp for left & right buttons.

## Key Code Points
- Gesture logic: `gestures.py` (`distance`, pinch thresholds, `average_pos`)
- Cursor mapping: `controller.move_cursor` scales normalized coordinates to screen size
- Click state guard: prevents repeated `mouseDown` calls while holding a pinch

## Adjusting Sensitivity
- Lower threshold (e.g. 0.04) for stricter pinch detection (fewer false positives, harder to trigger)
- Higher threshold (e.g. 0.06) for easier pinches (risk of accidental clicks)

## Safety / Notes
- PyAutoGUI failsafe is disabled for smoother full‑screen control: re‑enable by deleting the `pag.FAILSAFE = False` line if desired.
- Always test in a non‑critical environment first; unintended clicks can cause data loss.
- Lighting matters: ensure even illumination for best landmark stability.

## Troubleshooting
| Issue | Possible Fix |
|-------|--------------|
| No camera / black window | Check `camera_index` or that webcam isn't in use by another app. |
| Cursor jitter | Improve lighting; raise `detection_confidence`; add smoothing (see Improvements). |
| Accidental clicks | Lower pinch threshold; keep fingers more separated when moving. |
| Right click not triggering | Ensure pinky fully visible; adjust threshold; better lighting. |

## Extending
Ideas:
- Add scroll gesture (e.g., thumb + middle pinch while moving vertically)
- Add smoothing/filter (exponential moving average of palm position)
- Multi‑hand support (secondary hand for modifier keys)
- Sensitivity & threshold command‑line arguments
- UI overlay to show active gesture states

## Minimal Example (Headless Mode)
If you prefer running without visualization (already default in `main.py`):
```python
from gestures import GestureTracking
from controller import Controller

controller = Controller()

def handler(x, y, isPinching, isSecondaryPinching):
    controller.move_cursor(x, y)
    (controller.mouseDown() if isPinching else controller.mouseUp())
    (controller.rightClickDown() if isSecondaryPinching else controller.rightClickUp())

GestureTracking(handler).run(False)
```

## License
Add a license file (e.g. MIT) if you plan to share / open source formally.

## Disclaimer
This tool simulates mouse input. Use responsibly and at your own risk.

---
Happy hands‑free computing! Contributions & suggestions welcome.
