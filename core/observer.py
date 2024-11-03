# Убедись, что библиотека watchdog установлена:
# pip install watchdog

import threading
import functools
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from time import sleep


def observe(path='.'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Определяем обработчик событий
            class Handler(FileSystemEventHandler):
                def on_created(self, event):
                    if not event.is_directory:
                        # Если нужно, можем игнорировать временные файлы
                        if not event.src_path.endswith('.tmp'):
                            func(event.src_path)
                def on_moved(self, event):
                    if not event.is_directory:
                        # Обрабатываем переименование временного файла в финальный
                        func(event.dest_path)
            # Создаем наблюдателя
            observer = Observer()
            handler = Handler()
            observer.schedule(handler, path=path, recursive=True)
            # Запускаем наблюдателя в отдельном потоке
            observer_thread = threading.Thread(target=observer.start)
            observer_thread.daemon = True
            observer_thread.start()
            try:
                while True:
                    sleep(1)  # Уменьшил время сна для более быстрой реакции на прерывание
            except KeyboardInterrupt:
                observer.stop()
            observer.join()
        return wrapper
    return decorator



def is_file_downloaded(file_path, wait_time=5):
    """
    Проверяет, завершено ли скачивание файла.

    :param file_path: Путь к файлу для проверки.
    :param wait_time: Время ожидания в секундах для проверки изменений.
    :return: True, если файл полностью скачан, False в противном случае.
    """
    if not os.path.exists(file_path):
        return False

    initial_size = os.path.getsize(file_path)
    initial_mtime = os.path.getmtime(file_path)
    time.sleep(wait_time)
    current_size = os.path.getsize(file_path)
    current_mtime = os.path.getmtime(file_path)

    if initial_size == current_size and initial_mtime == current_mtime:
        return True
    else:
        return False
