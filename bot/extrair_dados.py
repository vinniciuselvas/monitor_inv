import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from pandas.errors import EmptyDataError 

def extrair_detalhes_e_transacoes(driver):
    # Espera o modal abrir e ficar visível
    wait  = WebDriverWait(driver, 10)
    modal = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-content"))
    )

    # ---------- DETALHES DO TOPO ----------
    token = modal.find_element(
        By.XPATH,
        ".//div[contains(@class,'value-box')]/span[contains(text(),'-')]"
    ).text.strip()

    nome_ativo = modal.find_element(
        By.XPATH,
        ".//strong[text()='Nome Ativo:']/following-sibling::span"
    ).text.strip()

    mercado = modal.find_element(
        By.XPATH,
        ".//strong[text()='Mercado:']/following-sibling::span"
    ).text.strip()

    saldo_atual = modal.find_element(
        By.XPATH,
        ".//strong[text()='Saldo:']/following-sibling::span"
    ).text.strip().replace("$", "").replace(",", ".")

    data_criacao = modal.find_element(
        By.XPATH,
        ".//strong[text()='Data de Criação:']/following-sibling::span"
    ).text.strip()

    lucro_total = modal.find_element(
        By.XPATH,
        ".//strong[contains(text(),'Você lucrou')]/following-sibling::span"
    ).text.strip()

    # ---------- TRANSAÇÕES ----------
    transacoes = modal.find_elements(By.CSS_SELECTOR, ".operations-modal .op")
    dados = []

    for t in transacoes:
        # p[0] = Data ...  p[1] = Saldo ...  p[2] = Lucro ...  p[3] = Token ...
        campos = t.find_elements(By.TAG_NAME, "p")
        registro = {
            "Token Bot":      token,
            "Nome Ativo":     nome_ativo,
            "Mercado":        mercado,
            "Saldo Atual":    saldo_atual,
            "Data de Criação":data_criacao,
            "Lucro Total":    lucro_total,
            "Data":           campos[0].text.replace("Data: ", "").strip(),
            "Saldo Parcial":  campos[1].text.replace("Saldo: $", "").strip(),
            "Lucro Parcial":  campos[2].text.replace("Lucro: ", "").strip(),
            "Token Transação":campos[3].text.replace("Token: ", "").strip()
        }
        dados.append(registro)

    return pd.DataFrame(dados)

def salvar_dados_novos(df: pd.DataFrame, caminho_csv="data/dados.csv"):
    """
    Salva/atualiza o CSV dentro da pasta data.
    Apenas registros novos (pelo campo 'Token Transação') são acrescentados.
    """

    # 1) Garante que a pasta data/ exista
    pasta = os.path.dirname(caminho_csv)          # "data"
    os.makedirs(pasta, exist_ok=True)

    # 2) Lê o CSV existente, se houver e tiver conteúdo
    if os.path.exists(caminho_csv):
        try:
            df_existente = pd.read_csv(caminho_csv)
        except EmptyDataError:
            df_existente = pd.DataFrame()
    else:
        df_existente = pd.DataFrame()

    # 3) Concatena, remove duplicados e grava
    df_final = (
        pd.concat([df_existente, df], ignore_index=True)
          .drop_duplicates(subset=["Token Transação"], keep="first")
    )

    df_final.to_csv(caminho_csv, index=False)
    print(f"CSV atualizado em {caminho_csv}. Total de linhas: {len(df_final)}")