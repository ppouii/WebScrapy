import requests
from bs4 import BeautifulSoup
import pandas as pd

listaTitulo=[]
listaLink=[]
listaPreco=[]

pesquisa="Tablet"
pesquisa = pesquisa.replace(" ","-")
link = f"https://lista.mercadolivre.com.br/{pesquisa}"
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"}
requisicao = requests.get(link,headers=headers)
site = BeautifulSoup(requisicao.text,'lxml')

for titulo in site.find_all(class_="ui-search-item__title"):
    listaTitulo.append(titulo.getText())
for link in site.find_all(class_="ui-search-item__group__element ui-search-link__title-card ui-search-link"):
    listaLink.append(link.get('href'))
for preco in site.find_all(class_="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"):
    listaPreco.append(preco.get("aria-label"))


print(len(listaTitulo))
print(len(listaLink))
print(len(listaPreco))

dtFrame =pd.DataFrame({"Titulo":listaTitulo,"Preço":listaPreco,"Link":listaLink})

arquivoExcel = pd.ExcelWriter(f'PesquisaML{pesquisa}.xlsx',engine="xlsxwriter")
dtFrame.to_excel(arquivoExcel,sheet_name='Sheet1',index=False)
arquivoExcel.close()

