import urllib.request
import urllib.response
from lxml import html#最新的lxml包里没有etree了

url='http://www.xicidaili.com/nn/1'
header=('User-Agent',"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36")
opener=urllib.request.build_opener()
opener.addheaders=[header]
data=opener.open(url).read().decode('utf-8','ignore')
root=html.etree.HTML(data)
items=root.xpath("//table[@id='ip_list']/tr/td/text()")

for i in range(0,len(items)):
     items[i]=str.strip(items[i])
for i in  items:
     if '' in items:
          items.remove('')
     elif '长城宽带' in items:
          items.remove('长城宽带')
print(len(items))
for i in  range(0,len(items),6):
     print(items[i:i+6])


