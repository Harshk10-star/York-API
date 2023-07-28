import json
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://www.yorku.ca/foodservices/dining-directory/")
    count = 0
    blocks = driver.find_elements(By.CLASS_NAME, 'wp-block-group__inner-container')
    print(len(blocks))
    blocks = blocks[4:]
    blocks = blocks[0:2] + blocks[4:]
    blocks = blocks[:16]
    blocks = blocks[0:5] + blocks[6:7] + blocks[8:]
    # lol weird ahh code

    short_form = ['BRG', 'CSQ', 'CFT', 'DB', 'LAS', 'OSG', 'SC', 'WSC', 'WC', 'FSC', 'SCS', 'SD', 'YLM', 'Q']
    curr = 0
    food = {}
    for p in blocks:
        name = p.find_element(By.TAG_NAME, 'h4').text

        try:
            index = name.index('(')
            name = name[:index]
        except ValueError:
            print(" ")

        short = short_form[curr]
        food[short_form[curr]] = []
        curr += 1
        places = p.find_elements(By.TAG_NAME, 'tr')
        count = 0

        for tr in places:
            count = 0
            place, monThurs, friday, saturday, sunday, menu = '', '', '', '', '', ''
            for td in tr.find_elements(By.TAG_NAME, 'td'):
                if count == 0:
                    place = td.text
                    if not place:
                        break
                elif count == 1:
                    monThurs = td.text
                elif count == 2:
                    friday = td.text
                elif count == 3:
                    saturday = td.text
                else:
                    menu = td.text

                count += 1
            if place:
                obj = {
                    "name": place,
                    "Monday-Thursday": monThurs,
                    "Friday": friday,
                    "Saturday": saturday,
                    "Menu_offering": menu
                }
                food[short].append(obj)

    with open("food.json", "w") as json_file:
        json.dump(food, json_file, indent=4)
