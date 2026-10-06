import sys
import time
from ui_notification.background_worker import NotificationManager, qt_app

manager = NotificationManager()

print(" Запуск симулятора всех уведомлений фонового модуля!")
qt_app.processEvents()
time.sleep(1)

# 1. Тестируем триггер СУТУЛОСТИ
print(" 1. Выезжает карточка СУТУЛОСТИ (Оранжевая)...")
manager.trigger_warning("slouch")
for _ in range(65): qt_app.processEvents(); time.sleep(0.1) # Даем карточке повисеть и исчезнуть

# 2. Тестируем триггер МОНИТОРА
print(" 2. Выезжает карточка БЛИЗОСТИ К МОНИТОРУ (Красная)...")
manager.trigger_warning("monitor")
for _ in range(65): qt_app.processEvents(); time.sleep(0.1)

# 3. Тестируем триггер СУХОСТИ ГЛАЗ
print(" 3. Выезжает карточка СУХОСТИ ГЛАЗ (Голубая)...")
manager.trigger_warning("eyes_dry")
for _ in range(65): qt_app.processEvents(); time.sleep(0.1)

# 4. Тестируем триггер МИКРОСНА
print("4. Выезжает карточка ЗАКРЫТЫХ ГЛАЗ (Синяя)...")
manager.trigger_warning("eyes_closed")
for _ in range(65): qt_app.processEvents(); time.sleep(0.1)

# 5. Тестируем триггер ГИПЕРМИГАНИЯ
print("5. Выезжает карточка ПЕРЕУТОМЛЕНИЯ ГЛАЗ (Фиолетовая)...")
manager.trigger_warning("eyes_frequent")

sys.exit(qt_app.exec())
