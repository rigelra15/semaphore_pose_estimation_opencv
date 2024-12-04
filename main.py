import cv2
import mediapipe as mp
import json
import math
import os
import re  # Import regular expression module

# Inisialisasi MediaPipe pose dan Drawing
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Fungsi untuk membaca landmark dari file JSON
def read_landmarks_from_json(filename):
    landmarks = []
    with open(filename, 'r') as file:
        data = json.load(file)
        for pose_data in data:
            pose_landmarks = pose_data.get("pose_landmarks", [])
            for landmark in pose_landmarks:
                landmarks.append([landmark["x"], landmark["y"], landmark["z"]])
    return landmarks

# Fungsi untuk mencetak landmark
def print_landmarks(landmarks):
    for idx, landmark in enumerate(landmarks):
        print(f"Landmark {idx}: {landmark}")

# Fungsi untuk menghitung jarak Euclidean antara dua titik 3D
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

# Fungsi untuk menghitung skor kesamaan antara landmark saat ini dan landmark yang disimpan
def calculate_similarity(current_landmarks, stored_landmarks):
    total_distance = 0
    for c_landmark, s_landmark in zip(current_landmarks, stored_landmarks):
        total_distance += euclidean_distance(c_landmark, s_landmark)

    avg_distance = total_distance / len(current_landmarks)
    return avg_distance

# Fungsi untuk mendeteksi pose dan membandingkannya dengan beberapa file JSON
def detect_and_compare_pose(folder_name):
    # Daftar untuk menyimpan landmarks dari semua file JSON di folder
    json_files = [f for f in os.listdir(folder_name) if f.endswith('.json')]
    stored_landmarks_dict = {}

    # Membaca semua file JSON
    for json_file in json_files:
        file_path = os.path.join(folder_name, json_file)
        stored_landmarks_dict[json_file] = read_landmarks_from_json(file_path)

    cap = cv2.VideoCapture(0)

    # Menetapkan window dengan ukuran lebih besar
    cv2.namedWindow("Pose Estimation", cv2.WINDOW_NORMAL)  # Membuat window yang bisa diubah ukurannya
    cv2.resizeWindow("Pose Estimation", 900, 700)  # Menyesuaikan ukuran window

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                )

                current_landmarks = []
                for landmark in results.pose_landmarks.landmark:
                    current_landmarks.append([landmark.x, landmark.y, landmark.z])

                # Perbandingan dengan setiap file JSON
                similarity_scores = {}
                for json_file, stored_landmarks in stored_landmarks_dict.items():
                    similarity_score = calculate_similarity(current_landmarks, stored_landmarks)
                    similarity_scores[json_file] = similarity_score

                # Menampilkan hasil perbandingan dengan file JSON tertentu
                min_similarity_score = min(similarity_scores.values())
                best_match_file = [k for k, v in similarity_scores.items() if v == min_similarity_score][0]

                # Extract huruf (misalnya 'A') dari nama file (contoh: 'semaphore_pose_A.json')
                match_letter = re.search(r'_(\w)\.json', best_match_file)
                if match_letter:
                    match_letter = match_letter.group(1)  # Ambil huruf yang ditemukan

                threshold = 0.2
                font_scale = 0.7  # Mengubah ukuran font
                thickness = 1  # Ketebalan teks
                if min_similarity_score < threshold:
                    message = f"Pose {match_letter}!"  # Tampilkan hanya huruf
                else:
                    message = f"Best Similarity: {min_similarity_score:.2f}"

                # Menambahkan kotak hitam di pojok kiri bawah untuk latar belakang teks
                text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
                text_width, text_height = text_size

                # Menentukan posisi kotak latar belakang (pada pojok kiri bawah)
                x1, y1 = 20, frame.shape[0] - 50  # Posisi kiri bawah
                x2, y2 = x1 + text_width + 20, y1 - text_height - 10  # Menghitung lebar kotak sesuai teks

                # Menggambar kotak hitam
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), -1)  # Menggambar kotak hitam

                # Menampilkan teks di dalam kotak hitam
                cv2.putText(image, message, (x1 + 10, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)

            cv2.imshow('Pose Estimation', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

# Menjalankan deteksi dan perbandingan pose dengan semua file JSON di folder
folder_name = "semaphore_poses"
detect_and_compare_pose(folder_name)
