import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox

def detect_fire(frame):
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for fire color in HSV
    lower = np.array([18, 50, 50], dtype=np.uint8)
    upper = np.array([35, 255, 255], dtype=np.uint8)

    # Threshold the image to get only fire-like colors
    mask = cv2.inRange(hsv, lower, upper)

    # Count fire-like pixels
    fire_pixels = cv2.countNonZero(mask)

    if fire_pixels > 2000:
        return True, mask
    return False, mask

# Tkinter setup
root = tk.Tk()
root.withdraw()  # Hide main window

# Open video file
cap = cv2.VideoCapture("forest_fire_video.mp4")
if not cap.isOpened():
    print("❌ Failed to open video file. Please check the path and filename.")
else:
    print("✅ Video opened successfully. Starting frame loop...")

# Show alert only once
alert_shown = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fire_detected, mask = detect_fire(frame)

    if fire_detected and not alert_shown:
        print("🔥 Fire Detected!")
        messagebox.showwarning("Fire Alert", "🔥 Fire Detected!")
        alert_shown = True  # Prevent repeated alerts

    cv2.imshow("Live Feed", frame)
    cv2.imshow("Fire Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
