import sys

from ui_notification.background_worker import qt_app
from ui_notification.background_worker import NotificationManager
from tracker.camera import TrackWorker
from ui_notification.tray_icon import TrayIcon
from ui_notification.welcome_window import WelcomeWindow



if __name__ == "__main__":
    ui_manager = NotificationManager()
    qt_app.setQuitOnLastWindowClosed(False)
    
    qt_app.tray_icon = TrayIcon(qt_app)

    qt_app.welcome = WelcomeWindow()
    qt_app.welcome.show()
            
    ai_thread = TrackWorker()
    ai_thread.trigger_warning_signal.connect(ui_manager.trigger_warning)
    ai_thread.start()
    status_code = qt_app.exec()
    ai_thread.requestInterruption()
    ai_thread.wait()
    sys.exit(status_code)