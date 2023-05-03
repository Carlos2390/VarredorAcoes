from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import mysql.connector
from datetime import date

data = date.today()


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="senha",
  database="acoes"
)

cursor = mydb.cursor()

def mostraTabela():
    cursor.execute("SELECT * FROM acoes")
    result = cursor.fetchall()
    for row in result:
        print(row)


def varrePagina(qtd):
    i = 1
    j = 0
    pagina = 1
    driver = webdriver.Edge()
    driver.get("https://www.infomoney.com.br/cotacoes/b3/acao/")
    sleep(3)
    for j in range(0, qtd):
        print(f"Pagina {pagina}")
        for i in range(1, 16):

            nome = driver.find_element(By.XPATH, f"/html/body/div[5]/article/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[{i}]/td[1]/a/strong").text
            
            preco = driver.find_element(By.XPATH, f"/html/body/div[5]/article/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[{i}]/td[2]/span").text
            preco = float(preco.replace("R$ ", "").replace(",", ".")) #Tranformando em float para inserir na tabela
            
            try: #Ignorando campos vazios
                varD = driver.find_element(By.XPATH, f"/html/body/div[5]/article/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[{i}]/td[3]/span").text
                varD = float(varD.replace(",", ".").replace("%", "")) #Tranformando em float para inserir na tabela
            except:
                varD = 0
            try:
                var12M = driver.find_element(By.XPATH, f"/html/body/div[5]/article/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[{i}]/td[4]/span").text
                var12M = float(var12M.replace(",", ".").replace("%", "")) #Tranformando em float para inserir na tabela
            except:
                var12M = 0
            
            volume = driver.find_element(By.XPATH, f"/html/body/div[5]/article/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[{i}]/td[5]/span").text
            #Tranformando em float e multiplicando em milhão ou bilhão para inserir na tabela
            ultimaLetra = volume[-1]
            numeroTexto = volume.replace("R$ ", "").replace(" ", "").replace(",", ".").replace(ultimaLetra, "")

            if ultimaLetra == "M":
                volume = float(numeroTexto) * 1000000
            elif ultimaLetra == "B":
                volume = float(numeroTexto) * 1000000000
            else:
                volume = float(numeroTexto)
            print(f"Nome: {nome} | Data: {data} | Preço: R$ {preco} | Var D: {varD}% | Var 12M: {var12M}% | Volume: {volume}")
            sql = f"INSERT INTO acoes (nome, data_, preco, varD, var12M, volume) VALUES ('{nome}', '{data}', {preco}, {varD}, {var12M}, {volume})"
            cursor.execute(sql)
            
        proximo = driver.find_element(By.XPATH, "/html/body/div[5]/article/div[3]/div[2]/div[2]/div[2]/div/button[2]")
        driver.execute_script("arguments[0].click();", proximo)
        pagina +=1
        mydb.commit()
        sleep(5)

while True:
    escolha = int(input("""Escolha uma opção
[1] Varrer ações
[2] Mostrar ações
[0] Sair
"""))
    
    if escolha == 0:
        break
    if escolha == 1:
        qtd = int(input("Quantas paginas deseja varrer? "))
        varrePagina(qtd)
    if escolha == 2:
        mostraTabela()