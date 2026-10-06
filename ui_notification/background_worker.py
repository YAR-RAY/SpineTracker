import sys
from PyQt6.QtWidgets import QApplication
from ui_notification.overlay import NotificationOverlay

qt_app = QApplication.instance() or QApplication(sys.argv)

class NotificationManager:
    def __init__(self):
        self.active_notification = None

    def trigger_warning(self, warning_type):
        """
        Универсальный триггер для ИИ. 
        """
        # Если карточка уже на экране — не спамим
        if self.active_notification and self.active_notification.isVisible():
            return
            
        # Формируем текст в зависимости от сигнала ИИ-движка
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
            return # Если пришел неизвестный тип — ничего не делаем

        # Создаем и запускаем PyQt6 оверлей
        self.active_notification = NotificationOverlay(
            title=title,
            message=message,
            click_callback=self._on_notification_clicked
        )
        self.active_notification.show_animated()

    def _on_notification_clicked(self):
        print("Клик зафиксирован! Закрываем карточку и открываем окно ИИ-Ассистента (Модуль 3)...")
