import requests

url = 'https://nlp.johnsnowlabs.com/docs/en/annotators'
r  = requests.get(url)
from bs4 import BeautifulSoup

data = r.text
soup = BeautifulSoup(data,features="html.parser")
print (soup.head.next_element)

for header in soup.find_all("div", {"class": "h3-box"}):
    # print(header)
    para = header.findNext('p')
    print(para.g)
    # print(header.next_siblig)