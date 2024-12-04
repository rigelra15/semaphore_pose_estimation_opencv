import cv2
import mediapipe as mp
import json
import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

landmark_names = {
    0: "nose", 1: "left_eye_inner", 2: "left_eye", 3: "left_eye_outer", 4: "right_eye_inner",
    5: "right_eye", 6: "right_eye_outer", 7: "left_ear", 8: "right_ear", 9: "mouth_left", 
    10: "mouth_right", 11: "left_shoulder", 12: "right_shoulder", 13: "left_elbow", 
    14: "right_elbow", 15: "left_wrist", 16: "right_wrist", 17: "left_pinky", 
    18: "right_pinky", 19: "left_index", 20: "right_index", 21: "left_thumb", 
    22: "right_thumb", 23: "left_hip", 24: "right_hip", 25: "left_knee", 
    26: "right_knee", 27: "left_ankle", 28: "right_ankle", 29: "left_heel", 
    30: "right_heel", 31: "left_foot_index", 32: "right_foot_index"
}

folder_name = "semaphore poses"
os.makedirs(folder_name, exist_ok=True)

def save_landmarks_to_json(landmarks, selected_letter):
    file_name = os.path.join(folder_name, f"semaphore_pose_{selected_letter}.json")

    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    landmarks_data = []
    for idx, landmark in enumerate(landmarks):
        landmarks_data.append({
            "landmark_name": landmark_names.get(idx, f"landmark_{idx}"),
            "x": landmark.x,
            "y": landmark.y,
            "z": landmark.z
        })

    data.append({"pose_landmarks": landmarks_data})

    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    
    messagebox.showinfo("Capture", f"Pose captured and saved to {file_name}!")

def open_image():
    file_path = filedialog.askopenfilename(title="Pilih Gambar", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image = cv2.imread(file_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                selected_letter = letter_select.get()
                save_landmarks_to_json(landmarks, selected_letter)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Semaphore Pose Capture")
root.geometry("400x300")

frame_buttons = ctk.CTkFrame(root)
frame_buttons.pack(expand=True, fill='both', padx=10, pady=10)

letters = [chr(i) for i in range(ord('A'), ord('Z')+1)]
letter_select = ctk.CTkComboBox(frame_buttons, values=letters, font=("Helvetica", 12), state="readonly")
letter_select.set("A")
letter_select.pack(pady=10)

open_button = ctk.CTkButton(frame_buttons, text="Open Image", command=open_image, font=("Helvetica", 14, "bold"), width=200, height=40)
open_button.pack(pady=10)

quit_button = ctk.CTkButton(frame_buttons, text="Quit", command=root.quit, font=("Helvetica", 14, "bold"), width=200, height=40)
quit_button.pack(pady=10)

root.mainloop()