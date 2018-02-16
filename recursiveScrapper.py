import os
import urllib.request
import requests
from bs4 import BeautifulSoup

def xkcdSpider(baseUrl, basePage):
    url = baseUrl
    page = basePage
    altText = {}
    comicTitle = ''
    print(baseUrl,basePage)
    url = baseUrl+"/"+str(page)+"/"
    sourceCode = requests.get(url)
    if sourceCode.status_code == 200:
        plainText = sourceCode.text
    else:
        # print("ASDASDAS")
        raise ValueError(url+": Couldn't reach the webpage.")

    soup = BeautifulSoup(plainText)

    for link in soup.findAll('div'):
        divID = link.get('id')
        if divID == 'ctitle':
            comicTitle = link.string

    for image in soup.findAll('img',{'alt':comicTitle}):
        altText[page] = comicTitle+': '+ image.get('title')
        imgUrl = 'https:'+image.get('src')
        urllib.request.urlretrieve(imgUrl, './images/'+str(page)+'.'+os.path.basename(imgUrl))

    for link in soup.findAll('a',{'rel':'next'}):
        nextRef = link.get('href')[1:-1]
        nextUrl = baseUrl+link.get('href')

    with open('./altTexts.txt','a') as file:
        file.write(str(page)+': '+altText.get('page','')+'\n')

    if nextRef == '':
        return
    else:
        xkcdSpider(baseUrl,nextRef)

    return


if __name__ == '__main__':

    webpageUrl = 'https://xkcd.com'

    with open('./altTexts.txt','r') as file:
        latestComic = file.readlines()[-1].split(':')[0]

    # latestComic = '1955'
    xkcdSpider(webpageUrl, latestComic)
