import os
import sys
from datetime import datetime
from time import sleep
from typing import Tuple

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from PIL import Image


CALENDAR_URL = ""
CHROMEDRIVER_PATH = f"{os.getcwd()}/chromedriver"
SCREEN_FILENAME = sys.argv[1]
DATE_TARGET = sys.argv[2]


def open_calendar() -> WebDriver:
    """
    Открывает страницу с календарем через Selenium.

    :return: Драйвер Chrome, в котором был открыт календарь.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1080,920")
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

    driver.get(CALENDAR_URL)
    sleep(2.5)
    calendar_frame = driver.find_element_by_css_selector("iframe[scrolling='no']")
    driver.switch_to.frame(calendar_frame)

    return driver


def calculate_number_of_click_and_css_selector(date_target: str) -> (int, str):
    date_target = date_target.split('.')
    month_target, year_target = int(date_target[0]), int(date_target[1])
    month_now, year_now = datetime.now().month, datetime.now().year

    result = (year_target - year_now) * 12
    result -= month_now
    result += month_target

    if result > 0:
        return result, 'navForward1'
    elif result < 0:
        return -result, 'navBack1'
    return 0, ''


def flip_calendar(driver: WebDriver, num_of_click: int, id_of_button: str) -> None:
    """
    Перелистывает страницы календаря вперед (назад) столько раз, сколько нужно.

    :param driver: Драйвер Chrome, в котором был открыт календарь.
    :param num_of_click: Число перелистываний (кликов).
    :param id_of_button: ID CSS-элемента, один из ['navBack1', 'navForward1'].
    :return: None.
    """
    for _ in range(num_of_click):
        driver.find_element_by_id(id_of_button).click()
        sleep(0.1)
    sleep(2.5)


def crop_image(image_filename: str, coordinates: Tuple[int, int, int, int]) -> None:
    """
    Обрезает скриншот веб-страницы.
    Используется для того, чтобы на скриншоте было видно только календарь.

    :param image_filename: Имя файла скриншота.
    :param coordinates: Координаты обрезки в виде (x1, y1, x2, y2), где A(x1, y1) и B(x2, y2) - это
                        верхняя левая и нижняя права точка остаточного изображения соотвественно.
    :return: None.
    """
    image = Image.open(image_filename)
    cropped_image = image.crop(coordinates)
    cropped_image.save(image_filename, quality=100)


if __name__ == '__main__':
    # Example.
    chrome_driver = open_calendar()
    number_of_click, css_selector = calculate_number_of_click_and_css_selector(DATE_TARGET)
    if number_of_click:
        flip_calendar(chrome_driver, number_of_click, css_selector)
    chrome_driver.save_screenshot(SCREEN_FILENAME)
    chrome_driver.quit()

    crop_image(SCREEN_FILENAME, coordinates=(8, 93, 808, 657))
