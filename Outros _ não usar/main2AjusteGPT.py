from asyncio import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time

def login(driver):
    usuario = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[1]/label[1]/input")
    usuario.send_keys("wcalestini")
    usuario.send_keys(webdriver.Keys.TAB)
    senha = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[1]/label[2]/input")
    senha.send_keys("937826")
    senha.send_keys(webdriver.Keys.ENTER)
    time.sleep(1)

def painel(driver):
    clickpainel = driver.find_element(By.CLASS_NAME, 'title-optionMenu').click()
    time.sleep(1)

def preencher_lojas(driver, loja):
    lojaInicial = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[1]/input")
    lojaInicial.clear()
    time.sleep(1)
    lojaInicial.send_keys(loja)
    time.sleep(1)

    lojaFinal = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[2]/input")
    lojaFinal.clear()
    time.sleep(1)
    lojaFinal.send_keys(loja)
    time.sleep(1)

def limpa_filtro_loja(driver):
    lojaInicial = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[1]/input")
    lojaInicial.clear()
    lojaFinal = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[2]/input")
    lojaFinal.clear()

def limpa_filtro_pdv(driver):
    pdvInicial = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[5]/input")
    pdvInicial.clear()
    pdvFinal = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[6]/input")
    pdvFinal.clear()

def converter_datas(driver):
    data_inicial_str = "2023-07-12"
    data_final_str = "2023-07-12"

    
    data_inicial = datetime.strptime(data_inicial_str, "%Y-%m-%d").date()
    data_final = datetime.strptime(data_final_str, "%Y-%m-%d").date()

    data_inicial_element = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[3]/input")
    data_inicial_element.clear()
    data_inicial_element.send_keys(data_inicial.strftime("%d/%m/%Y"))
    data_final_element = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[4]/input")
    data_final_element.clear()
    data_final_element.send_keys(data_final.strftime("%d/%m/%Y"))

def preencher_pdvs(driver, pdv):
    pdvInicial = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[5]/input")
    pdvInicial.clear()
    time.sleep(1)
    pdvInicial.send_keys(pdv)
    pdvFinal = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[6]/input")
    pdvFinal.clear()
    time.sleep(1)
    pdvFinal.send_keys(pdv)

def ativar_checkboxes(driver):
    filtroIntegrar = driver.find_element(By.NAME, "TODO")
    filtroIntegrar.click()
    filtroAguardando = driver.find_element(By.NAME, "AWAIT")
    filtroAguardando.click()
    filtroErro = driver.find_element(By.NAME, "ERROR")
    filtroErro.click()
    filtroFalha = driver.find_element(By.NAME, "FATAL_ERROR")
    filtroFalha.click()
    filtroProcessando = driver.find_element(By.NAME, "PROCESSING")
    filtroProcessando.click()
    filtroDados = driver.find_element(By.NAME, "REINTEGRATING")
    filtroDados.click()
    filtroConvertido = driver.find_element(By.NAME, "MAPPED")
    filtroConvertido.click()
    time.sleep(1)

def filtrar(driver):
    botaoFiltrar = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[10]/button")
    botaoFiltrar.click()
    time.sleep(1)  # Pequeno atraso para aguardar a ação concluir

def reintegra_cupom(driver, soup):
    # Valida se a página não possui cupom:
    empty_message_div = soup.find('div', class_='ColorEmptyMessage')
    if empty_message_div:
        pass
    else:
        # Clicar no switch "Selecionar toda pagina"
        botao_selecionar = driver.find_element(By.CSS_SELECTOR, '.react-switch-handle')
        actions = ActionChains(driver)
        actions.click(botao_selecionar)
        actions.perform()
        time.sleep(1)  # Pequeno atraso para aguardar a ação concluir

    # Clicará na aba de "Selecionar todos cupons" procurando pelo elemento "Clique Aqui!"
        mensagem_clique_aqui = soup.find('div', text='Clique aqui!')
        if mensagem_clique_aqui:
            message_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Clique aqui!')]")
            actions = ActionChains(driver)
            actions.click(message_element)
            actions.perform()
            time.sleep(1)  # Pequeno atraso para aguardar a ação concluir
        # Senão ele apenas clicará no Botão Reintegrar
        else:
            pass
        botaoReintegrar = driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div[1]/div/button/p')
        botaoReintegrar.click()


def main():
    # Abre o Navegador
    driver_path = "C:\ChromeDriver\chromedriver.exe"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://10.255.4.139:5001/login")
    assert "Painel" in driver.title

    login(driver)  # Realiza Login

    # Lista de Lojas e PDVs
    lojas_pdvs = [
        {"loja": "5114", "pdvs": ["1", "2", "3", "4"]},
        {"loja": "5119", "pdvs": ["1", "2", "3", "4"]},
        {"loja": "5134", "pdvs": ["1", "2", "3", "4", "5", "6", "7"]},
        {"loja": "5135", "pdvs": ["1", "2", "3", "4", "5"]},
        {"loja": "5138", "pdvs": ["1", "2", "3"]},
        {"loja": "5158", "pdvs": ["1", "2", "3", "4"]},
        {"loja": "5162", "pdvs": ["1", "2", "3", "4", "5"]},
        {"loja": "5163", "pdvs": ["1", "2", "3", "4", "5"]},
        {"loja": "5170", "pdvs": ["1", "2", "3", "4", "5"]},
        {"loja": "5184", "pdvs": ["1", "2", "3", "4", "5"]},
        {"loja": "5187", "pdvs": ["1", "2", "3", "4", "5"]},
        {"loja": "5212", "pdvs": ["1", "2", "3", "4", "5"]},
        {"loja": "5229", "pdvs": ["1", "2", "3", "4"]},
        {"loja": "5230", "pdvs": ["1", "2", "3", "4"]},
        {"loja": "5242", "pdvs": ["1", "2", "3", "4"]},
        {"loja": "5244", "pdvs": ["1", "2", "3", "4"]},
        {"loja": "5259", "pdvs": ["1", "2", "3", "4"]},
        {"loja": "5263", "pdvs": ["1", "2", "3", "4", "5"]},
        {"loja": "5265", "pdvs": ["1", "2", "3", "4"]},
        {"loja": "5282", "pdvs": ["1", "2", "3", "4"]},
        {"loja": "5284", "pdvs": ["1", "2", "3", "4"]}
    ]

    # Loop para iterar sobre as lojas e PDVs
    for item in lojas_pdvs:
        loja = item["loja"]
        pdvs = item["pdvs"]

        painel(driver)  # Clica no painel
        limpa_filtro_loja(driver)
        limpa_filtro_pdv(driver)
        preencher_lojas(driver, loja)  # Preenchendo informação de Loja Inicial e Final
        ativar_checkboxes(driver)  # Ativa os checkboxes
        converter_datas(driver)

        # Loop para iterar sobre os PDVs
        for pdv in pdvs:
            preencher_pdvs(driver, pdv)  # Preenchendo campos de PDV inicial e Final
            filtrar(driver)  # Clica em Filtrar

            # Obter o conteúdo HTML após o filtro
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            time.sleep(1)  # Pequeno atraso para aguardar a ação concluir
            reintegra_cupom(driver, soup)  # Realiza o processo de Exportação
            limpa_filtro_loja(driver)  # Limpa os campos de loja antes do próximo loop
            time.sleep(1)  # Pequeno atraso para aguardar a ação concluir
            limpa_filtro_pdv(driver)  # Limpa os campos de pdv antes do próximo loop
    # Fechar o navegador após a conclusão do loop
    driver.quit()

if __name__ == "__main__":
    main()
