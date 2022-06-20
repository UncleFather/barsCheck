import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime as dt


# Процедура проверки доступности хоста пингом
def ping_check(hostname):
    # Проверяем доступность с 3-х попыток, время задержки 4000 мс
    response = os.system("ping -n 4 -w 4000 " + hostname)
    # Если ответ получен, возвращаем «True», иначе - «False»
    return True if response == 0 else False


# Устанавливаем константы с учетными данными
username = "username"
password = "password"
# Прописываем ip-адрес МИС «Барс»
bars_address = '10.31.6.59'
# Инициализируем драйвер Google Chrome
driver = webdriver.Chrome("chromedriver")
# Формируем начало сообщения для записи в файл журнала
message = f'{"".join(["-" for i in range(60)])}\n{dt.now():%d.%m.%Y %H:%M:%S}\n'
# Объявляем переменную для записи продолжения сообщения
result = ''

# Пытаемся открыть страницу с Барсом, войти и выйти
try:
    # Устанавливаем размер окна браузера
    driver.set_window_size(1561, 1060)
    # Переходим на страницу входа на сайт
    driver.get(f'http://{bars_address}/inst')

    # Парсим страничку входа. Находим поле для ввода имени пользователя и записываем в него имя
    driver.find_element(By.NAME, "DBLogin").find_element(By.CLASS_NAME, "input-ctrl").send_keys(username)
    # Находим поле для ввода пароля и записываем в него пароль
    driver.find_element(By.NAME, "DBPassword").find_element(By.CLASS_NAME, "input-ctrl").send_keys(password)
    # Находим кнопку отправки и нажимаем ее
    driver.find_element(By.CLASS_NAME, "bt").click()

    # Ждем 3 секунды
    sleep(3)
    # Подтверждаем организацию и кабинет (находим кнопку и кликаем по ней)
    driver.find_element(By.CLASS_NAME, "bt").click()

    # Ждем 3 секунды
    sleep(3)
    # Находим кнопку выхода и нажимаем ее
    driver.find_element(By.CLASS_NAME, "Exit").click()

    # Ждем 3 секунды
    sleep(3)
    # Если все прошло успешно, фомируем вторую часть сообщения
    result = 'МИС «Барс» доступна'

# При появлении любой ошибки обрабатываем ее
except Exception as my_error:
    # Выполняем пинг до сервера Барса и фомируем вторую часть сообщения
    result = f'Проблемы с МИС «Барс» (Проверка пингом прошла {"" if ping_check(bars_address) else "без"}успешно):\n{my_error}'

# Закрываем окно экземпляра браузера
driver.close()

# Открываем файл для записи результатов проверки
handler = open('bars_log.txt', 'a', encoding='utf8')
# Записываем сообщение в файл
handler.write(f'{message}{result}')
# Закрываем файл
handler.close()