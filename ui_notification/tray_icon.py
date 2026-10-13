from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction

from ui_notification.background_worker import qt_app
from ui_notification.settings_window import open_settings_window

TRAY_EXIT_TEXT = "Выход из ИИ-Эргономиста"
TRAY_SETTINGS_TEXT = "Настройки приложения"
TRAY_TOOLTIP_TEXT = "ИИ-Эргономист: Мониторинг осанки активен"


class TrayIcon(QSystemTrayIcon):
    def __init__(self, qt_app, parent=None):
        super().__init__(qt_app)

        self.tray_menu = QMenu()

        self.exit_action = QAction(TRAY_EXIT_TEXT, self.tray_menu)
        self.exit_action.triggered.connect(qt_app.quit)
        self.tray_menu.addAction(self.exit_action)
        self.tray_menu.addSeparator()
        self.settings_action = QAction(TRAY_SETTINGS_TEXT, self.tray_menu)
        self.settings_action.triggered.connect(lambda: open_settings_window(qt_app))
        self.tray_menu.addAction(self.settings_action)
        
        self.setContextMenu(self.tray_menu)
        
        self.setIcon(get_standard_tray_icon())
        self.setToolTip(TRAY_TOOLTIP_TEXT)

        self.show()
        
def get_standard_tray_icon():
    current_style = QApplication.style()
    return current_style.standardIcon(current_style.StandardPixmap.SP_ComputerIcon)