import math
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QTimer

DOT_SIZE = 24              
DOT_COLOR = "#33A1FF"      
DOT_SPEED = 5          

TRAJECTORY_MODE = ["vertical", "horizontal", "infinity", "circle"]
TIME_PER_EXERCISE_SEC = 10
RELAX_DURATION_SEC = len(TRAJECTORY_MODE) * TIME_PER_EXERCISE_SEC

RADIUS_X_RATIO = 0.35      
RADIUS_Y_RATIO = 0.25     
    
ANIMATION_TICK_MS = 40   

class RelaxWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setObjectName("Background")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        
        self.setStyleSheet("background-color: #1E1E1E;")

        
        screen_geo = QApplication.primaryScreen().geometry()
        self.setFixedSize(screen_geo.width(), screen_geo.height())

        self.center_x = screen_geo.width() // 2
        self.center_y = screen_geo.height() // 2
        
        self.radius_x = int(screen_geo.width() * RADIUS_X_RATIO)
        self.radius_y = int(screen_geo.height() * RADIUS_Y_RATIO)
        
        self.angle = 0.0
        self.time_left = RELAX_DURATION_SEC

        self.exercises = TRAJECTORY_MODE 
        self.exercise_index = 0                      
        self.exercise_timer_sec = 0
        
        self.dot = QWidget(self)
        self.dot.setObjectName("EyeDot")
        self.dot.setStyleSheet(f"""
            QWidget#EyeDot {{
                background-color: {DOT_COLOR}; 
                border-radius: {DOT_SIZE // 2}px;
            }}
        """)
        self.dot.setFixedSize(DOT_SIZE, DOT_SIZE)
        
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.animate_dot)
        self.anim_timer.start(ANIMATION_TICK_MS)
        
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)
        
        self.animate_dot()
        
        self.showFullScreen()

    def animate_dot(self):
        trajectory = self.exercises[self.exercise_index]    
        self.angle += (DOT_SPEED / 100.0)
        x = self.center_x
        y = self.center_y
        if trajectory == "vertical":
            x = self.center_x
            y = self.center_y + int(1.5 * self.radius_y * math.sin(2 * self.angle))
        elif trajectory == "horizontal":
            x = self.center_x + int(self.radius_x * math.cos(self.angle))
            y = self.center_y
        elif trajectory == "infinity":
            x = self.center_x + int(self.radius_x * math.sin(self.angle))
            y = self.center_y + int(self.radius_y * math.sin(2*self.angle)/2)                    
        elif trajectory == "circle":
            x = self.center_x + int(self.radius_x * math.cos(self.angle))
            y = self.center_y + int(self.radius_y * math.sin(self.angle))
        
        self.dot.move(x - DOT_SIZE // 2, y - DOT_SIZE // 2)

    def update_countdown(self):
        self.time_left -= 1
        self.exercise_timer_sec += 1
        
        if self.exercise_timer_sec >= TIME_PER_EXERCISE_SEC:
            self.exercise_timer_sec = 0 
            self.exercise_index += 1            
        if self.time_left <= 0 or self.exercise_index >= len(self.exercises):
            self.stop_all_timers_and_close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.stop_all_timers_and_close()

    def stop_all_timers_and_close(self):
        self.anim_timer.stop()
        self.countdown_timer.stop()
        self.close()

_relax_window_instance = None

def open_relax_window():
    global _relax_window_instance
    if _relax_window_instance is not None and _relax_window_instance.isVisible():
        return
        
    _relax_window_instance = RelaxWindow()
    _relax_window_instance.showFullScreen()
    _relax_window_instance.raise_()
    _relax_window_instance.activateWindow()
