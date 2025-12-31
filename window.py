from datetime import datetime, date
import pyautogui
import time
from clickhouse_driver import Client

try:
    client = Client(
        host='192.168.56.10',
        port=9000,
        user='admin',
        password='admin',
        database='default'
    )
    print("Подключение к ClickHouse успешно")

    # Создание таблицы
    client.execute('''
    CREATE TABLE IF NOT EXISTS activity_log
    (
        log_date Date,
        active_window String,
        time_spent String
    )
    ENGINE = MergeTree
    PARTITION BY toYYYYMM(log_date)
    ORDER BY (log_date, active_window)
    SETTINGS index_granularity = 8192
    ''')
    print("Таблица activity_log создана/проверена")

except Exception as e:
    print(f"Ошибка подключения/создания таблицы: {e}")
    exit(1)

win = pyautogui.getActiveWindow()
window_start_time = datetime.now()
print("Трекер запущен.")

try:
    while True:
        try:
            active_window = pyautogui.getActiveWindow()

            if active_window and win:
                if win.title != active_window.title:
                    time_spent = datetime.now() - window_start_time

                    previous_title = win.title if win.title else ""
                    app_name = previous_title.strip() or "Рабочий стол"


                    current_date = datetime.now().date()


                    total_seconds = time_spent.total_seconds()
                    hours = int(total_seconds // 3600)
                    minutes = int((total_seconds % 3600) // 60)
                    seconds = int(total_seconds % 60)
                    time_spent_str = f"{hours}:{minutes:02d}:{seconds:02d}"


                    try:
                        client.execute(
                            "INSERT INTO activity_log VALUES",
                            [(current_date, app_name, time_spent_str)]
                        )
                        print(f"{current_date},{app_name},{time_spent_str}")
                    except Exception as db_error:
                        print(f"Ошибка записи в БД: {db_error}")

                    win = active_window
                    window_start_time = datetime.now()

            time.sleep(1)

        except Exception as e:
            print(f"Ошибка в цикле: {e}")
            time.sleep(1)


except Exception as e:
    print(f"Критическая ошибка: {e}")
finally:
    client.disconnect()
    print("Соединение закрыто")