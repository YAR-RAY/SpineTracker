DOT_SIZE = 24              
DOT_COLOR ="#33A1FF"      
DOT_SPEED = 5          

TRAJECTORY_MODE = ["vertical", "horizontal", "infinity", "circle"]
TIME_PER_EXERCISE_SEC = 10
RELAX_DURATION_SEC = len(TRAJECTORY_MODE) * TIME_PER_EXERCISE_SEC

RADIUS_X_RATIO = 0.35      
RADIUS_Y_RATIO = 0.25     

RELAX_DURATION_SEC = 40    
ANIMATION_TICK_MS = 40     

WIDGET_STYLE = """
    QWidget#Background {
        background-color: rgba(20, 20, 20, 0.85); /* Полупрозрачный темный фон на весь экран */
    }
    QWidget#CenterBox {
        background-color: #2D2D30;
        border: 1px solid #3F3F46;
        border-radius: 16px;
    }
    QLabel {
        color: #FFFFFF;
        font-family: 'Segoe UI', Arial, sans-serif;
        background-color: transparent;
    }
    QPushButton {
        background-color: #3F3F46;
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #52525B;
    }
"""
