CHAT_WIDTH = 420
CHAT_HEIGHT = 550

CHAT_STYLE_SHEET = """
    QWidget#ChatWindow {
        background-color: #1E1E1E;
        color: #F1F1F1;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    QLabel {
        background-color: transparent;
        color: #F1F1F1;
    }
    
    QTextEdit#HistoryArea {
        background-color: #252526;
        color: #D4D4D4;
        border: 1px solid #3F3F46;
        border-radius: 8px;
        padding: 10px;
        font-size: 13px;
        line-height: 18px;
    }
    
    QLineEdit#InputField {
        background-color: #2D2D30;
        color: #FFFFFF;
        border: 1px solid #3F3F46;
        border-radius: 6px;
        padding: 8px;
        font-size: 13px;
    }
    QLineEdit#InputField:focus {
        border: 1px solid #007ACC; /* Синяя подсветка при клике на поле ввода */
    }
    
    QPushButton#SendButton {
        background-color: #0E639C; /* Синий цвет */
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        font-size: 13px;
    }
    QPushButton#SendButton:hover {
        background-color: #1177BB; /* Подсветка при наведении */
    }
    QPushButton#SendButton:pressed {
        background-color: #005B94; /* Потемнение при клике */
    }
"""
