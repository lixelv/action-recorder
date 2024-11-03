import cv2
import numpy as np
import mss
import pyautogui
import time
import signal
import sys

# Параметры записи
def record(filename, fps, cursor_size=5):

    # Получаем размеры экрана
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Первый монитор (если их несколько)
        screen_width = monitor["width"]
        screen_height = monitor["height"]

    # Настраиваем видеокодек и создаём объект записи
    fourcc = cv2.VideoWriter_fourcc(*"XVID")  # Используем кодек XVID
    out = cv2.VideoWriter(filename, fourcc, fps, (screen_width, screen_height))

    def signal_handler(sig, frame):
        """Обработчик сигнала для корректного завершения записи."""
        print("\nЗавершение записи...")
        out.release()
        cv2.destroyAllWindows()
        sys.exit(0)

    # Назначаем обработчик для сигнала прерывания (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    print("Начало записи экрана. Нажмите Ctrl+C для завершения.")

    # Основной цикл записи
    with mss.mss() as sct:
        try:
            while True:
                start_time = time.time()

                # Захватываем экран
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # Получаем позицию курсора
                cursor_x, cursor_y = pyautogui.position()

                # Рисуем курсор на кадре
                cv2.circle(frame, (cursor_x, cursor_y), cursor_size, (0, 0, 255), -1)

                # Записываем кадр в видеофайл
                out.write(frame)

                # Рассчитываем время обработки кадра и корректируем задержку
                elapsed_time = time.time() - start_time
                delay = max(1.0 / fps - elapsed_time, 0)
                time.sleep(delay)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            # Освобождаем ресурсы
            out.release()
            cv2.destroyAllWindows()
            print(f"Запись экрана сохранена в файл '{filename}'")

if __name__ == "__main__":
    record("output.avi", 10)