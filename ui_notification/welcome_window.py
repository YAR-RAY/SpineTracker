from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication, QPushButton
from PyQt6.QtCore import Qt, QTimer

import ui_notification.configs.config_welcome_window as ww_config

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ИИ-Эргономист: Старт")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setFixedSize(ww_config.WELCOME_WINDOW_WIDTH, ww_config.WELCOME_WINDOW_HEIGHT)
        self.setStyleSheet(ww_config.STYLE_SHEET)
        
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("MainWidget")
        self.main_widget.setStyleSheet(ww_config.STYLE_SHEET)
        self.main_widget.setFixedSize(ww_config.WELCOME_WINDOW_WIDTH, ww_config.WELCOME_WINDOW_HEIGHT)
                
        
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 15, 20)
        layout.setSpacing(10)

        top_layout = QHBoxLayout()
                
        title = QLabel("ИИ-Эргономист запущен!")
        title.setObjectName("TitleText")
        title.setStyleSheet(ww_config.STYLE_SHEET)
        
        desc = QLabel(
            "Система компьютерного зрения начала скрытный\n"
            "мониторинг вашей осанки и состояния глаз.\n\n"
            "Если вы ссутулитесь — появится ИИ-помощник.\n"
            "Программа работает полностью в фоновом режиме.\n\n"
            "Управление и Выход доступны в системном трее\n"
            "    (в правом нижнем углу экрана возле часов)."
        )
        desc.setObjectName("DescriptionText")
        desc.setStyleSheet(ww_config.STYLE_SHEET)

        self.close_button = QPushButton('x')
        self.close_button.setObjectName("CloseButton")
        self.close_button.setFixedSize(24, 24)
        self.close_button.clicked.connect(self.close)
        
        top_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop) 
        

        layout.addLayout(top_layout)
        layout.addWidget(desc)


        
        QTimer.singleShot(ww_config.WINDOW_DURATION, self.close)