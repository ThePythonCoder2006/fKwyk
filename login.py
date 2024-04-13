from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

import os
import traceback

fast_login = True

settings_path = "./setting.txt"


def get_pwd_usr():
    username = ""
    password = ""
    if fast_login:
        if os.path.isfile(settings_path):
            f = open(settings_path, "r")
            username = f.readline().replace("\n", "")
            password = f.readline().replace("\n", "")
            f.close()
        else:
            username, password = None, None
    else:
        username, password = None, None

    return username, password


def fast_log(driver: WebDriver, username: str, password: str, usernameField: WebElement, passwordField: WebElement):
    if username != None and password != None:
        usernameField.send_keys(username)
        passwordField.send_keys(password + Keys.ENTER)
        username, password = None, None

    driver.implicitly_wait(0)
    while len(driver.find_elements(By.CSS_SELECTOR, "#bouton_valider")) == 1:
        try:
            username = usernameField.get_attribute("value")
            password = passwordField.get_attribute("value")
        except:
            break

        if fast_login:
            f = open(settings_path, "w")
            f.write(username + "\n")
            f.write(password + "\n")
            f.close()
    driver.implicitly_wait(4)


def login(driver: WebDriver, wait: WebDriverWait):
    username, password = get_pwd_usr()

    valid = False
    while not valid:
        try:
            driver.find_element(By.CSS_SELECTOR, "a.fo-connect__link")\
                .click()  # se connecter

            # eleve / parent educ nat
            driver.find_element(By.CSS_SELECTOR, "label[for=idp-EDU]").click()
            driver.find_element(By.CSS_SELECTOR, "#button-submit").click()

            driver.find_element(By.CSS_SELECTOR, "#bouton_eleve")\
                .click()  # eleve

            usernameField: WebElement = driver.find_element(
                By.CSS_SELECTOR, "#username")
            passwordField: WebElement = driver.find_element(
                By.CSS_SELECTOR, "#password")
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print(
                "quelque chose d'innatendu est arrivé, merci de ne pas interférer avec le programme")
            traceback.print_exception(e)
            ans = input(
                "appuies sur <enter> quand tu est pres pour que le programme réessaie de se connecter")
            if ans == 'q':
                break
            valid = False
        else:
            break

    print("connecte toi sur Mon Bureau Numérique")
    if fast_login:
        fast_log(driver,
                 username, password, usernameField, passwordField)
    else:
        input("appuies sur <enter> quand tu as entrer ton MDP")

        try:
            driver.find_element(By.CSS_SELECTOR, "#bouton_valider").click()
        except:
            pass

    valid = False
    while not valid:
        try:
            driver.find_element(
                By.CSS_SELECTOR, "div.btn.btn--inverted.dropdown__toggle.js-dropdown__toggle").click()
            # ".btn.btn--inverted.dropdown__toggle--light.dropdown__toggle.js-dropdown__toggle").click()  # portails
            driver.find_elements(
                By.CSS_SELECTOR, ".dropdown__item.js-dropdown__item")[0].click()  # in the drop down menu

            driver.find_elements(
                By.CSS_SELECTOR, ".services-list__group-name.js-opener")[5].click()  # ressources
            driver.find_element(
                By.LINK_TEXT, "Médiacentre").click()  # mediacentre
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print(
                "quelque chose d'innatendu est arrivé, merci de ne pas interférer avec le programme")
            traceback.print_exception(e)
            ans = input(
                "appuies sur <enter> quand tu est pres pour que le programme réessaie de se connecter")
            if ans == 'q':
                break
            valid = False
        else:
            break

    # Store the ID of the original window
    original_window = driver.current_window_handle

    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1

    driver.find_element(
        By.CSS_SELECTOR, 'a[href="https://idp-auth.gar.education.fr/domaineGar?idENT=QTA=&idEtab=MDY3MDAwN1U=&idRessource=ark%3A%2F25998%2Fkwyk-math"]').click()  # kwyk

    # switch tab

    # Wait for the new window or tab
    wait.until(EC.number_of_windows_to_be(2))

    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    prev_wait = driver.timeouts.implicit_wait
    driver.timeouts.implicit_wait = 4
    try:
        driver.find_element(By.CSS_SELECTOR, "#decorationModalOk").click()
    except:
        pass
    driver.timeouts.implicit_wait = prev_wait

    valid = False
    while not valid:
        try:
            driver.find_elements(
                By.CSS_SELECTOR, ".consent-buttons button")[1].click()

            driver.find_elements(
                By.CSS_SELECTOR, ".sommaire-entry.algodecouverte-btn")[0].click()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            traceback.print_exception(e)
            print(
                "quelque chose d'innatendu est arrivé, merci de ne pas interférer avec le programme")
            ans = input(
                "appuies sur <enter> quand tu est pres pour que le programme réessaie d'accéder à kwyk")
            if ans == 'q':
                break
            valid = False
        else:
            break


if __name__ == "__main__":
    from selenium import webdriver
    driver: WebDriver = webdriver.Chrome()
    driver.get("https://www.monbureaunumerique.fr/")

    wait = WebDriverWait(driver, timeout=4)
    login(driver, wait)
