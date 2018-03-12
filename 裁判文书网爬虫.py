from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import guoxiaoyi.xiciProxies
from lxml import html
import time
import  random
import xlsxwriter
import xlrd
#函数库


def nextpage(browser):#查找下一页
     nextpage=WebDriverWait(browser,300).until(
          EC.presence_of_element_located((By.CLASS_NAME,"download"))
     )#设置等待时间
     time.sleep(1)
     nextpage=browser.find_element_by_class_name("next")
     while True:
          if nextpage.is_enabled():
               nextpage.click()
               break
          else:
               pass
     return browser

def myfind(x,y):
    return [ a for a in range(len(y)) if y[a] == x]

def gettitles(titles):
     for j in range(0,len(titles)):
          i=myfind("|",titles[j])
          titles[j]=titles[j][i[0]+1:i[1]]

def writeDataXls(urllist,titlelist,fp):
     workbook = xlsxwriter.Workbook(fp)
     sheet=workbook.add_worksheet()
     sheet.write(0,0,'URL')
     sheet.write(0,1,'文书标题')
     for i in range(0,len(urllist)):
          for j in range(0,len(urllist[i])):
               sheet.write(j+1,0,urllist[i][j])
               sheet.write(j+1,1,titlelist[i][j])
     workbook.close()

#初始化各项参数
url="http://wenshu.court.gov.cn/"
keyword="索普"
pat='href="(/content/content\?DocID=.*?&amp;KeyWord='+keyword+')"'##这里非常奇葩，有时候amp这个参数你源码中看不到，但是不要忘记加
print(pat)
IPfp=r'E:\GitHub\测试文件\IP_Pool.xls'
#------保存数据的变量
urllist=[]
titlelist=[]
#获取代理IP
#list=guoxiaoyi.xiciProxies.start_crawlProxies()
#guoxiaoyi.xiciProxies.writeIPaddr(list,IPfp)
Proxy=guoxiaoyi.xiciProxies.getPoxiesRand(IPfp)

#设置请求头和获取代理池，设置代理IP
browser=webdriver.Chrome#设置浏览器类型
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://'+IPfp)
chrome_options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
#chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options)


browser.get(url)
elem1=browser.find_element_by_id("gover_search_key")
elem1.clear()
elem1.send_keys(keyword)
searchbutton=browser.find_element_by_class_name("head_search_btn")#中国裁判文书网找这个搜索按钮一定要用
searchbutton.click()
time.sleep(3)
elem1=WebDriverWait(browser,300).until(
     EC.presence_of_element_located((By.CLASS_NAME,"dataItem"))
)#设置等待时间
data=browser.page_source#page_source方法输出的字符串，一定要Encode编码转换成二进制才能open出来
#保存爬取的所需数据
xpathdata=html.etree.HTML(data)
title_count=xpathdata.xpath('//*[@id="span_datacount"]/text()')
pageno=int(title_count[0])//5
print("共有"+str(pageno)+"页")

workbook = xlsxwriter.Workbook("E:/GitHub/测试文件/裁判文书网.xls")
sheet=workbook.add_worksheet(keyword)
sheet.write(0,0,'URL')
sheet.write(0,1,'文书标题')
sheet.write(0,2,'裁判时间')

for i in  range(0,4):
     try:
          WebDriverWait(browser,300).until(
          EC.presence_of_element_located((By.CLASS_NAME,"download"))
     )#设置等待时间
          data=browser.page_source
          xpathdata=html.etree.HTML(data)
          urllist.append(xpathdata.xpath('//*[@id="resultList"]/div/table/tbody/tr/td/div/a[2]/@href'))
          titlelist.append(xpathdata.xpath('//*[@id="resultList"]/div/table/tbody/tr/td/div/input[@type="hidden"]/@value'))
          if len(urllist[i])!=0:
               for j in range(0,len(urllist[i])):
                    sheet.write(i*5+1+j,0,"http://wenshu.court.gov.cn"+urllist[i][j])
                    index=myfind("|",titlelist[i][j])
                    sheet.write(i*5+1+j,1,titlelist[i][j][index[0]+1:index[1]])
                    sheet.write(i*5+1+j,2,titlelist[i][j][index[1]+1:])
                    print("正在下载第"+str(i)+"页数据")
          elif len(urllist[i])==0:
               print("未采集到"+str(i)+"页数据")
          nextpage(browser)
          '''
          if i!=0 and i%20==0:
               Proxy=guoxiaoyi.xiciProxies.getPoxiesRand(IPfp)
               browser.create_options().add_argument('--proxy-server=http://'+IPfp)
               browser.create_options().add_argument('user-agent="Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"')
               time.sleep(3)'''
     except Exception as e:
          print(e)
          workbook.close()
          break
workbook.close()
browser.close()