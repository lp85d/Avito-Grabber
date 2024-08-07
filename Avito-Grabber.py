import requests
from bs4 import BeautifulSoup
import customtkinter
import threading
import socket
from loguru import logger
import time  # Import time module for delay

customtkinter.set_appearance_mode("dark")

class AvitoLinkParser(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Установим размер окна и его заголовок
        self.geometry("800x500")  # Increased height to accommodate additional input field
        self.title("AvitoLinkParser")
        
        # Заблокируем возможность изменения размера окна
        self.resizable(False, False)

        # Инициализация переменных
        self.is_run = False
        self.parse_thread = None
        self.original_getaddrinfo = socket.getaddrinfo  # Сохранить оригинальную функцию getaddrinfo
        self.init_ui()

        # Центрируем окно относительно экрана
        self.center_window()

    def init_ui(self):
        """Инициализация всех полей"""
        
        # Метка и поле ввода для URL
        self.url_label = customtkinter.CTkLabel(self, text="Url:")
        self.url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.url_entry = customtkinter.CTkEntry(self, width=500, placeholder_text="Адрес для парсинга")
        self.url_entry.grid(row=0, column=1, pady=5, sticky='w')
        self.url_entry.insert(0, "https://www.avito.ru/moskva/bytovaya_tehnika/dlya_doma/stiralnye_i_sushilnye_mashiny-ASgBAgICAkRgpE_OB6ZP")

        # Метка и поле ввода для количества страниц
        self.pages_label = customtkinter.CTkLabel(self, text="Количество страниц:")
        self.pages_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.pages_entry = customtkinter.CTkEntry(self, width=500, placeholder_text="Сколько страниц проверять")
        self.pages_entry.grid(row=1, column=1, pady=5, sticky='w')
        self.pages_entry.insert(0, "1")  # Установим значение по умолчанию для количества страниц

        # Метка и поле ввода для задержки между запросами
        self.delay_label = customtkinter.CTkLabel(self, text="Задержка (сек):")
        self.delay_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.delay_entry = customtkinter.CTkEntry(self, width=500, placeholder_text="Задержка между запросами в секундах")
        self.delay_entry.grid(row=2, column=1, pady=5, sticky='w')
        self.delay_entry.insert(0, "1")  # Установим значение по умолчанию для задержки

        # Кнопка "Старт"
        self.start_button = customtkinter.CTkButton(self, text="Старт", command=self.start_parsing)
        self.start_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Кнопка "Стоп"
        self.stop_button = customtkinter.CTkButton(self, text="Стоп", command=self.stop_parsing)
        self.stop_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.stop_button.grid_forget()

        # Виджет для логирования
        self.log_widget = customtkinter.CTkTextbox(self, wrap="word", width=750, height=200, text_color="#00ff26")
        self.log_widget.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Добавление обработчика для логирования в виджет
        logger.add(self.logger_text_widget, format="{time:HH:mm:ss} - {message}")

    def logger_text_widget(self, message):
        """Логирование в log_widget (окно приложения)"""
        self.log_widget.insert("end", message + "\n")
        self.log_widget.see("end")

    def start_parsing(self):
        """Запуск парсинга"""
        self.is_run = True
        self.switch_buttons()
        threading.Thread(target=self.run_parse).start()

    def stop_parsing(self):
        """Остановка парсинга"""
        self.is_run = False

    def switch_buttons(self):
        """Смена видимости кнопок старт и стоп"""
        if self.is_run:
            self.start_button.grid_forget()
            self.stop_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        else:
            self.stop_button.grid_forget()
            self.start_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    def run_parse(self):
        """Основной цикл парсинга"""
        url = self.url_entry.get()
        try:
            pages = int(self.pages_entry.get() or 1)
        except ValueError:
            logger.error("Некорректное значение количества страниц, установлено значение по умолчанию 1")
            pages = 1

        try:
            delay = float(self.delay_entry.get() or 1)
        except ValueError:
            logger.error("Некорректное значение задержки, установлено значение по умолчанию 1 секунда")
            delay = 1.0

        links = self.get_avito_links(url, pages, delay)
        self.save_links_to_file(links)
        logger.info(f"Сохранено {len(links)} ссылок в файл avito_links.txt")
        self.is_run = False
        self.switch_buttons()

    def get_avito_links(self, url, pages, delay):
        """Сбор ссылок с Avito"""
        links = []
        for page in range(1, pages + 1):
            if not self.is_run:
                break  # Прерываем парсинг если он был остановлен

            response = requests.get(f"{url}?p={page}")
            if response.status_code != 200:
                logger.error(f"Ошибка: Не удалось получить доступ к странице {page}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('a', {'data-marker': 'item-title'})
            for item in items:
                link = 'https://www.avito.ru' + item.get('href')
                links.append(link)

            logger.info(f"Обработана страница {page}, задержка {delay} секунд перед следующей страницей.")
            time.sleep(delay)  # Задержка перед запросом следующей страницы

        return links

    def save_links_to_file(self, links, filename='avito_links.txt'):
        """Сохранение ссылок в файл"""
        with open(filename, 'w') as file:
            for link in links:
                file.write(f"{link}\n")
    
    def center_window(self):
        """Центрируем окно относительно экрана"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 800
        window_height = 500
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

if __name__ == '__main__':
    AvitoLinkParser().mainloop()
