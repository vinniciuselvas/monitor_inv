from bot.login import fazer_login
from bot.navegar import ir_para_software, abrir_modal_visualizar
from bot.extrair_dados import extrair_detalhes_e_transacoes, salvar_dados_novos


def executar_extracao():
    driver = fazer_login()
    ir_para_software(driver)
    abrir_modal_visualizar(driver)
    df = extrair_detalhes_e_transacoes(driver)
    salvar_dados_novos(df)
    driver.quit()

if __name__ == "__main__":
    executar_extracao()
