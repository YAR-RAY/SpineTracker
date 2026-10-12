import sys
from PyQt6.QtWidgets import QApplication
from ui_notification.overlay import NotificationOverlay
from ui_notification.chat_window import ChatWindow
qt_app = QApplication.instance() or QApplication(sys.argv)

class NotificationManager:
    def __init__(self):
        self.active_notification = None
        self.active_chat = None 
        self.last_warning_type = "general" 

    def trigger_warning(self, warning_type):
        if self.active_notification and self.active_notification.isVisible():
            return
        if self.active_chat and self.active_chat.isVisible():
            return
        if warning_type == "monitor":
            title = "Слишком близко к монитору!"
            message = "Вы сильно наклонились вперед. Это создает опасное напряжение для глаз. Нажмите для консультации с ИИ."
        elif warning_type == "slouch":
            title = "Нарушение осанки!"
            message = "Ваша спина согнута. Портиться осанка. Нажмите, чтобы размяться."
        elif warning_type == "eyes_dry":
            title = "Поморгайте! Сухость глаз"
            message = "ИИ заметил, что вы моргаете слишком редко. Ваши глаза пересыхают. Нажмите, чтобы сделать разминку."
        elif warning_type == "eyes_closed":
            title = "Высокая усталость глаз!"
            message = "Ваши глаза были закрыты слишком долго. Сделайте короткий перерыв. Нажмите, чтобы ИИ подобрал упражнение."
        elif warning_type == "eyes_frequent":
            title = "Переутомление глаз! Частое моргание"
            message = "Вы моргаете слишком часто. Это признак сильного утомления глазных мышц. Нажмите, ИИ подскажет технику расслабления."
        else:
            return 

        self.active_notification = NotificationOverlay(
            title=title,
            message=message,
            click_callback=lambda: self.open_chat_for_problem(warning_type)
        )
        self.active_notification.show_animated()
    def open_chat_for_problem(self, problem_type):
        self.active_chat = ChatWindow(problem_type=problem_type)
        self.active_chat.show()

    def _on_notification_clicked(self):
        self.active_chat = ChatWindow(problem_type=self.last_warning_type)
        self.active_chat.show()
