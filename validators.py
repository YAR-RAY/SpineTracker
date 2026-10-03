import numpy as np

def calculate_ear(landmarks, eye_config):
    idx_v1_top, idx_v1_bot = eye_config["v1"]
    idx_v2_top, idx_v2_bot = eye_config["v2"]
    idx_h_left, idx_h_right = eye_config["h"]
    
    p_v1_top = np.array(landmarks[idx_v1_top])
    p_v1_bot = np.array(landmarks[idx_v1_bot])
    p_v2_top = np.array(landmarks[idx_v2_top])
    p_v2_bot = np.array(landmarks[idx_v2_bot])
    p_h_left = np.array(landmarks[idx_h_left])
    p_h_right = np.array(landmarks[idx_h_right])
    
    dist_v1 = np.linalg.norm(p_v1_top - p_v1_bot)
    dist_v2 = np.linalg.norm(p_v2_top - p_v2_bot)
    dist_h = np.linalg.norm(p_h_left - p_h_right)
    return (dist_v1 + dist_v2) / (2.0 * dist_h)

def check_posture(pose_result, base_shoulder_dist, base_neck_dist, config):
    """
    Тот самый рабочий код без тригонометрии, но с автоматическим порогом.
    """
    points_list = pose_result.pose_landmarks[0]
    
    left_ear = points_list[7]
    left_shoulder = points_list[11]
    right_shoulder = points_list[12]
    
    # 1. Расстояние плеч
    p1 = np.array([left_shoulder.x, left_shoulder.y])
    p2 = np.array([right_shoulder.x, right_shoulder.y])
    current_shoulder_dist = np.linalg.norm(p1 - p2)
    
    is_leaning = False
    if base_shoulder_dist and current_shoulder_dist > base_shoulder_dist * config.SHOULDER_DIST_LIMIT_RATIO:
        is_leaning = True
        
    # 2. Текущее сжатие шеи (расстояние по вертикали Y)
    current_neck_dist = left_shoulder.y - left_ear.y
    
    is_slouching = False
    if base_neck_dist:
        # Если расстояние ухо-плечо уменьшилось на 20% от вашего нормального состояния
        if current_neck_dist < base_neck_dist * 0.80:
            is_slouching = True
            
    return is_leaning, is_slouching, current_shoulder_dist, current_neck_dist
