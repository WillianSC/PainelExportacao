import tkinter as tk
from tkinter import simpledialog
from datetime import datetime
from tkinter import messagebox
from dateutil.parser import parse
from asyncio import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import logging
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(filename='Painel_Exportacao.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def login(driver):
    logging.info("Realizando Login")
    usuario = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[1]/label[1]/input")
    usuario.send_keys("wcalestini")
    usuario.send_keys(webdriver.Keys.TAB)
    senha = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[1]/label[2]/input")
    senha.send_keys("937826")
    senha.send_keys(webdriver.Keys.ENTER)
    time.sleep(1)

def painel(driver):
    logging.info("Clicando no Painel Reduzao Z")
    clickpainel = driver.find_element(By.XPATH, '/html/body/div/div[2]/nav/ul/div/a/p')
    clickpainel.click()
    time.sleep(1)
    return clickpainel  # Retorna o elemento clicado

def preencher_lojas(driver, lojas):
    logging.info(f"Preenchendo Informação de Loja: {', '.join(lojas)}")

    lojaInicial = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[1]/input")
    lojaInicial.clear()
    time.sleep(1)
    lojaInicial.send_keys(lojas[0])
    time.sleep(1)

    lojaFinal = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[2]/input")
    lojaFinal.clear()
    time.sleep(1)
    lojaFinal.send_keys(lojas[-1])
    time.sleep(1)

def limpa_filtro_loja(driver):
    logging.info("Limpando Filtro Loja Inicial e Final")
    lojaInicial = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[1]/input")
    lojaInicial.clear()
    lojaFinal = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[2]/input")
    lojaFinal.clear()

def limpa_filtro_pdv(driver):
    logging.info("Limpando Filtro PDV Inicial e Final")
    pdvInicial = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[5]/input")
    pdvInicial.clear()
    pdvFinal = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[6]/input")
    pdvFinal.clear()

def convert_date_format(date_string):
    formats_to_try = ["%d-%m-%Y", "%d/%m/%Y", "%d-%m-%Y"]
    for fmt in formats_to_try:
        try:
            date_obj = datetime.strptime(date_string, fmt)
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None

def preencher_data_processamento(driver, data_processamento):
    logging.info(f"Data de processamento: {data_processamento}")
    data_processamento_element = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[3]/input")
    data_processamento_element.clear()
    data_processamento_element.send_keys(data_processamento)

def converter_datas(driver, data_processamento):
    logging.info("Convertendo Data inserida")
    data_inicial_str = data_processamento
    data_inicial = datetime.strptime(data_inicial_str, "%Y-%m-%d").date()
    data_final_str = data_inicial_str
    data_final = datetime.strptime(data_final_str, "%Y-%m-%d").date()

    data_inicial_element = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[3]/input")
    data_inicial_element.clear()
    data_inicial_element.send_keys(data_inicial.strftime("%d/%m/%Y"))
    data_final_element = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[4]/input")
    data_final_element.clear()
    data_final_element.send_keys(data_final.strftime("%d/%m/%Y"))

def preencher_pdvs(driver, pdv):
    logging.info(f"Preenchendo Informação de PDV: {pdv}")
    pdvInicial = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[5]/input")
    pdvInicial.clear()
    time.sleep(1)
    pdvInicial.send_keys("1")
    pdvFinal = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[6]/input")
    pdvFinal.clear()
    time.sleep(1)
    pdvFinal.send_keys("99")

def ativar_checkboxes(driver):
    logging.info("Ativando CheckBox's")
    filtroIntegrar = driver.find_element(By.NAME, "TODO")
    filtroIntegrar.click()
    filtroIntegrado = driver.find_element(By.NAME, "DONE")
    filtroIntegrado.click()
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
    logging.info("Clicando botão Filtrar")
    botaoFiltrar = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[10]/button")
    botaoFiltrar.click()
    time.sleep(1)  # Pequeno atraso para aguardar a ação concluir

def reintegra_cupom(driver, soup):
    logging.info("Ação de REINTEGRAR Cupom")
    # Valida se a página não possui cupom:
    empty_message_div = soup.find('div', class_='ColorEmptyMessage')
    if empty_message_div:
        logging.info("Campo Cupom Vazio, Pulando para o próximo PDV")
        pass
    else:
        logging.info("Selecionando todos Cupons")
        # Clicar no switch "Selecionar toda pagina"
        botao_selecionar = driver.find_element(By.CSS_SELECTOR, '.react-switch-handle')
        actions = ActionChains(driver)
        actions.click(botao_selecionar)
        actions.perform()
        time.sleep(1)  # Pequeno atraso para aguardar a ação concluir

        # Verifica se o elemento "Clique Aqui!" está presente na página
        try:
            logging.info("Clicando no painel Clique aqui")
            message_element = driver.find_element(By.CSS_SELECTOR, 'div.message')
            actions = ActionChains(driver)
            actions.click(message_element)
            actions.perform()
            time.sleep(1)  # Pequeno atraso para aguardar a ação concluir
        except NoSuchElementException:
            logging.info("Painel Clique Aqui não encontrado")
            pass  # Se não encontrar o elemento "Clique Aqui!", continua o fluxo

        logging.info("Clicando no botão Reintegrar")
        # Botão Reintegrar
        botaoReintegrar = driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div[1]/div/button/p')
        botaoReintegrar.click()

def on_close():
    if messagebox.askokcancel("Fechar programa", "Tem certeza que deseja sair?"):
        root.destroy()

def main():
    logging.info("Abrindo Navegador") # Abre o Navegador
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://10.255.4.139:5001/login")
    assert "Painel" in driver.title

    login(driver)  # Realiza Login

    # Solicitar a data de processamento ao usuário
    root = tk.Tk() # Biblioteca que vai tratar o fechamento da GUI
    root.withdraw()
    root.protocol("WM_DELETE_WINDOW", on_close)  # Definir tratamento para o fechamento da janela

    data_processamento = None
    while data_processamento is None:
        data_processamento = simpledialog.askstring("Data de Processamento", "Qual a data de processamento (DD-MM-YYYY)?")
        if data_processamento is None:
            if not messagebox.askokcancel("Fechar programa", "Tem certeza que deseja sair?"):
                continue  # Continua no loop para solicitar nova data
            else:
                logging.info("Nenhuma data de processamento inserida. Encerrando o programa.")
                root.destroy()
                return
        else:
            converted_date = convert_date_format(data_processamento)
            if not converted_date:
                messagebox.showerror("Erro", "Formato de data inválido. Tente novamente.")
                data_processamento = None

    # Lista de Lojas e PDVs
    lojas_pdvs = [
        {"loja": "5001"},
        {"loja": "5002"},
        {"loja": "5003"},
        {"loja": "5004"},
        {"loja": "5005"},
        {"loja": "5006"},
        {"loja": "5007"},
        {"loja": "5008"},
        {"loja": "5009"},
        {"loja": "5011"},
        {"loja": "5012"},
        {"loja": "5013"},
        {"loja": "5014"},
        {"loja": "5015"},
        {"loja": "5016"},
        {"loja": "5017"},
        {"loja": "5018"},
        {"loja": "5019"},
        {"loja": "5020"},
        {"loja": "5021"},
        {"loja": "5022"},
        {"loja": "5023"},
        {"loja": "5024"},
        {"loja": "5025"},
        {"loja": "5026"},
        {"loja": "5027"},
        {"loja": "5028"},
        {"loja": "5029"},
        {"loja": "5030"},
        {"loja": "5031"},
        {"loja": "5032"},
        {"loja": "5033"},
        {"loja": "5034"},
        {"loja": "5035"},
        {"loja": "5036"},
        {"loja": "5037"},
        {"loja": "5038"},
        {"loja": "5039"},
        {"loja": "5040"},
        {"loja": "5041"},
        {"loja": "5042"},
        {"loja": "5043"},
        {"loja": "5044"},
        {"loja": "5045"},
        {"loja": "5046"},
        {"loja": "5047"},
        {"loja": "5048"},
        {"loja": "5049"},
        {"loja": "5050"},
        {"loja": "5051"},
        {"loja": "5052"},
        {"loja": "5053"},
        {"loja": "5054"},
        {"loja": "5055"},
        {"loja": "5056"},
        {"loja": "5057"},
        {"loja": "5058"},
        {"loja": "5059"},
        {"loja": "5060"},
        {"loja": "5061"},
        {"loja": "5062"},
        {"loja": "5063"},
        {"loja": "5064"},
        {"loja": "5065"},
        {"loja": "5066"},
        {"loja": "5067"},
        {"loja": "5068"},
        {"loja": "5069"},
        {"loja": "5070"},
        {"loja": "5071"},
        {"loja": "5072"},
        {"loja": "5073"},
        {"loja": "5074"},
        {"loja": "5075"},
        {"loja": "5076"},
        {"loja": "5077"},
        {"loja": "5078"},
        {"loja": "5079"},
        {"loja": "5080"},
        {"loja": "5081"},
        {"loja": "5082"},
        {"loja": "5083"},
        {"loja": "5084"},
        {"loja": "5085"},
        {"loja": "5086"},
        {"loja": "5087"},
        {"loja": "5088"},
        {"loja": "5089"},
        {"loja": "5090"},
        {"loja": "5091"},
        {"loja": "5092"},
        {"loja": "5093"},
        {"loja": "5094"},
        {"loja": "5095"},
        {"loja": "5096"},
        {"loja": "5097"},
        {"loja": "5098"},
        {"loja": "5099"},
        {"loja": "5100"},
        {"loja": "5101"},
        {"loja": "5102"},
        {"loja": "5103"},
        {"loja": "5105"},
        {"loja": "5106"},
        {"loja": "5107"},
        {"loja": "5108"},
        {"loja": "5109"},
        {"loja": "5110"},
        {"loja": "5111"},
        {"loja": "5112"},
        {"loja": "5113"},
        {"loja": "5114"},
        {"loja": "5115"},
        {"loja": "5116"},
        {"loja": "5117"},
        {"loja": "5118"},
        {"loja": "5119"},
        {"loja": "5120"},
        {"loja": "5121"},
        {"loja": "5122"},
        {"loja": "5123"},
        {"loja": "5124"},
        {"loja": "5126"},
        {"loja": "5127"},
        {"loja": "5129"},
        {"loja": "5130"},
        {"loja": "5131"},
        {"loja": "5132"},
        {"loja": "5133"},
        {"loja": "5134"},
        {"loja": "5135"},
        {"loja": "5136"},
        {"loja": "5137"},
        {"loja": "5138"},
        {"loja": "5139"},
        {"loja": "5140"},
        {"loja": "5141"},
        {"loja": "5142"},
        {"loja": "5143"},
        {"loja": "5144"},
        {"loja": "5145"},
        {"loja": "5146"},
        {"loja": "5147"},
        {"loja": "5148"},
        {"loja": "5149"},
        {"loja": "5150"},
        {"loja": "5151"},
        {"loja": "5158"},
        {"loja": "5161"},
        {"loja": "5162"},
        {"loja": "5163"},
        {"loja": "5164"},
        {"loja": "5184"},
        {"loja": "5187"},
        {"loja": "5201"},
        {"loja": "5212"},
        {"loja": "5219"},
        {"loja": "5236"},
        {"loja": "5240"},
        {"loja": "5242"},
        {"loja": "5246"},
        {"loja": "5254"},
        {"loja": "5271"},
        {"loja": "5276"},
        {"loja": "5286"},
        {"loja": "7100"},
        {"loja": "9100"},
        {"loja": "9101"},
        {"loja": "9102"},
        {"loja": "9103"},
        {"loja": "9104"},
        {"loja": "9105"},
        {"loja": "9106"},
        {"loja": "9107"},
        {"loja": "9108"},
        {"loja": "9109"},
        {"loja": "9110"},
        {"loja": "9111"},
        {"loja": "9112"},
        {"loja": "9113"},
        {"loja": "9114"},
        {"loja": "9115"},
        {"loja": "9116"},
        {"loja": "9117"},
        {"loja": "9118"},
        {"loja": "9119"},
        {"loja": "9120"},
        {"loja": "9121"},
        {"loja": "9122"},
        {"loja": "9123"},
        {"loja": "9124"},
        {"loja": "9125"},
        {"loja": "9126"},
        {"loja": "9127"},
        {"loja": "9128"},
        {"loja": "9129"},
        {"loja": "9130"},
        {"loja": "9131"},
        {"loja": "9132"},
        {"loja": "9133"},
        {"loja": "9134"},
        {"loja": "9135"},
        {"loja": "9136"},
        {"loja": "9137"}       
    ]
    
    lojas_por_iteracao = 30
    
    # Loop para iterar sobre as lojas e PDVs
    for i in range(0, len(lojas_pdvs), lojas_por_iteracao):
        lojas_subset = [item["loja"] for item in lojas_pdvs[i:i+lojas_por_iteracao]]
        # Chama a função painel e guarda o elemento clicado
        panel_element = painel(driver)

        # Agora que o painel foi chamado, podemos preencher as lojas
        preencher_lojas(driver, lojas_subset)
        
        limpa_filtro_loja(driver) # Limpa filtro Loja
        converter_datas(driver, converted_date) # Insere data no campo
        ativar_checkboxes(driver)  # Ativa os checkboxes
        
        filtrar(driver)  # Clica em Filtrar
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        time.sleep(1)  # Pequeno atraso para aguardar a ação concluir
        reintegra_cupom(driver, soup)  # Realiza o processo de Exportação
        limpa_filtro_loja(driver)  # Limpa os campos de loja antes do próximo loop
        time.sleep(1)  # Pequeno atraso para aguardar a ação concluir

    # Fechar o navegador após a conclusão do loop
    driver.quit()

if __name__ == "__main__":
    main()