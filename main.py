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

    # Calculate number of fire-like pixels
    fire_pixels = cv2.countNonZero(mask)

    if fire_pixels > 2000:  # You can adjust this threshold
        return True, mask
    return False, mask

# Tkinter setup
root = tk.Tk()
root.withdraw()  # Hide main window

# Open webcam (or replace 0 with a video file path)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fire_detected, mask = detect_fire(frame)

    if fire_detected:
        print("🔥 Fire Detected!")
        messagebox.showwarning("Fire Alert", "🔥 Fire Detected!")

    cv2.imshow("Live Feed", frame)
    cv2.imshow("Fire Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
