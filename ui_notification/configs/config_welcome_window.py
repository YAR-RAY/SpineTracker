WELCOME_WINDOW_WIDTH = 400   
WELCOME_WINDOW_HEIGHT = 240 
        
WINDOW_DURATION = 10000

STYLE_SHEET = """
    QWidget#MainWidget {
        background-color: #1E1E1E;
        border: 2px solid #0E639C;
        border-radius: 12px;
    }
    QLabel {
        color: #FFFFFF;
        border: none;
    }
    QLabel#TitleText {
        font-size: 18px;
        font-weight: bold; 
        color: #33A1FF;
        background: none;
    }
    QLabel#DescriptionText {
        font-size: 13px; 
        line-height: 1.4; 
        background: none;
    }
    QPushButton#CloseButton {
        background-color = transparent;
        color = #888888;
        font-size: 18px;
        font-weight: normal;
        border: none;
        border-radius: 4px;
        padding-bottom: 2px;
    }
    QPushButton#CloseButton: hover {
        background-color = #E81123;
        color: #FFFFFF;
    }
"""
