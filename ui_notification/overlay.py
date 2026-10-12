from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint

import ui_notification.configs.config_ui_notification as ui_config

class NotificationOverlay(QWidget):
    def __init__(self, title, message, click_callback=None):
        super().__init__()
        self.click_callback = click_callback 
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.Tool)
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(ui_config.NOTIFICATION_WIDTH, ui_config.NOTIFICATION_HEIGHT)
        
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("MainWidget")
        self.main_widget.setStyleSheet(ui_config.STYLE_SHEET)
        self.main_widget.setFixedSize(ui_config.NOTIFICATION_WIDTH, ui_config.NOTIFICATION_HEIGHT)
        

        widget_layout = QVBoxLayout(self.main_widget)
        widget_layout.setContentsMargins(12, 10, 12, 10)
        widget_layout.setSpacing(6)

        top_layout = QHBoxLayout()


        self.title_label = QLabel(title)
        if "близко" in title.lower() or "монитор" in title.lower():
            self.title_label.setObjectName("MonitorTitle") 
        elif "глаз" in title.lower() or "сухость" in title.lower():
            self.title_label.setObjectName("EyesTitle")
        elif "переутомление" in title.lower() or "часто" in title.lower():
            self.title_label.setObjectName("EyesFatigueTitle")
        else:
            self.title_label.setObjectName("SlouchTitle")  

        self.close_button = QPushButton('x')
        self.close_button.setObjectName("CloseButton")
        self.close_button.setFixedSize(24, 24)
        self.close_button.clicked.connect(self.close)

        top_layout.addWidget(self.title_label)
        top_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop) 

        self.separator = QFrame()
        self.separator.setObjectName("Separator")

        self.msg_label = QLabel(message)
        self.msg_label.setObjectName("Message")
        self.msg_label.setWordWrap(True)

        widget_layout.addLayout(top_layout)
        widget_layout.addWidget(self.separator)
        widget_layout.addWidget(self.msg_label)

        
        
        screen = QApplication.primaryScreen() 
        screen_geo = screen.geometry()        
        
        
        self.end_x = screen_geo.width() - ui_config.NOTIFICATION_WIDTH - 20
        self.end_y = screen_geo.height() - ui_config.NOTIFICATION_HEIGHT - 50
        self.start_y = screen_geo.height() + 100
        
        self.move(self.end_x, self.start_y)
        
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(ui_config.ANIMATION_DURATION) 
        self.anim.setStartValue(QPoint(self.end_x, self.start_y)) 
        self.anim.setEndValue(QPoint(self.end_x, self.end_y))     
        
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.close)

    def show_animated(self):
        self.show() 
        self.anim.start() 
        self.hide_timer.start(ui_config.DISPLAY_TIME) 

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.close() 
            if self.click_callback:
                self.click_callback()
