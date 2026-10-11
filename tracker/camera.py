import os
import sys
import cv2
import time
import urllib.request
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mediapipe as mp

import config
import validators
from ui_notification.background_worker import NotificationManager
from ui_notification.background_worker import qt_app

for name, url, path in [("Лицо", config.FACE_MODEL_URL, config.FACE_MODEL_PATH), 
                        ("Поза", config.POSE_MODEL_URL, config.POSE_MODEL_PATH)]:
    if not os.path.exists(path):
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, path)
        except Exception:
            exit()

class TrackWorker(QThread):
    trigger_warning_signal = pyqtSignal(str)

    def run(self):
        """Вся тяжелая математика MediaPipe и OpenCV выполняется здесь параллельно чату!"""
        base_face = python.BaseOptions(model_asset_path=config.FACE_MODEL_PATH)
        face_options = vision.FaceLandmarkerOptions(base_options=base_face, num_faces=1)
        face_detector = vision.FaceLandmarker.create_from_options(face_options)

        base_pose = python.BaseOptions(model_asset_path=config.POSE_MODEL_PATH)
        pose_options = vision.PoseLandmarkerOptions(base_options=base_pose, num_poses=1)
        pose_detector = vision.PoseLandmarker.create_from_options(pose_options)

        blink_counter = 0
        frame_counter = 0
        base_shoulder_distance = None
        base_neck_distance = None  
        calibration_frames = 0
        calibration_shoulders = []
        calibration_necks = []
        start_minute_timer = time.time()

        cap = cv2.VideoCapture(0)
        print("\n Фоновый поток ИИ запущен. Сядьте ровно...")

        while cap.isOpened() and not self.isInterruptionRequested():
            success, frame = cap.read()
            if not success: break
            
            frame = cv2.resize(frame, (640, 480))
            h_img, w_img, _ = frame.shape
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            face_result = face_detector.detect(mp_image)
            pose_result = pose_detector.detect(mp_image)
            
            status_text = "Status: Searching for user..."
            color = (128, 128, 128)
            
            # --- ЛОГИКА ОСАНКИ ---
            if pose_result and pose_result.pose_landmarks and len(pose_result.pose_landmarks) > 0:
                if base_shoulder_distance is None:
                    _, _, cur_sh, cur_nk = validators.check_posture(pose_result, None, None, config)
                    calibration_shoulders.append(cur_sh)
                    calibration_necks.append(cur_nk)
                    calibration_frames += 1
                    status_text = f"Calibrating... {int((calibration_frames/30)*100)}%"
                    color = (0, 255, 255)
                    
                    if calibration_frames >= 30:
                        base_shoulder_distance = sum(calibration_shoulders) / len(calibration_shoulders)
                        base_neck_distance = sum(calibration_necks) / len(calibration_necks)
                        print(f"Калибровка завершена!")
                else:
                    status_text = "Status: OK"
                    color = (0, 255, 0)
                    
                    is_leaning, is_slouching, _, _ = validators.check_posture(pose_result, base_shoulder_distance, base_neck_distance, config)
                    if is_leaning:
                        status_text = "Too close to monitor!"
                        color = (0, 0, 255)
                        self.trigger_warning_signal.emit("monitor") 
                    elif is_slouching:
                        status_text = "Don't slouch!"
                        color = (0, 165, 255)
                        self.trigger_warning_signal.emit("slouch") 

            
            if face_result and face_result.face_landmarks and len(face_result.face_landmarks) > 0:
                actual_face_landmarks = face_result.face_landmarks[0]
                landmarks = [(int(lm.x * w_img), int(lm.y * h_img)) for lm in actual_face_landmarks]
                
                if len(landmarks) >= 400:
                    left_ear_val = validators.calculate_ear(landmarks, config.LEFT_EYE)
                    right_ear_val = validators.calculate_ear(landmarks, config.RIGHT_EYE)
                    avg_ear = (left_ear_val + right_ear_val) / 2.0
                    cv2.putText(frame, f"EAR: {avg_ear:.3f}", (30, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    if avg_ear < config.EAR_THRESHOLD:
                        frame_counter += 1
                        if frame_counter >= 40:
                            self.trigger_warning_signal.emit("eyes_closed")
                    else:
                        if frame_counter >= config.BLINK_FRAME_CONSECUTIVE:
                            blink_counter += 1
                        frame_counter = 0
                        
                    cv2.putText(frame, f"Blinks: {blink_counter}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            current_time = time.time()
            if current_time - start_minute_timer >= 60:
                if blink_counter < 8:
                    self.trigger_warning_signal.emit('eyes_dry')
                elif blink_counter >= 30:
                    self.trigger_warning_signal.emit("eyes_frequent")
                blink_counter = 0
                start_minute_timer = current_time
                
            cv2.putText(frame, status_text, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.imshow('AI Ergonomist (Dev Mode)', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    ui_manager = NotificationManager()
    
    ai_thread = TrackWorker()
    
    ai_thread.trigger_warning_signal.connect(ui_manager.trigger_warning)
    ai_thread.start()
    
    sys.exit(qt_app.exec())
