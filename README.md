# Avito-Grabber
### Avito Grabber — это эффективный инструмент для автоматизированного сбора данных с сайта Avito

Avito Grabber — это эффективный инструмент для автоматизированного сбора данных с сайта Avito. Программа извлекает информацию с каждой ссылки с интервалом в 15 секунд, что обеспечивает аккуратный и безопасный процесс сборки. Идеальна для мониторинга цен, поиска товаров и анализа рынка. Удобный интерфейс и настройка параметров делают использование программы простым и интуитивно понятным.

Доступ ограничен: проблема с IP
Иногда такое случается — чтобы вернуться на сайт, нажмите кнопку «Отправить».
Что можно сделать, если проблема повторяется
— Отключить VPN.
— Перезагрузить роутер.
— Запустить проверку антивирусом.
Не сработает — напишите поддержке. Обязательно укажите свой город, провайдера и IP.
Что не так с IP
С него идёт очень много запросов — как если бы вы разом открывали десятки вкладок или слишком часто обновляли страницу.
Обычно такое бывает, когда одним IP пользуются несколько человек. Например, если ваш провайдер объединяет абонентов в подсети, вы открываете сайт с рабочего компьютера или пользуетесь VPN. Также причина может быть в расширениях браузера и вирусах.
### Soft.7z pip install pandas requests beautifulsoup4 loguru customtkinter gspread oauth2client
![image](https://github.com/user-attachments/assets/cf8c4aab-2f5b-4f6c-a075-53e1dddaac4d)
![image](https://github.com/user-attachments/assets/6719841c-c32f-4a52-a204-4d8e3f8a1a85)

### Новая версия [AvitoLinkParser.py](https://github.com/lp85d/Avito-Grabber/blob/main/AvitoLinkParser.7z)
![image](https://github.com/user-attachments/assets/7f114082-b743-4e96-9bde-f7d85418ed69)

### Изменения: [AvitoLinkParser_NEW.py](https://github.com/lp85d/Avito-Grabber/blob/main/AvitoLinkParser_NEW.7z)
Добавлена переменная retry_attempts, которая определяет количество попыток перезагрузки страницы, если на ней не найдено объявлений. 

Внутри цикла по страницам добавлен еще один цикл, который пытается повторить запрос страницы до двух раз с задержкой, указанной в переменной delay.

Если после всех попыток страницы все еще пусты, программа завершает парсинг этой страницы и переходит к следующей.

Теперь программа будет пытаться дважды перезагрузить страницу, если объявления не загрузились с первого раза.

### Компилируем exe
C:\Windows\System32>cd C:\Users\user\Desktop\Soft

C:\Users\user\Desktop\Soft>pyinstaller --onefile --add-data "avitolinkparser-f92b970c7daa.json;." AvitoLinkParser.py

44658 INFO: Building EXE from EXE-00.toc completed successfully.

### Create Project
https://console.cloud.google.com/apis/credentials?project

Create Project

Create credentials

Service account

Create and continue

Keys 

Add key 

Create new key 

JSON
