import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import shutil


def TrocaPasta():
	pasta ="/storage/emulated/0/Documents/Pydroid3"
	arquivos = os.listdir(pasta)
	xlsx = [arq for arq in arquivos if arq.lower().endswith(".xlsx")]
	for planilha in xlsx:
		shutil.move(pasta+f"/{planilha}",pasta+"/Planilhas")

listaURL=[]
listaTitulo =[]
listaPreco = []
listaDescricao = []
listaLocalidade = []

pesquisa=str(input("O que deseja pesquisar?\n"))
pesquisa = pesquisa.replace(" ", "%20")

for i in range(0,5):

	
	link=(f"https://www.olx.com.br/brasil?q={pesquisa}d&opst=3&opst=2&o={i}")
	
	headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"}
	requisicao = requests.get(link, headers=headers)
	requisicao=requisicao.text
	soup =  BeautifulSoup(requisicao,features='lxml')
	
	for link in soup.find_all('a',class_="olx-ad-card__title-link"):
		listaURL.append(link.get('href'))
		print(link)
		request = requests.get(link.get('href'),headers=headers)
		request = request.text
		anuncio = BeautifulSoup(request, features='lxml')
		
	for titulo in soup.find_all(class_="olx-text olx-text--title-small olx-text--block olx-ad-card__title olx-ad-card__title--horizontal"):
		listaTitulo.append(titulo.getText())
		
	for preco in soup.find_all(class_="olx-text olx-text--body-large olx-text--block olx-text--semibold olx-ad-card__price olx-ad-card__price--mobile"):
		listaPreco.append(preco.getText())	

print(len(listaTitulo))
print(len(listaPreco))
print(len(listaURL))


dtFrame =pd.DataFrame({"Titulo":listaTitulo,"Preço":listaPreco,"Link":listaURL})

arquivoExcel = pd.ExcelWriter(f'PesquisaOLX{pesquisa}.xlsx',engine="xlsxwriter")
dtFrame.to_excel(arquivoExcel,sheet_name='Sheet1',index=False)
arquivoExcel.close()
#TrocaPasta()
