import urllib.request
import urllib.response
from lxml import html#最新的lxml包里没有etree了
import xlsxwriter
import xlrd
import random

Proxyfp=r"E:\GitHub\测试文件\IP_pool.xls"
url='http://www.xicidaili.com/nn/'
header=('User-Agent',"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36")
opener=urllib.request.build_opener()
opener.addheaders=[header]
errorlist=[]

#去除爬到IP中的空数据函数
def removalnull(items):
     for i in range(0,len(items)):
          items[i]=str.strip(items[i])
     for i in  items:
          if '' in items:
               items.remove('')
          elif '长城宽带' in items:
               items.remove('长城宽带')
     return items

#分割爬取下来的IP列表
def recreateIPlist(items,Proxylist):
     for i in  range(0,len(items),6):
          Proxylist.append(items[i:i+6])
     return Proxylist

#写入IP地址到xls文件
def writeIPaddr(data,filepath):
     try:
          workbook = xlsxwriter.Workbook(filepath)
     except Exception as e:
          print("写入代理IP错误！")
     sheet=workbook.add_worksheet()
     sheet.write(0,0,'IP地址')
     sheet.write(0,1,'端口号')
     sheet.write(0,2,'匿名属性')
     sheet.write(0,3,'协议类型')
     sheet.write(0,4,'有效期')
     sheet.write(0,5,'验证时间')
     for i in range(0,len(data)):
          for j in range(0,len(data[i])):
               sheet.write(i+1,j,data[i][j])
     workbook.close()

def getPoxiesRand(filepath):
     try:
     #workbook=xlrd.open_workbook(r"E:\GitHub\测试文件\2016年保险明细报表.xls")
          workbook=xlrd.open_workbook(filepath)
     except Exception as e:
          print("读取代理IP池出现异常！请确认文件路径！")
     sheets=workbook.sheet_by_index(0)
     print("代理IP共有"+str(sheets.nrows-1)+'个')
     rand_no=random.randint(1,sheets.nrows-1)#注意边际范围
     IPAdrr=sheets.cell(rand_no,0).value
     IPPort=sheets.cell(rand_no,1).value
     #print(data)
     return IPAdrr+':'+IPPort#返回IP

#打印爬取失败的异常
def errorPrint(errorlist):
     for i in errorlist:
          print(errorlist)



def start_crawlProxies():
     Proxylist=[]
     for i in range(1,10):
          url='http://www.xicidaili.com/nn/'+str(i)
          print(url)
          try:
               data=opener.open(url,timeout=3).read().decode('utf-8','ignore')
               root=html.etree.HTML(data)
               items=root.xpath("//table[@id='ip_list']/tr/td/text()")
               items=removalnull(items)
               list=recreateIPlist(items,Proxylist)
          except Exception as e:
               print(e)
               errorlist.append(e)
               continue
     return list

list=start_crawlProxies()
writeIPaddr(list,Proxyfp)
'''测试
list=start_crawlProxies()
writeIPaddr(list,Proxyfp)
getPoxiesRand(Proxyfp)
'''