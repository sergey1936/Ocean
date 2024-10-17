import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import telebot

# Замените на ваш токен бота
API_TOKEN = "YOUR_API_TOKEN"
bot = telebot.TeleBot(API_TOKEN)

# URL для проверки статуса ноды
NODE_STATUS_URL = 'https://nodes.oceanprotocol.com/'


def get_node_status(node_id):
    try:
        # Настройка и запуск браузера Chrome через Selenium
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Запуск в фоновом режиме
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Открытие страницы
        driver.get(NODE_STATUS_URL)
        time.sleep(2)  # Ожидание загрузки страницы

        # Поиск всех полей ввода и ввод значения в первое подходящее
        input_fields = driver.find_elements(By.TAG_NAME, 'input')  # Найти все поля ввода
        if not input_fields:
            driver.quit()
            return "Ошибка: Поле ввода не найдено"

        search_box = input_fields[0]  # Использовать первое поле ввода, проверьте правильность
        search_box.send_keys(node_id)

        # Поиск кнопки поиска и имитация нажатия
        search_button = driver.find_elements(By.XPATH, '//button[@aria-label="search"]')
        if not search_button:
            driver.quit()
            return "Ошибка: Кнопка поиска не найдена"

        search_button[0].click()
        time.sleep(2)  # Ожидание обновления результатов

        # Считывание всех элементов с классом 'MuiDataGrid-cell'
        status_elements = driver.find_elements(By.CLASS_NAME, 'MuiDataGrid-cell')
        if not status_elements:
            driver.quit()
            return "Ошибка: Статус не найден"

        # Попробуем найти элемент с нужными данными
        for element in status_elements:
            if element.get_attribute('data-field') == 'eligibilityCauseStr':
                status_text = element.text
                print(f"Статус ноды: {status_text}")  # Отладочное сообщение
                driver.quit()
                return status_text

        driver.quit()
        return "Ошибка: Статус не найден"
    except Exception as e:
        return f"Ошибка: {str(e)}"


@bot.message_handler(commands=['status'])
def send_node_status(message):
    node_id = 'YOUR_NODE_ID'  # Ваш Node ID
    status = get_node_status(node_id)
    bot.reply_to(message, f"Статус ноды: {status}")


bot.polling()









