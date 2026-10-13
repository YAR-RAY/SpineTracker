from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint

NOTIFICATION_WIDTH = 340   
NOTIFICATION_HEIGHT = 110 
ANIMATION_DURATION = 300   
DISPLAY_TIME = 6000

class NotificationOverlay(QWidget):
    def __init__(self, title, message, click_callback=None):
        super().__init__()
        self.click_callback = click_callback 
        
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.CustomizeWindowHint | 
            Qt.WindowType.WindowCloseButtonHint
        )
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(NOTIFICATION_WIDTH, NOTIFICATION_HEIGHT)
        
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("NotificationWindow")
        self.main_widget.setFixedSize(NOTIFICATION_WIDTH, NOTIFICATION_HEIGHT)
        

        widget_layout = QVBoxLayout(self.main_widget)
        widget_layout.setContentsMargins(12, 10, 12, 10)
        widget_layout.setSpacing(6)

        top_layout = QHBoxLayout()


        self.title_label = QLabel(title)
        self.title_label.setProperty("class", "heading")
        if "близко" in title.lower() or "монитор" in title.lower():
            self.title_label.setObjectName("MonitorTitle") 
        elif "глаз" in title.lower() or "сухость" in title.lower():
            self.title_label.setObjectName("EyesTitle")
        elif "переутомление" in title.lower() or "часто" in title.lower():
            self.title_label.setObjectName("EyesFatigueTitle")
        else:
            self.title_label.setObjectName("SlouchTitle")  

        top_layout.addWidget(self.title_label)
        
        self.separator = QFrame()
        self.separator.setObjectName("Separator")

        self.msg_label = QLabel(message)
        self.msg_label.setProperty("class", "description")
        self.msg_label.setObjectName("Message")
        self.msg_label.setWordWrap(True)

        widget_layout.addLayout(top_layout)
        widget_layout.addWidget(self.separator)
        widget_layout.addWidget(self.msg_label)

        
        
        screen = QApplication.primaryScreen() 
        screen_geo = screen.geometry()        
        
        
        self.end_x = screen_geo.width() - NOTIFICATION_WIDTH - 20
        self.end_y = screen_geo.height() - NOTIFICATION_HEIGHT - 50
        self.start_y = screen_geo.height() + 100
        
        self.move(self.end_x, self.start_y)
        
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(ANIMATION_DURATION) 
        self.anim.setStartValue(QPoint(self.end_x, self.start_y)) 
        self.anim.setEndValue(QPoint(self.end_x, self.end_y))     
        
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.close)

    def show_animated(self):
        self.show() 
        self.anim.start() 
        self.hide_timer.start(DISPLAY_TIME) 

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.close() 
            if self.click_callback:
                self.click_callback()
