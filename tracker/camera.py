import cv2
import time
from PyQt6.QtCore import QThread, pyqtSignal
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mediapipe as mp

import tracker.config_points as config_p
import tracker.validators as validators

class TrackWorker(QThread):
    trigger_warning_signal = pyqtSignal(str)

    def run(self):
        base_face = python.BaseOptions(model_asset_path=config_p.FACE_MODEL_PATH)
        face_options = vision.FaceLandmarkerOptions(base_options=base_face, num_faces=1)
        face_detector = vision.FaceLandmarker.create_from_options(face_options)

        base_pose = python.BaseOptions(model_asset_path=config_p.POSE_MODEL_PATH)
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
        last_face_time = 0.0
        last_pose_time = 0.0

        cap = cv2.VideoCapture(0)

        while cap.isOpened() and not self.isInterruptionRequested():
            success, frame = cap.read()
            if not success: 
                break
            current_time = time.time()

            if current_time - last_face_time < config_p.FACE_INTERVAL:
                time.sleep(0.01)
                continue
            last_face_time = current_time

            frame = cv2.resize(frame, (640, 480))
            h_img, w_img, _ = frame.shape
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            face_result = face_detector.detect(mp_image)
            pose_result = pose_detector.detect(mp_image)

            if current_time - last_pose_time >= config_p.POSE_INTERVAL:
                pose_result = pose_detector.detect(mp_image)
                last_pose_time = current_time
            else:
                pose_result = None

            if pose_result and pose_result.pose_landmarks and len(pose_result.pose_landmarks) > 0:
                if base_shoulder_distance is None:
                    _, _, cur_sh, cur_nk = validators.check_posture(pose_result, None, None, config_p)
                    calibration_shoulders.append(cur_sh)
                    calibration_necks.append(cur_nk)
                    calibration_frames += 1
                    
                    if calibration_frames >= 30:
                        base_shoulder_distance = sum(calibration_shoulders) / len(calibration_shoulders)
                        base_neck_distance = sum(calibration_necks) / len(calibration_necks)
                else:
                    
                    is_leaning, is_slouching, _, _ = validators.check_posture(pose_result, base_shoulder_distance, base_neck_distance, config_p)
                    if is_leaning:
                        self.trigger_warning_signal.emit("monitor") 
                    elif is_slouching:
                        self.trigger_warning_signal.emit("slouch") 

            
            if face_result and face_result.face_landmarks and len(face_result.face_landmarks) > 0:
                actual_face_landmarks = face_result.face_landmarks[0]
                landmarks = [(int(lm.x * w_img), int(lm.y * h_img)) for lm in actual_face_landmarks]
                
                if len(landmarks) >= 400:
                    left_ear_val = validators.calculate_ear(landmarks, config_p.LEFT_EYE)
                    right_ear_val = validators.calculate_ear(landmarks, config_p.RIGHT_EYE)
                    avg_ear = (left_ear_val + right_ear_val) / 2.0
                    if avg_ear < config_p.EAR_THRESHOLD:
                        frame_counter += 1
                        if frame_counter >= 40:
                            self.trigger_warning_signal.emit("eyes_closed")
                    else:
                        if frame_counter >= config_p.BLINK_FRAME_CONSECUTIVE:
                            blink_counter += 1
                        frame_counter = 0
            
            if current_time - start_minute_timer >= 60:
                if blink_counter < 8:
                    self.trigger_warning_signal.emit('eyes_dry')
                elif blink_counter >= 30:
                    self.trigger_warning_signal.emit("eyes_frequent")
                blink_counter = 0
                start_minute_timer = current_time

        cap.release()
