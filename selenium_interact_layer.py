from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as exc


def setup(url: str):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver: WebDriver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, timeout=20)
    return driver, wait


katex_css_selector = ".katex-mathml annotation"
MathJax_css_selector = "#MathJax-Element-1"


def get_expr(driver: WebDriver, wait, katex: bool, qt_num: int) -> str:
    # getting the equation to solve
    css_selector = katex_css_selector if katex else MathJax_css_selector

    valid = False
    while not valid:
        try:
            LatexText = driver.find_element(
                By.CSS_SELECTOR, css_selector).get_attribute("textContent")
            valid = True
        except:
            print("impossible d'accéder à l'expression mathématique de la question. Êtes-vous sur d'être à la bonne question ? (le programme considère que vous êtes actuellement à la question n° " + str(qt_num) + ")")
            ans = input("appuyer sur <enter> pour ressayer")
            if ans == 'q':
                valid = True
                break
            valid = False
    return LatexText


def write_output(driver: WebDriver, wait, outputLatex: list[str], exclude: list[int] = []):
    selector_base = "#id_answer_"

    indices = []
    i = 0
    while len(indices) < len(outputLatex):
        if i not in exclude:
            indices.append(i)
        i += 1

    for i in range(len(outputLatex)):
        textBox = driver.find_element(
            By.CSS_SELECTOR, selector_base + str(indices[i]))
        driver.execute_script(
            "arguments[0].setAttribute('type','text')", textBox)
        driver.execute_script(
            "arguments[0].style.display = 'block';", textBox)

        textBox.send_keys(outputLatex[i])
        if len(outputLatex) > 1:
            input("appuies sur la touche <enter> pour continuer")


def finish(driver, wait):
    driver.close()
