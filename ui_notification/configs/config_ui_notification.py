NOTIFICATION_WIDTH = 340   
NOTIFICATION_HEIGHT = 110 

ANIMATION_DURATION = 300   
DISPLAY_TIME = 6000        


STYLE_SHEET = """
    QWidget#MainWidget {
        background-color: #252526;
        border: 1px solid #3F3F46;
        border-radius: 12px;
    }
    QLabel {
        background-color: transparent;
        color: #F1F1F1;
    }
    QLabel#SlouchTitle {
        font-size: 16px;
        font-weight: bold;
        color: #FF9900; 
    }
    QLabel#MonitorTitle {
        font-size: 16px;
        font-weight: bold;
        color: #FF3333; 
    }
    QLabel#EyesTitle {
        font-size: 16px;
        font-weight: bold;
        color: #33A1FF; 
    }
    QLabel#EyesFatigueTitle {
            font-size: 16px;
            font-weight: bold;
            color: #33A1FF; 
        }
    QLabel#Message {
        font-size: 14px;
        color: #CCCCCC;
    }
    QFrameSeparator {
        background-color: #3F3F46
        max-height: 1px;
        border: none;
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
