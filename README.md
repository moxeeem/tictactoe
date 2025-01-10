# 🎮 Бот для игры в крестики-нолики

![img](\img\cover.png)

## Описание проекта

![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white) ![python-telegram-bot-20.8](https://img.shields.io/badge/python--telegram--bot-20.8-3776AB?style=flat-square&logo=python&logoColor=white)

Этот проект представляет собой простейший бот для игры в крестики-нолики. Бот реализован при помощи библиотеки `python-telegram-bot`.

## Содержание

  - [Описание проекта](#описание-проекта)
  - [Содержание](#содержание)
  - [Структура репозитория](#структура-репозитория)
  - [Инструкция по запуску](#инструкция-по-запуску)
  - [Авторы](#авторы)
  - [Лицензия](#лицензия)

## Структура репозитория

- [/app](https://github.com/moxeeem/tictactoe/tree/main/app) : Файлы бота
- [/app/main.py](https://github.com/moxeeem/tictactoe/tree/main/app/main.py) : Основной файл для запуска бота
- [/app/tictactoe](https://github.com/moxeeem/tictactoe/tree/main/app/tictactoe) : Пакет с кодом игровой логики
- [requirements.txt](https://github.com/moxeeem/tictactoe/tree/main/requirements.txt) : Файл зависимостей
- [tests.py](https://github.com/moxeeem/tictactoe/tree/main/tests.py) : Файл с тестами основного функционала бота

## Инструкция по запуску

Примечание:

- Для запуска бота необходимо создать бота в Telegram и получить токен.
- Обратите внимание, что необходимо дать вашему боту разрешение на использование групповых чатов:
  - Откройте настройки вашего бота в BotFather
  - Найдите пункт "Allow Groups?"
  - Установите значение в "Enable"
  - Найдите пункт "Group Privacy"
  - Установите значение Privacy mode в "Disable"

1. Загрузите репозиторий.
2. Установите зависимости:

  ```bash
  pip install -r requirements.txt
  ```

3. Введите свой токен в файле `tictactoe/constants.py`:

  ```python
  os.environ["TOKEN"] = "ВАШ_ТОКЕН_ЗДЕСЬ"
  ```

4. Запустите бота:

  ```bash
  python app/main.py
  ```

5. Бот готов к работе! Важно помнить, что мультиплеер доступен только в групповых чатах, но вы можете играть с ИИ в личных сообщениях.

6. Запустите тесты:

  ```bash
  pytest tests.py
  ```

## Авторы

[![Максим Иванов](https://img.shields.io/badge/Максим_Иванов-GitHub-black?style=flat-square&logo=github&logoColor=white)](https://github.com/moxeeem)

Данный проект реализован в рамках курса "Python Advanced" от Академии Аналитиков Авито.

## Лицензия

Данный репозиторий лицензируется по лицензии MIT. Дополнительную информацию см. в файле [LICENSE](/LICENSE).
