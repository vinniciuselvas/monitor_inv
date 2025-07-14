from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

# Carrega as variáveis do arquivo .env
load_dotenv()
USER = os.getenv("BOT_USER")
PASS = os.getenv("BOT_PASS")

def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Descomente para rodar invisível
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def fazer_login():
    driver = iniciar_driver()
    driver.get("https://app.fixbrokers.com/")  # ajuste a URL se for diferente

    time.sleep(2)
    driver.find_element(By.NAME, "email").send_keys(USER)
    driver.find_element(By.NAME, "password").send_keys(PASS)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(3)
    print("Login realizado. Página atual:", driver.current_url)
    return driver

# Teste rápido se rodar esse script direto
if __name__ == "__main__":
    fazer_login()

def ir_para_software(driver):
    wait = WebDriverWait(driver, 10)
    software_menu = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='menu-text' and contains(text(),'Software')]")
    ))
    software_menu.click()
    print("Clicou no menu 'Software'.")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    print("Tabela carregada.")

def abrir_modal_visualizar(driver):
    """Abre o modal clicando no botão 'Visualizar' da primeira linha da tabela."""
    wait = WebDriverWait(driver, 10)

    try:
        # Espera o botão 'Visualizar' aparecer e ficar clicável
        botao_visualizar = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(text(),'Visualizar')]"
        )))

        driver.execute_script("arguments[0].scrollIntoView();", botao_visualizar)
        wait.until(EC.element_to_be_clickable(botao_visualizar))

        driver.execute_script("arguments[0].click();", botao_visualizar)
        print("✅ Botão 'Visualizar' clicado.")

        wait.until(EC.visibility_of_element_located((By.ID, "ranking")))
        print("✅ Modal 'ranking' aberto.")

    except Exception as e:
        print("❌ Erro ao abrir o modal:", e)


def extrair_linhas_do_modal(driver):
    """Abre o modal, extrai todas as linhas da tabela do modal e retorna um DataFrame."""
    wait = WebDriverWait(driver, 10)

    try:
        # Aguarda o modal aparecer
        modal = wait.until(EC.visibility_of_element_located((By.ID, "ranking")))
        print("✅ Modal aberto e visível.")

        # Aguarda tabela interna dentro do modal
        tabela = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ranking table")))
        linhas = tabela.find_elements(By.TAG_NAME, "tr")

        dados = []
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) >= 5:  # ajusta conforme o número real de colunas
                dados.append({
                    "Token": colunas[0].text.strip(),
                    "Ativo": colunas[1].text.strip(),
                    "Mercado": colunas[2].text.strip(),
                    "Saldo": colunas[3].text.strip().replace("R$", "").replace(",", "."),
                    "Lucro": colunas[4].text.strip().replace("R$", "").replace(",", "."),
                })

        print(f"✅ {len(dados)} linhas extraídas do modal.")
        return pd.DataFrame(dados)

    except Exception as e:
        print("❌ Erro ao extrair dados do modal:", e)
        return pd.DataFrame()

df = extrair_linhas_do_modal(driver)
df.to_excel("dados_bots_modal.xlsx", index=False)