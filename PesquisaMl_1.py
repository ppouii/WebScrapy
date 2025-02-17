import requests as re
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter

listaReal=[]
listaCentavos=[]
listaValor=[]
listaTitulo=[]
listaLink=[]

pesquisa=str(input("Digite o que você deseja: "))
pesquisa = pesquisa.replace(" ","-")
url=f"https://lista.mercadolivre.com.br/{pesquisa}"
headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"}

request = re.get(url,headers)
#print(request)

site=BeautifulSoup(request.text,"lxml")

for titulo in site.find_all(class_="poly-component__title"):
    #print(titulo.getText())
    listaTitulo.append(titulo.getText())

for link in site.find_all(class_="poly-component__title"):
    #print(link.get("href"))
    listaLink.append(link.get("href"))
    r = re.get(link.get("href"),headers)
    pagina = BeautifulSoup(r.text,"lxml")
    for real in pagina.find(class_="andes-money-amount__fraction"):
        listaReal.append(real.getText(), )
    try:
        for centavos in pagina.find(class_="andes-money-amount__cents andes-money-amount__cents--superscript-36"):
            listaCentavos.append(centavos.getText())
    except:
        listaCentavos.append("00")


print(len(listaTitulo))
print(len(listaLink))
print(len(listaCentavos))
print(len(listaReal))

for i in range(len(listaReal)):
    listaValor.append('R$ '+listaReal[i]+','+listaCentavos[i])

dtFrame =pd.DataFrame({"Titulo":listaTitulo,"Link":listaLink, "Valor Cheio":listaValor})

try:
    arquivoExcel = pd.ExcelWriter(f'PesquisaML{pesquisa}.xlsx',engine="xlsxwriter")
    dtFrame.to_excel(arquivoExcel,sheet_name='PesquisaML',index=False)
    worksheet = arquivoExcel.sheets['PesquisaML']


    worksheet.set_column('A:C', 30)

    arquivoExcel.close()
except:
    print("Excel já criado")
