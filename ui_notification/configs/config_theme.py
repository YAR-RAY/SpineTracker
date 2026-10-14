import os
import json

SETTINGS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
    "user_settings.json"
)

DARK_THEME_STYLE = """
    QWidget#ChatWindow, QWidget#SettingsWindow, QWidget#WelcomeWindow, QWidget#NotificationWindow {
        background-color: #1E1E1E;
        color: #FFFFFF;
        font-family: 'Segoe UI', Arial;
    }
    
    QLabel { 
        font-family: 'Segoe UI', Arial;
        color: #FFFFFF; 
    }
    
    QLabel[class="heading"] { 
        font-size: 18px; 
        font-weight: bold; 
        color: #33A1FF; 
    }
    QLabel[class="description"] { 
        font-size: 13px; 
        line-height: 1.4; 
        color: #E0E0E0; 
    }
    
    QTextEdit, QLineEdit {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border: 1px solid #3F3F3F;
        border-radius: 6px;
        padding: 6px;
        font-size: 13px;
    }
    
    QPushButton {
        background-color: #2D2D2D;      
        color: #FFFFFF;
        border: 1px solid #3F3F3F;
        border-radius: 4px;
        padding: 5px 12px;
        font-family: 'Segoe UI', Arial;
        font-weight: bold;
    }
    QPushButton:hover { 
        background-color: #0E639C;      
        border: 1px solid #1177BB;
    }
    #InfoBlock { color: #888888; }
    #SettingsSeparator { background-color: #3F3F3F; }
"""

LIGHT_THEME_STYLE = """
    QWidget#ChatWindow, QWidget#SettingsWindow, QWidget#WelcomeWindow, QWidget#NotificationWindow {
        background-color: #F3F3F3;
        color: #000000;
        font-family: 'Segoe UI', Arial;
    }
    
    QLabel { 
        font-family: 'Segoe UI', Arial;
        color: #000000; 
    }
    
    QLabel[class="heading"] { 
        font-size: 18px; 
        font-weight: bold; 
        color: #0E639C; 
    }
    QLabel[class="description"] { 
        font-size: 13px; 
        line-height: 1.4; 
        color: #333333; 
    }
    
    QTextEdit, QLineEdit {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #CCCCCC;
        border-radius: 6px;
        padding: 6px;
        font-size: 13px;
    }
    
    QPushButton {
        background-color: #E1E1E1;          
        color: #000000;
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        padding: 5px 12px;
        font-family: 'Segoe UI', Arial;
        font-weight: bold;
    }
    QPushButton:hover { 
        background-color: #0E639C;      
        color: #FFFFFF;
        border: 1px solid #1177BB;
    }
    #InfoBlock { color: #555555; }
    #SettingsSeparator { background-color: #CCCCCC; }
"""

def load_user_theme():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("theme", "dark")
        except:
            pass
    return "dark"

def save_user_theme(theme_name):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"theme": theme_name}, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[Ошибка сохранения настроек]: {e}")
