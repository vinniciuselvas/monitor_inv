from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def ir_para_software(driver):
    wait = WebDriverWait(driver, 10)
    botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Software']")))
    botao.click()

def abrir_modal_visualizar(driver):
    wait = WebDriverWait(driver, 10)
    botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Visualizar')]")))
    botao.click()
