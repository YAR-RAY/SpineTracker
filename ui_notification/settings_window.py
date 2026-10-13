from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QApplication
from PyQt6.QtCore import Qt
import ui_notification.configs.config_theme as config_theme

SETTINGS_WINDOW_TITLE = "ИИ-Эргономист: Настройки"

SETTINGS_WINDOW_WIDTH = 380
SETTINGS_WINDOW_HEIGHT = 260

class SettingsWindow(QWidget):
    def __init__(self, main_app_instance):
        super().__init__()
        self.main_app = main_app_instance

        self.setObjectName("SettingsWindow")
        self.setWindowTitle(SETTINGS_WINDOW_TITLE)
        self.setFixedSize(SETTINGS_WINDOW_WIDTH, SETTINGS_WINDOW_HEIGHT)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        
        self.current_theme = config_theme.load_user_theme()

        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        header_theme = QLabel("Тема оформления приложения")
        header_theme.setObjectName("HeaderTheme")
        main_layout.addWidget(header_theme)
        
        theme_layout = QHBoxLayout()
        theme_layout.setSpacing(10)
        
        self.btn_dark = QPushButton("Темная")
        self.btn_dark.clicked.connect(lambda: self.change_theme("dark"))
        theme_layout.addWidget(self.btn_dark)
        
        self.btn_light = QPushButton("Светлая")
        self.btn_light.clicked.connect(lambda: self.change_theme("light"))
        theme_layout.addWidget(self.btn_light)
        
        main_layout.addLayout(theme_layout)
        main_layout.addStretch()
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.close_button = QPushButton("ОК")
        self.close_button.setFixedSize(80, 30)
        self.close_button.clicked.connect(self.close)
        btn_layout.addWidget(self.close_button)
        
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
    def change_theme(self, theme_name):
        config_theme.save_user_theme(theme_name)
        
        style = config_theme.DARK_THEME_STYLE if theme_name == "dark" else config_theme.LIGHT_THEME_STYLE
        
        app = QApplication.instance()
        if app:
            app.setStyleSheet(style)
    
_settings_window_instance = None

def open_settings_window(main_app_instance):
    global _settings_window_instance
    if _settings_window_instance is not None and _settings_window_instance.isVisible():
        _settings_window_instance.raise_()
        _settings_window_instance.activateWindow()
        return
        
    _settings_window_instance = SettingsWindow(main_app_instance)
    _settings_window_instance.show()
