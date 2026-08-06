"""
Ghost / Invisibility Mode  (smooth fade)
A webcam app that makes you gradually fade away when you pinch your fingers.

Pinch once and you dissolve to invisible over about 1.5 seconds. Pinch again
and you fade back in over the same time. Change FADE_SECONDS to make the fade
faster or slower.

The background is a FIXED capture, so your own shape can never soak into it
and make you translucent by accident. A tiny lighting correction is made only
FAR from your body, so slow lighting changes are tracked without baking in.

If the image is dark or green from an earlier version, the lines under
"RESET CAMERA TO AUTO" put the webcam back to normal.

Best results come from setup, not code:
  * put the camera on something FIXED and do not move it
  * light yourself from the FRONT (face a window or a lamp) so no shadow
  * stand at a normal distance, not right up against the camera
  * be COMPLETELY out of frame when you press 'b'

Keys:
  b  capture / reset the background (step out of frame first)
  q  quit
"""

import time
import cv2
import numpy as np
import mediapipe as mp

# ---------- setup ----------
mp_hands = mp.solutions.hands
mp_seg = mp.solutions.selfie_segmentation
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)
segmenter = mp_seg.SelfieSegmentation(model_selection=1)

# CAP_DSHOW opens the camera faster on Windows. If the camera fails to
# open, delete ", cv2.CAP_DSHOW" and just use cv2.VideoCapture(0).
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

# ---- RESET CAMERA TO AUTO (undo any earlier dark / green lock) ----
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)   # auto exposure back on
cap.set(cv2.CAP_PROP_AUTO_WB, 1)            # auto white balance back on
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)         # autofocus back on
# -------------------------------------------------------------------

background = None       # FIXED plate we paint you out with
ghost = False           # is invisibility currently REQUESTED (the toggle)
fade_level = 0.0        # 0 = fully visible, 1 = fully invisible (slides between)
last_toggle = 0.0       # cooldown so one pinch does not flip it repeatedly
prev_time = time.time()
persist = None          # mask that lingers a few frames to stop flicker

FADE_SECONDS = 1.5      # how long the fade in / fade out takes
DIFF_THRESH = 18        # how different from the background a pixel must be
SHADOW_DROP = 12        # how much darker than the background counts as shadow
BG_DRIFT = 0.03         # tiny lighting correction, ONLY far from your body
KERNEL = np.ones((5, 5), np.uint8)
BIG_KERNEL = np.ones((9, 9), np.uint8)
GREEN = (80, 255, 80)
YELLOW = (60, 220, 255)


def distance(a, b):
    return np.hypot(a[0] - b[0], a[1] - b[1])


def is_pinch(lm, w, h):
    """True when thumb tip (4) and index tip (8) are close, scaled by hand size."""
    thumb = (lm[4].x * w, lm[4].y * h)
    index = (lm[8].x * w, lm[8].y * h)
    wrist = (lm[0].x * w, lm[0].y * h)
    mid = (lm[9].x * w, lm[9].y * h)
    hand_size = distance(wrist, mid) + 1e-6
    return distance(thumb, index) / hand_size < 0.4


def keep_largest_blobs(mask, min_area=1500):
    """Keep only sizeable connected regions, delete tiny stray speckle."""
    num, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    clean = np.zeros_like(mask)
    for i in range(1, num):                       # skip 0, which is the background
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            clean[labels == i] = 1
    return clean


# ---------- main loop ----------
print("Step out of frame, then press 'b' to capture the background.")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)
    clean = frame.copy()            # pristine copy: used for capture AND the effect
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ---- timing (also drives the fade so it is the same speed at any FPS) ----
    now = time.time()
    dt = now - prev_time
    prev_time = now
    fps = 1.0 / dt if dt > 0 else 0.0

    # ---- gesture detection ----
    hand_result = hands.process(rgb)
    pinch_now = False
    if hand_result.multi_hand_landmarks:
        for hlm in hand_result.multi_hand_landmarks:
            if is_pinch(hlm.landmark, w, h):
                pinch_now = True
            if fade_level < 0.05:               # only show skeleton while visible
                mp_draw.draw_landmarks(frame, hlm, mp_hands.HAND_CONNECTIONS)

    if pinch_now and now - last_toggle > 1.0:
        ghost = not ghost
        last_toggle = now

    # ---- slide the fade level toward the target (full or none) ----
    target = 1.0 if ghost else 0.0
    step = dt / FADE_SECONDS
    if fade_level < target:
        fade_level = min(target, fade_level + step)
    elif fade_level > target:
        fade_level = max(target, fade_level - step)

    # ---- the invisibility effect (runs while any fade is in progress) ----
    if fade_level > 0.001 and background is not None:
        bg_uint8 = background.astype(np.uint8)

        # A. torso / head from the person detector
        seg = segmenter.process(rgb)
        seg_mask = (seg.segmentation_mask > 0.5).astype(np.uint8)

        # B. anything different from the background (this is what catches hands)
        diff = cv2.absdiff(clean, bg_uint8)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, diff_mask = cv2.threshold(gray, DIFF_THRESH, 1, cv2.THRESH_BINARY)

        # C. shadow: areas that got DARKER than the background
        plate_gray = cv2.cvtColor(bg_uint8, cv2.COLOR_BGR2GRAY).astype(np.int16)
        live_gray = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY).astype(np.int16)
        shadow_mask = ((plate_gray - live_gray) > SHADOW_DROP).astype(np.uint8)

        # union of all three, then clean up
        person = cv2.bitwise_or(seg_mask, diff_mask)
        person = cv2.bitwise_or(person, shadow_mask)
        person = cv2.morphologyEx(person, cv2.MORPH_OPEN, BIG_KERNEL)   # wipe speckle
        person = cv2.morphologyEx(person, cv2.MORPH_CLOSE, BIG_KERNEL)  # fill holes
        person = keep_largest_blobs(person, min_area=1500)             # drop stray spots
        person = cv2.dilate(person, KERNEL, iterations=2)              # cover edges/hair

        # persistence: new areas turn on instantly, old areas fade slowly (no flicker)
        pf = person.astype(np.float32)
        if persist is None or persist.shape != pf.shape:
            persist = pf
        else:
            persist = np.maximum(pf, persist * 0.85)

        # tiny lighting drift correction, ONLY far from the body so you never bake in
        far = 1 - cv2.dilate(person, BIG_KERNEL, iterations=8)
        farf = far.astype(np.float32)[:, :, None]
        background = background + (BG_DRIFT * farf) * (clean.astype(np.float32) - background)

        # solid interior, softened edge, THEN scaled by the fade level so you
        # dissolve in and out gradually instead of snapping
        solid = (persist > 0.5).astype(np.float32)
        m = cv2.GaussianBlur(solid, (7, 7), 0)
        m = (m * fade_level)[:, :, None]

        frame = (clean * (1 - m) + background * m).astype(np.uint8)
    else:
        persist = None

    # ---- HUD ----
    cv2.putText(frame, "Ghost / Invisibility Mode", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, YELLOW, 2)
    cv2.putText(frame, f"FPS {fps:04.1f}", (w - 160, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, GREEN, 2)
    if fade_level > 0.5:
        cv2.putText(frame, "GHOST ACTIVE", (w - 205, 72),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, YELLOW, 2)
    cv2.drawMarker(frame, (w // 2, h // 2), GREEN, cv2.MARKER_CROSS, 20, 1)

    cv2.imshow("Ghost", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('b'):
        background = clean.astype(np.float32)
        persist = None
        print("Background captured.")

cap.release()
cv2.destroyAllWindows()