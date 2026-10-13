from ui_notification.background_worker import NotificationManager
from ui_notification.background_worker import qt_app
from tracker.camera import TrackWorker
from ui_notification.tray_icon import TrayIcon
import ui_notification.configs.config_theme as config_theme
import sys

from ui_notification.welcome_window import WelcomeWindow

if __name__ == "__main__":
    ui_manager = NotificationManager()
    qt_app.setQuitOnLastWindowClosed(False)
    initial_theme = config_theme.load_user_theme()
    start_style = config_theme.DARK_THEME_STYLE if initial_theme == "dark" else config_theme.LIGHT_THEME_STYLE
    qt_app.setStyleSheet(start_style)
    welcome = WelcomeWindow()
    welcome.show()
    tray_icon = TrayIcon(qt_app)


    ai_thread = TrackWorker()
    ai_thread.trigger_warning_signal.connect(ui_manager.trigger_warning)
    ai_thread.start()
    status_code = qt_app.exec()
    ai_thread.requestInterruption()
    ai_thread.wait() 
    sys.exit(status_code)