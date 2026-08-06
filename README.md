# 👻 Ghost / Invisibility Mode

Transform yourself into a ghost using Computer Vision! This project creates a smooth invisibility effect where your body gradually fades away when you perform a simple finger pinch gesture in front of your webcam.

Inspired by the famous "Invisible Cloak" concept, this project uses **MediaPipe**, **OpenCV**, and **AI-based Selfie Segmentation** to replace your body with a previously captured background, creating a realistic disappearing effect.

---

## 🎥 Demo

> 📹 Add a GIF or demo video here

Example:

![Demo](demo.gif)

---

# ✨ Features

- 👻 Smooth fade-in / fade-out invisibility animation
- 🤏 Finger pinch gesture to toggle invisibility
- 🎯 AI Selfie Segmentation for accurate body detection
- 🖐 Hand tracking using MediaPipe Hands
- 🖼 Background replacement using a captured static frame
- 💡 Automatic lighting adaptation
- 🌟 Soft edge blending for realistic transitions
- ⚡ Real-time webcam processing
- 📈 Live FPS counter
- 🔄 One-key background recapture

---

# 🛠 Technologies Used

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ghost-invisibility-mode.git
```

Move into the project

```bash
cd ghost-invisibility-mode
```

Install dependencies

```bash
pip install opencv-python mediapipe numpy
```

---

# ▶️ Run

```bash
python ghost.py
```

---

# 🎮 Controls

| Key | Action |
|------|--------|
| **b** | Capture / Reset Background |
| **q** | Quit Application |

---

# 🖐 Gesture Controls

Perform a **Thumb + Index Finger Pinch**

✅ First Pinch
- Become Invisible

✅ Second Pinch
- Fade Back In

The transition takes approximately **1.5 seconds** for a smooth effect.

---

# 📸 Best Results

For the best invisibility effect:

- Keep the webcam fixed.
- Do not move the camera after capturing the background.
- Stand at a normal distance.
- Face a light source.
- Minimize shadows.
- Step completely out of the frame before pressing **B**.

---

# ⚙ How It Works

### 1. Background Capture

The application captures a clean background frame when the user presses **B**.

---

### 2. Hand Tracking

MediaPipe Hands detects hand landmarks and recognizes a thumb-index pinch gesture.

---

### 3. Person Detection

MediaPipe Selfie Segmentation generates a human mask.

---

### 4. Motion Detection

The live frame is compared against the captured background to detect movement.

---

### 5. Shadow Detection

Additional processing detects darker regions to preserve realistic body boundaries.

---

### 6. Mask Refinement

Morphological operations remove noise and smooth edges.

---

### 7. Smooth Fade

Instead of instantly disappearing, the body opacity is gradually interpolated over time for a cinematic fade effect.

---

# 📂 Project Structure

```
Ghost-Invisibility-Mode/
│
├── ghost.py
├── README.md
├── requirements.txt
├── demo.gif
└── screenshots/
```

---

# 🚀 Future Improvements

- Multiple gesture controls
- Dynamic background updating
- Green-screen mode
- Recording support
- Custom fade speed settings
- Full-body tracking improvements
- AR visual effects
- Mobile version

---

# 📷 Screenshots

Add your screenshots here.

```
screenshots/
```

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# ⭐ If you like this project

Give it a ⭐ on GitHub!

---

# 👨‍💻 Author

**Ebinezer N**

Computer Vision • AI • Python Developer

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

# 📄 License

This project is licensed under the MIT License.
