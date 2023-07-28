import json
import time


from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import redis

# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    driver = webdriver.Chrome()
    driver.get("https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm")

    goSubject = driver.find_element(By.CSS_SELECTOR,
                                    "body > p > table > tbody > tr:nth-child(2) > td.bodytext > table > tbody > tr:nth-child(3) > td > a")
    goSubject.click()



    # only working with Kelee Campus

    campus = driver.find_element(By.CSS_SELECTOR, "#campusSelect > option:nth-child(3)")
    campus.click()


    press = driver.find_element(By.CSS_SELECTOR,
                                "body > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > form > table > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=submit]")

    dic = {}
    select_subject = Select(driver.find_element(By.CSS_SELECTOR, "#subjectSelect"))
    options = select_subject.options.copy()
    for value in range(155):
        time.sleep(10)
        select_subject.select_by_value(str(value))
        selected_subject = select_subject.first_selected_option.text

        press.click()

        count = 0

        table_locator = (By.CSS_SELECTOR,
                         "body > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(2) "
                         "> td > table > tbody > tr > td > table:nth-child(3) > tbody")
        try:
            table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(table_locator))
        except TimeoutException:
            # Break the loop if the element is not visible within the specified time
            driver.back()
            select_subject = Select(driver.find_element(By.CSS_SELECTOR, "#subjectSelect"))
            press = driver.find_element(By.CSS_SELECTOR,
                                        "body > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > form > table > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=submit]")
            continue

        for tr in table.find_elements(By.TAG_NAME, "tr"):
            # first tr is not needed
            if count == 0:
                count = 1
                continue
            arr = []
            for td in tr.find_elements(By.TAG_NAME, "td"):
                if count == 3:
                    count = 1
                    break
                arr.append(td.text)
                count += 1
            v1, v2 = arr
            temp = v1.split()
            subject_fac = temp[0].split("/")
            createObj = {
                "faculty": subject_fac[0],
                "subject": subject_fac[1],
                "title": v2,
                "course_code": temp[1],
                "course_cerdit": temp[2]
            }
            if subject_fac[1] not in dic:
                dic[subject_fac[1]] = [createObj]
            else:
                dic[subject_fac[1]].append(createObj)

        driver.back()
        wait = WebDriverWait(driver, 10)
        select_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#subjectSelect")))
        select_subject = Select(select_element)
        press = driver.find_element(By.CSS_SELECTOR,
                                    "body > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > form > table > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=submit]")

    faculties = ['SB', 'GS', 'AP', 'FA', 'SC', 'GL', 'ED', 'EU', 'LE', 'HH']
    driver.quit()

    sb = []
    gs = []
    ap = []
    fa = []
    sc = []
    gl = []
    ed = []
    eu = []
    le = []
    hh = []

    obj = {"faculties": {}}

    for subject in dic:
        for course in dic[subject]:
            fac = course.get("faculty")
            if fac == 'SB':
                sb.append(course)
            elif fac == 'GS':
                gs.append(course)
            elif fac == 'AP':
                ap.append(course)
            elif fac == 'FA':
                fa.append(course)
            elif fac == 'SC':
                sc.append(course)
            elif fac == 'AP':
                ap.append(course)
            elif fac == 'GL':
                gl.append(course)
            elif fac == 'ED':
                ed.append(course)
            elif fac == 'EU':
                eu.append(course)
            elif fac == 'LE':
                le.append(course)
            else:
                hh.append(course)

    # initialize
    for fac in faculties:
        obj["faculties"][fac] = {}

    # AP faculity
    for c in ap:
        sub = c.get("subject")
        key = c.get("title")
        if obj["faculties"]["AP"].get(sub) is None:
            obj["faculties"]["AP"][sub] = {}
            obj["faculties"]["AP"][sub]["name"] = sub
            obj["faculties"]["AP"][sub]["courses"] = []

        obj["faculties"]["AP"][sub]["courses"].append(c)

    # SB faculity
    for c in sb:
        sub = c.get("subject")
        key = c.get("title")
        if obj["faculties"]["SB"].get(sub) is None:
            obj["faculties"]["SB"][sub] = {}
            obj["faculties"]["SB"][sub]["name"] = sub
            obj["faculties"]["SB"][sub]["courses"] = []
        obj["faculties"]["SB"][sub]["courses"].append(c)

    # GS faculity
    for c in gs:
        sub = c.get("subject")
        key = c.get("title")
        if obj["faculties"]["GS"].get(sub) is None:
            obj["faculties"]["GS"][sub] = {}
            obj["faculties"]["GS"][sub]["name"] = sub
            obj["faculties"]["GS"][sub]["courses"] = []
        obj["faculties"]["GS"][sub]["courses"].append(c)
    # FA faculity
    for c in fa:
        sub = c.get("subject")
        key = c.get("title")
        if obj["faculties"]["FA"].get(sub) is None:
            obj["faculties"]["FA"][sub] = {}
            obj["faculties"]["FA"][sub]["name"] = sub
            obj["faculties"]["FA"][sub]["courses"] = []
        obj["faculties"]["FA"][sub]["courses"].append(c)
    # SC faculity
    for c in sc:
        sub = c.get("subject")
        key = c.get("title")
        if obj["faculties"]["SC"].get(sub) is None:
            obj["faculties"]["SC"][sub] = {}
            obj["faculties"]["SC"][sub]["name"] = sub
            obj["faculties"]["SC"][sub]["courses"] = []
        obj["faculties"]["SC"][sub]["courses"].append(c)
    # GL faculity
    for c in gl:
        sub = c.get("subject")
        key = c.get("title")
        if obj["faculties"]["GL"].get(sub) is None:
            obj["faculties"]["GL"][sub] = {}
            obj["faculties"]["GL"][sub]["name"] = sub
            obj["faculties"]["GL"][sub]["courses"] = []
        obj["faculties"]["GL"][sub]["courses"].append(c)
    # ED faculity
    for c in ed:
        sub = c.get("subject")
        key = c.get("title")
        if obj["faculties"]["ED"].get(sub) is None:
            obj["faculties"]["ED"][sub] = {}
            obj["faculties"]["ED"][sub]["name"] = sub
            obj["faculties"]["ED"][sub]["courses"] = []
        obj["faculties"]["ED"][sub]["courses"].append(c)
    # EU faculity
    for c in eu:
        sub = c.get("subject")
        key = c.get("title")
        if obj["faculties"]["EU"].get(sub) is None:
            obj["faculties"]["EU"][sub] = {}
            obj["faculties"]["EU"][sub]["name"] = sub
            obj["faculties"]["EU"][sub]["courses"] = []
        obj["faculties"]["EU"][sub]["courses"].append(c)
    # LE faculity
    for c in le:
        sub = c.get("subject")
        key = c.get("title")
        if obj["faculties"]["LE"].get(sub) is None:
            obj["faculties"]["LE"][sub] = {}
            obj["faculties"]["LE"][sub]["name"] = sub
            obj["faculties"]["LE"][sub]["courses"] = []
        obj["faculties"]["LE"][sub]["courses"].append(c)
    # HH faculity
    for c in hh:
        sub = c.get("subject")
        key = c.get("title")
        if obj["faculties"]["HH"].get(sub) is None:
            obj["faculties"]["HH"][sub] = {}
            obj["faculties"]["HH"][sub]["name"] = sub
            obj["faculties"]["HH"][sub]["courses"] = []
        obj["faculties"]["HH"][sub]["courses"].append(c)


    with open("courses.json", "w") as json_file:
        json.dump(obj, json_file, indent=4)
