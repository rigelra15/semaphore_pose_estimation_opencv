# Semaphore Pose Capture

A Python project to capture and save human pose landmarks based on semaphore poses using the MediaPipe library. The captured pose data is saved as JSON files and can be used for further analysis or comparison.

## Features

- **Pose Detection**: Utilizes MediaPipe Pose module to detect human body landmarks.
- **Pose Capture**: Captures the pose data and saves it to a JSON file based on the selected semaphore letter (A-Z).
- **Graphical User Interface (GUI)**: Built using `customtkinter` to make the application user-friendly, allowing users to select images and save captured poses.
- **File Saving**: Saves the detected pose landmarks as JSON files in the `semaphore poses` folder.

## Requirements

- Python 3.x
- `opencv-python` for image processing and camera access
- `mediapipe` for pose detection
- `customtkinter` for GUI development
- `tkinter` for file dialog and message box support

You can install the required libraries using pip:

```bash
pip install opencv-python mediapipe customtkinter
