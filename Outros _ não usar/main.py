from asyncio import sleep
from datetime import date, datetime
from lib2to3.pgen2 import driver
from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def login():
    usuario = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[1]/label[1]/input")
    usuario.send_keys("wcalestini")
    usuario.send_keys(Keys.TAB)
    senha = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[1]/label[2]/input")
    senha.send_keys("937826")
    senha.send_keys(Keys.ENTER)
    time.sleep(1)

def painel():
    clickpainel = driver.find_element(By.CLASS_NAME, 'title-optionMenu').click()
    time.sleep(1)

def preencher_lojas():
    lojaInicial = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div/div[3]/form/div[1]/input")
    lojaInicial.clear()
    lojaInicial.send_keys("5114")
    lojaFinal = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div/div[3]/form/div[2]/input")
    lojaFinal.clear()
    lojaFinal.send_keys("5114")
    time.sleep(1)

def converter_datas():
    data_inicial_str = "2023-07-13"
    data_inicial = datetime.strptime(data_inicial_str, "%Y-%m-%d").date()
    data_final_str = "2023-07-13"
    data_final = datetime.strptime(data_final_str, "%Y-%m-%d").date()

    data_inicial_element = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[3]/input")
    data_inicial_element.clear()
    data_inicial_element.send_keys(data_inicial.strftime("%d/%m/%Y"))
    data_final_element = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[4]/input")
    data_final_element.clear()
    data_final_element.send_keys(data_final.strftime("%d/%m/%Y"))
    time.sleep(1)

def preencher_pdvs():
    pdvInicial = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[5]/input")
    pdvInicial.clear()
    pdvInicial.send_keys("1")
    pdvFinal = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[3]/form/div[6]/input")
    pdvFinal.clear()
    pdvFinal.send_keys("1")

def ativar_checkboxes():
    filtroIntegrar = driver.find_element(By.NAME,"TODO")
    filtroIntegrar.click()
    filtroAguardando = driver.find_element(By.NAME,"AWAIT")
    filtroAguardando.click()
    filtroErro = driver.find_element(By.NAME,"ERROR")
    filtroErro.click()
    filtroFalha = driver.find_element(By.NAME,"FATAL_ERROR")
    filtroFalha.click()
    filtroProcessando = driver.find_element(By.NAME,"PROCESSING")
    filtroProcessando.click()
    filtroDados = driver.find_element(By.NAME,"REINTEGRATING")
    filtroDados.click()
    filtroConvertido = driver.find_element(By.NAME,"MAPPED")
    filtroConvertido.click()
    time.sleep(1)

def filtrar():
    botaoFiltrar = driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div/div[3]/form/div[10]/button")
    botaoFiltrar.click()

def validaDados():
    validaInfo = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/div/table/div/h2')
    if validaInfo.text == "<h2>A busca retornou nenhum resultado, tente com outros filtros.</h2>":
        print("A busca retornou nenhum resultado, tente com outros filtros.")
    else:
        print("A busca retornou resultados.")



## O código rodará daqui para baixo, pois as defs serão chamadas abaixo.##
# Abre o Navegador
driver = webdriver.Chrome()
driver.get("http://10.255.4.139:5001/login")
assert "Painel" in driver.title


login()             # Realiza Login
painel()            # Clica no painel
preencher_lojas()   # Preenchendo informação de Loja Inicial e Final
converter_datas()   # Convertendo as datas
preencher_pdvs()    # Preenchendo campos de PDV inicial e Final
ativar_checkboxes() # Ativa os checkboxes
filtrar()           # Clica em Filtrar