import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

import ui_notification.configs.config_ai_assistant as chat_config
from ai_assistant.client import health_care_assistant
class ChatWindow(QWidget):
    chat_counter = 0
    def __init__(self, problem_type="общая усталость"):
        super().__init__()
        self.problem_type = problem_type

        self.raw_initial_greeting = ''
        self.is_first_message = True
        ChatWindow.chat_counter += 1
        self.current_session_id = f"{self.problem_type}_session_{ChatWindow.chat_counter}"

        self.setObjectName("ChatWindow")
        self.setWindowTitle("ИИ-Эргономист")
        self.setStyleSheet(chat_config.CHAT_STYLE_SHEET)
        self.setFixedSize(chat_config.CHAT_WIDTH, chat_config.CHAT_HEIGHT)

        screen = QApplication.primaryScreen()
        screen_geo = screen.geometry()
        
        chat_x = screen_geo.width() - chat_config.CHAT_WIDTH - 20
        chat_y = screen_geo.height() - chat_config.CHAT_HEIGHT - 50 
        self.move(chat_x, chat_y)
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        self.header_label = QLabel("Ваш персональный ИИ-Эргономист")
        self.header_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #0E639C;")
        main_layout.addWidget(self.header_label)
        
        self.history_area = QTextEdit()
        self.history_area.setObjectName("HistoryArea")
        self.history_area.setReadOnly(True)
        main_layout.addWidget(self.history_area)
        
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        self.input_field = QLineEdit()
        self.input_field.setObjectName("InputField")
        self.input_field.setPlaceholderText("Задайте вопрос ИИ-доктору...")
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_button = QPushButton("Отправить")
        self.send_button.setObjectName("SendButton")
        self.send_button.setFixedSize(85, 30)
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)
        
        self.setLayout(main_layout)
        

        self.generate_initial_greeting()

    def generate_initial_greeting(self):
        prob = str(self.problem_type).strip().lower()
        greetings = {
            "slouch": "Привет! Я зафиксировал, что ты начал сутулиться. \nЭто сильно пережимает сосуды шеи. Давай сделаем простое упражнение: отведи плечи максимально назад, сведи лопатки и подержи 5 секунд. Сделай глубокий вдох. \n\nЧем я могу тебе помочь?",
            "monitor": "Внимание! Ты сидишь слишком близко к монитору. \nТвои глаза сейчас испытывают большую нагрузку. Пожалуйста, отодвинься назад на расстояние вытянутой руки. \n\nХочешь, подберу технику расслабления глазных мыш?",
            "eyes_dry": "Я заметил, что твои глаза пересыхают, ты моргаешь слишком редко. \nПожалуйста, зажмурься сильно-сильно на 3 секунды, а затем быстро-быстро поморгай в течение 10 секунд. Это восстановит слезную пленку.\n\nЗадай мне любой вопрос по эргономике!",
            "eyes_closed": "Ого, твои глаза были закрыты подозрительно долго. Высокий уровень усталости! \nНастоятельно рекомендую встать из-за стола, сделать глоток воды и посмотреть в окно на самую дальнюю точку в течение полуминуты.\n\nНужна разминка для восстановления сил?",
            "eyes_frequent": "Твои глаза начали судорожно часто моргать — это явный признак спазма аккомодации (усталости глазных мышц). \nПрикрой глаза ладонями так, чтобы не проникал свет (палминг), и посиди в темноте 30 секунд, расслабив лицо.\n\nСпроси меня, как правильно настроить яркость монитора!"
        }
        text = greetings.get(prob, "Привет! Я твой ИИ-помощник по эргономике. Готов подсказать упражнения для спины и глаз. Что тебя интересует?")
        self.raw_initial_greeting = text
        self.history_area.append(f"<b>ИИ-эргономист:</b> {text}<br>")
        


    def send_message(self):
        user_text = self.input_field.text().strip()
        if not user_text:
            return 
            
        
        self.history_area.append(f"<b>Вы:</b> {user_text}")
        self.input_field.clear() 
        
    
        self.history_area.append("<i><b>ИИ-эргономист:</b> Хм, дайте подумать...</i>")
        QApplication.processEvents() 
        if self.is_first_message:
            full_prompt = (
                f"Контекст: Ты только что поприветствовал пользователя сообщением: '{self.raw_initial_greeting}'. "
                f"Пользователь отвечает тебе на это приветствие следующей фразой: '{user_text}'"
            )
            ai_response = health_care_assistant(full_prompt, session_id=self.current_session_id)
            self.is_first_message = False
        else:
            ai_response = health_care_assistant(user_text, session_id=self.current_session_id)
        cursor = self.history_area.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.select(cursor.SelectionType.LineUnderCursor)
        cursor.removeSelectedText()
        
        self.history_area.append(f"<b>ИИ-эргономист:</b> {ai_response}<br>")
        
        self.history_area.ensureCursorVisible()
