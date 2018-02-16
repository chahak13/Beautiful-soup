import os
import urllib.request
import requests
from bs4 import BeautifulSoup

def xkcdSpider(max_pages):
    page = 1
    altText = {}
    comicTitle = ''
    while page <= max_pages:
        url = "https://xkcd.com/"+str(page)+"/"
        sourceCode = requests.get(url)
        if sourceCode.status_code == 200:
            plainText = sourceCode.text
        else:
            pass
            # raise ValueError("Couldn't reach the webpage.")

        soup = BeautifulSoup(plainText)

        for link in soup.findAll('div'):
            divID = link.get('id')
            if divID == 'ctitle':
                comicTitle = link.string

        for image in soup.findAll('img',{'alt':comicTitle}):
            altText[page] = comicTitle+': '+ image.get('title')
            imgUrl = 'https:'+image.get('src')
            urllib.request.urlretrieve(imgUrl, './images/'+str(page)+'.'+os.path.basename(imgUrl))

        print(page)
        with open('./altTexts.txt','a') as file:
            file.write(str(page)+': '+altText[page]+'\n')
        page += 1


    return


if __name__ == '__main__':
    xkcdSpider(1956)
