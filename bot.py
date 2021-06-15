import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyperclip
import pyautogui
import datetime

chromedriver_linux = '/usr/bin/chromedriver'
chromedriver_window = 'C:\\Users\\Lorca\\AppData\\Local\\Google\\Chrome\\chromedriver.exe'

usr = 'lorcaphan@gmail.com'
pwd = 'Longphan0612'

user_links = []

def format_number(string_number):

    return int(string_number.replace('.',''))


def format_date():

    today = datetime.datetime.now()

    return str(today.strftime("%d/%m"))


def get_statistics(website):

    response = requests.get(website)
    soup = BeautifulSoup(response.content, "html.parser")

    vietnam = soup.findAll('div', class_='UvMayb')

    total_cases = vietnam[0]
    total_deaths = vietnam[1]
    total_vaccines = vietnam[2]
    total_vaccinated = vietnam[3]

    statistics = soup.findAll('td', class_='l3HOY')

    case_per_1m = format_number(string_number=statistics[8].text)
    infect_probability = case_per_1m/1e6

    deaths = format_number(string_number=total_deaths.text)
    cases = format_number(string_number=total_cases.text)
    death_probability = deaths/cases

    today = soup.findAll('div', class_='tIUMlb')

    cases_today = today[0].text
    death_today = today[1].text

    extract_cases = cases_today.find('+') 
    cases_today = cases_today[extract_cases:]

    extract_death = death_today.find('+') 
    death_today = death_today[extract_death:]

    # print("Total cases: {}".format(total_cases.text))
    # print("Total deaths: {}".format(total_deaths.text))
    # print("Total vaccines: {}".format(total_vaccines.text))
    # print("Total vaccinated: {}".format(total_vaccinated.text))
    # print("New cases today: {}".format(cases_today))
    # print("Death today: {}".format(death_today))
    # print("Chance of infected: {}%".format(infect_probability))
    # print("Chance of death: {}%".format(death_probability))

    information = [total_cases.text, total_deaths.text, total_vaccines.text, total_vaccinated.text, cases_today, death_today, infect_probability, death_probability]

    return information


def send_message(info, date):

    driver = webdriver.Chrome(chromedriver_linux)

    driver.get("https://www.messenger.com/login/")

    sleep(2)

    username = driver.find_element_by_id('email')
    username.send_keys(usr)

    password = driver.find_element_by_id('pass')
    password.send_keys(pwd)

    login = driver.find_element_by_id('loginbutton')
    login.click()

    for user_link in user_links:

        sleep(2)
        
        driver.get(user_link)

        sleep(2)

        message_box = driver.find_element_by_css_selector(".notranslate")
        message_box.click()

        pyperclip.copy("--------[Tin nhắn tự động]--------\nCập nhật tình hình diễn biến dịch bệnh COVID-19 hôm nay ({date})\n\nSố ca nhiễm hôm nay: {case_today}\nSố ca tử vong hôm nay: {death_today}\n\nTổng ca nhiễm: {total_cases}\nTổng ca tử vong: {total_deaths}\nTổng lượng vaccine hiện tại: {total_vaccines}\nSố lượng người đã tiêm vaccine: {total_vaccinated}\nTỉ lệ lây nhiễm: {infect_probability}%\nTỉ lệ tử vong: {death_probability}%\n\nChi tiết tham khảo thêm tại: {link}".format(
            date=date, total_cases = info[0], total_deaths = info[1], total_vaccines = info[2], total_vaccinated = info[3], case_today = info[4], death_today = info[5], infect_probability = info[6], death_probability = info[7], link='https://news.google.com/covid19/map?hl=vi&mid=%2Fm%2F01crd5&gl=VN&ceid=VN%3Avi'))

        pyautogui.hotkey('ctrl', 'v')

        pyautogui.press('enter')


today = format_date()

info = get_statistics(website="https://news.google.com/covid19/map?hl=vi&mid=%2Fm%2F01crd5&gl=VN&ceid=VN%3Avi")

send_message(info=info, date=today)
