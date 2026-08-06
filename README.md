# Ghost / Invisibility Mode

A webcam app that makes you disappear when you pinch your fingers.
Pinch your thumb and index finger together and your whole body vanishes,
revealing the empty room behind you, while the rest of the video stays live.

## How it works

The app stacks three pieces together:

1. **Gesture trigger (MediaPipe Hands).** It tracks 21 landmarks on each
   hand and measures the gap between your thumb tip and index tip. A pinch
   toggles ghost mode on or off.
2. **The vanishing (MediaPipe Selfie Segmentation).** Each frame it builds a
   mask of where your body is, then paints those pixels with a clean photo of
   the empty room that you captured at the start.
3. **The HUD (OpenCV).** The title, FPS counter, crosshair, and the yellow
   GHOST ACTIVE label are just text and shapes drawn on top of each frame.

## Setup

You need Python 3.9 to 3.12. MediaPipe does not yet support 3.13.

Open a terminal inside this folder and run:

```
python -m venv venv
```

Activate the environment.

On Windows:

```
venv\Scripts\activate
```

On macOS or Linux:

```
source venv/bin/activate
```

Then install the dependencies:

```
pip install -r requirements.txt
```

## Run

```
python ghost.py
```

A window opens showing your webcam.

## Using it

1. Step out of frame so the camera sees only the empty room.
2. Press the `b` key to capture that empty room as your background.
3. Sit back down.
4. Pinch your thumb and index finger together to vanish. Pinch again to reappear.

### Keys

| Key | Action                                            |
|-----|---------------------------------------------------|
| `b` | Capture or recapture the background               |
| `q` | Quit                                              |

## Tips

* Keep the camera on a fixed surface. The illusion breaks the moment the
  background photo stops matching the live view, so any camera movement ruins it.
* Recapture the background with `b` whenever the lighting changes.
* If the edges of your body flicker, raise the mask threshold (the `0.5` in
  `ghost.py`) or increase the blur on the mask.

## Troubleshooting

* **Black window or no camera.** Another app may be using the webcam. Close it,
  or change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` for a second camera.
* **Cannot install mediapipe.** Check your Python version with
  `python --version`. It must be 3.9 to 3.12.
* **Low FPS.** Lower the capture resolution near the top of `ghost.py`.
