from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication, QPushButton
from PyQt6.QtCore import Qt, QTimer


WELCOME_WINDOW_WIDTH = 400   
WELCOME_WINDOW_HEIGHT = 240 
        
WINDOW_DURATION = 10000

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ИИ-Эргономист: Старт")
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.CustomizeWindowHint | 
            Qt.WindowType.WindowCloseButtonHint
        )
        self.setFixedSize(WELCOME_WINDOW_WIDTH, WELCOME_WINDOW_HEIGHT)
        
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("WelcomeWindow")
        self.main_widget.setFixedSize(WELCOME_WINDOW_WIDTH, WELCOME_WINDOW_HEIGHT)
                
        
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 15, 20)
        layout.setSpacing(10)

                
        title = QLabel("ИИ-Эргономист запущен!")
        title.setProperty("class", "heading")

        desc = QLabel(
            "Система компьютерного зрения начала скрытный\n"
            "мониторинг вашей осанки и состояния глаз.\n\n"
            "Если вы ссутулитесь — появится ИИ-помощник.\n"
            "Программа работает полностью в фоновом режиме.\n\n"
            "Управление и Выход доступны в системном трее\n"
            "    (в правом нижнем углу экрана возле часов)."
        )
        desc.setProperty("class", "description")

        
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(desc)
        self.setLayout(layout)


        
        QTimer.singleShot(WINDOW_DURATION, self.close)