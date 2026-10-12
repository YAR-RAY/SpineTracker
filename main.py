from ui_notification.background_worker import NotificationManager
from ui_notification.background_worker import qt_app
from tracker.camera import TrackWorker
import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction

if __name__ == "__main__":
    ui_manager = NotificationManager()
    tray_menu = QMenu()
    exit_action = QAction("Выход из ИИ-Эргономиста", tray_menu)
    exit_action.triggered.connect(qt_app.quit)
    tray_menu.addAction(exit_action)
    tray_icon = QSystemTrayIcon(qt_app)
    current_style = QApplication.style()
    standard_icon = current_style.standardIcon(current_style.StandardPixmap.SP_ComputerIcon)
    tray_icon.setIcon(standard_icon)
    tray_icon.setContextMenu(tray_menu)
    tray_icon.setToolTip("ИИ-Эргономист: Мониторинг осанки активен")
    tray_icon.show()


    ai_thread = TrackWorker()
    ai_thread.trigger_warning_signal.connect(ui_manager.trigger_warning)
    ai_thread.start()
    status_code = qt_app.exec()
    ai_thread.requestInterruption()
    ai_thread.wait() 
    sys.exit(status_code)