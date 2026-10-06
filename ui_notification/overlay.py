import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt6.QtGui import QScreen

import ui_notification.config as ui_config

# Создаем класс окна уведомления, который наследуется от базового QWidget (окна PyQt)
class NotificationOverlay(QWidget):
    def __init__(self, title, message, click_callback=None):
        super().__init__()
        self.click_callback = click_callback # Запоминаем функцию, которую надо запустить при клике
        
        # 1. СИСТЕМНЫЕ ФЛАГИ ОКНА (Магия прозрачности и фокуса)
        # FramelessWindowHint — убирает рамку Windows, кнопки закрыть/свернуть
        # WindowStaysOnTopHint — заставляет окно всплывать ПОВЕРХ всех игр, браузеров и VS Code
        # Tool — прячет иконку приложения с панели задач Windows, чтобы не мусорить
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.WindowStaysOnTopHint | 
                            Qt.WindowType.Tool)
        
        # Делаем так, чтобы клики мыши по углам прозрачной области не блокировали рабочий стол
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(ui_config.NOTIFICATION_WIDTH, ui_config.NOTIFICATION_HEIGHT)
        
        # Применяем дизайн-стили из нашего конфигуратора
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("MainWidget")
        self.main_widget.setStyleSheet(ui_config.STYLE_SHEET)
        self.main_widget.setFixedSize(ui_config.NOTIFICATION_WIDTH, ui_config.NOTIFICATION_HEIGHT)
        

        widget_layout = QVBoxLayout(self.main_widget)
        widget_layout.setContentsMargins(12, 10, 12, 10)
        widget_layout.setSpacing(6)

        top_layout = QHBoxLayout()


        self.title_label = QLabel(title)
        if "близко" in title.lower() or "монитор" in title.lower():
            self.title_label.setObjectName("MonitorTitle") # Будет красным
        elif "глаз" in title.lower() or "сухость" in title.lower():
            self.title_label.setObjectName("EyesTitle")
        elif "переутомление" in title.lower() or "часто" in title.lower():
            self.title_label.setObjectName("EyesFatigueTitle")
        else:
            self.title_label.setObjectName("SlouchTitle")  # Будет оранжевым

        self.close_button = QPushButton('x')
        self.close_button.setObjectName("CloseButton")
        self.close_button.setFixedSize(24, 24)
        self.close_button.clicked.connect(self.close)

        top_layout.addWidget(self.title_label)
        top_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop) 

        self.separator = QFrame()
        self.separator.setObjectName("Separator")

        self.msg_label = QLabel(message)
        self.msg_label.setObjectName("Message")
        self.msg_label.setWordWrap(True)

        widget_layout.addLayout(top_layout)
        widget_layout.addWidget(self.separator)
        widget_layout.addWidget(self.msg_label)

        
        # 3. ГЕОМЕТРИЯ: Расчет правого нижнего угла экрана
        screen = QApplication.primaryScreen() # Получаем доступ к главному монитору ноутбука
        screen_geo = screen.geometry()        # Достаем его разрешение (например, 1920x1080)
        
        # Вычисляем конечную точку, где карточка застынет (с отступом 20 пикселей от правого и нижнего края)
        self.end_x = screen_geo.width() - ui_config.NOTIFICATION_WIDTH - 20
        self.end_y = screen_geo.height() - ui_config.NOTIFICATION_HEIGHT - 50
        self.start_y = screen_geo.height() + 100
        
        self.move(self.end_x, self.start_y) # Перемещаем окно в скрытую стартовую позицию
        
        # 4. АНИМАЦИЯ И ТАЙМЕРЫ
        # Настраиваем анимацию плавного изменения позиции окна (свойства "pos")
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(ui_config.ANIMATION_DURATION) # Берем скорость из конфига (0.3 сек)
        self.anim.setStartValue(QPoint(self.end_x, self.start_y)) # Откуда выезжать
        self.anim.setEndValue(QPoint(self.end_x, self.end_y))     # Где остановиться
        
        # Создаем таймер автоскрытия. Когда карточка постоит на экране, она должна исчезнуть
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True) # Таймер должен сработать строго 1 раз
        self.hide_timer.timeout.connect(self.close) # По истечении времени вызываем системное закрытие окна

    def show_animated(self):
        """Функция для запуска показа карточки с анимацией"""
        self.show() # Показываем окно в системе
        self.anim.start() # Включаем анимацию выезда вверх
        self.hide_timer.start(ui_config.DISPLAY_TIME) # Запускаем отсчет 7 секунд до автоскрытия

    def mousePressEvent(self, event):
        """Встроенная функция PyQt, которая отслеживает клик мыши по окну"""
        if event.button() == Qt.MouseButton.LeftButton: # Если пользователь кликнул левой кнопкой мыши
            self.close() # Немедленно закрываем карточку предупреждения
            if self.click_callback:
                self.click_callback() # Если мы передали функцию открытия ИИ-ассистента — запускаем её!
