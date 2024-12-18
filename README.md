# Semaphore Pose Estimation using MediaPipe

A Python project to capture, analyze, and compare human pose landmarks based on semaphore poses using the MediaPipe library. The captured pose data is saved as JSON files and can be used for further analysis or comparison.

**Semaphore** in this context refers to the signaling system used in scouting (Pramuka) to communicate messages over long distances using two flags. The flags are held in specific positions to represent different letters of the alphabet, allowing scouts to send messages without speaking.

![semaphore-pict](semaphore.gif)

## Abstract

This project aims to capture and analyze human pose landmarks based on semaphore poses using the MediaPipe library. The system detects human body landmarks using the MediaPipe Pose module and captures the pose data for each semaphore letter (A-Z). The captured pose data is saved as JSON files in the `semaphore poses` folder and can be used for further analysis or comparison.

The system provides a graphical user interface (GUI) built with `customtkinter` for a user-friendly interface. Users can select images and save captured poses based on the selected semaphore letter. The system also provides functionality to test and capture semaphore poses based on predefined letters and compares the captured pose against those stored in JSON files.

## Features

- **Pose Detection**: Uses the MediaPipe Pose module to detect human body landmarks.
- **Pose Capture**: Captures pose data and saves it to a JSON file based on the selected semaphore letter (A-Z).
- **Graphical User Interface (GUI)**: Built with `customtkinter` for a user-friendly interface, allowing users to select images and save captured poses.
- **File Saving**: Saves the detected pose landmarks as JSON files in the `semaphore poses` folder.
- **Testing Semaphore**: Provides functionality to test and capture semaphore poses based on predefined letters and compares the captured pose against those stored in JSON files.

## Requirements

- Python 3.x
- `opencv-python` for image processing and camera access
- `mediapipe` for pose detection
- `customtkinter` for GUI development
- `tkinter` for file dialog and message box support

## How to Use

1. Clone the repository to your local machine.
2. Install the required libraries using the following command:

```bash
pip install -r requirements.txt
```

3. Run the `get_landmark.py` script to get the pose landmarks from data images `poses_data`. The script will save the landmarks in the `semaphore_poses` folder.

```bash
python get_landmark.py
```

4. If you want to test the semaphore poses, run the `main.py` script. The script will display the semaphore letter and the captured pose landmarks.

```bash
python main.py
```


## Limitations and Development Stage

Please note that this project is still in the early stages of development. The pose detection is based on **MediaPipe 3D landmarks**, but the accuracy and reliability of pose detection, especially for semaphore poses, may not be fully optimized. The application captures and saves pose data into JSON files, but further refinement is needed to improve pose recognition, real-time performance, and accuracy.

This system is still being tested, and there may be issues with pose alignment or inaccurate landmark identification in some poses. The captured data is currently intended for experimentation and further development.