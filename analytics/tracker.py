import os
import csv
from datetime import datetime
import psutil

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stats.csv")

def log_event(event_type, comment=""):
    file_exists = os.path.exists(CSV_PATH)
    try:
        cpu_usage = psutil.cpu_percent(interval=None)
        
        process = psutil.Process(os.getpid())
        ram_usage_mb = process.memory_info().rss / (1024 * 1024)
        
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else "AC Power" 
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            
            if not file_exists:
                writer.writerow([
                    "Дата", "Время", "Тип События", "Комментарий", 
                    "Нагрузка CPU (%)", "Память RAM (МБ)", "Заряд батареи (%)"
                ])
            
            writer.writerow([
                date_str, time_str, event_type, comment, 
                f"{cpu_usage:.1f}", f"{ram_usage_mb:.1f}", battery_percent
            ])
            
        print(f"[АНАЛИТИКА] Событие '{event_type}' успешно записано в stats.csv (RAM: {ram_usage_mb:.1f}MB)")
        
    except Exception as e:
        print(f"[АНАЛИТИКА-ОШИБКА] Не удалось записать лог: {e}")
