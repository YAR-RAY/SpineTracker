from ui_notification.background_worker import NotificationManager
from ui_notification.background_worker import qt_app
from tracker.camera import TrackWorker
import sys
if __name__ == "__main__":
    ui_manager = NotificationManager()
    
    ai_thread = TrackWorker()
    
    ai_thread.trigger_warning_signal.connect(ui_manager.trigger_warning)
    ai_thread.start()
    
    sys.exit(qt_app.exec())