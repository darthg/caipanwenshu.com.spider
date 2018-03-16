from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import guoxiaoyi.xiciProxies
from lxml import html
import csv
import time
import xlsxwriter
import xlrd
import urllib.parse
#函数库
def is_currentPage(xpathdata,i):
     if xpathdata.xpath('//*[@id="pageNumber"]/span[2]/text()')[0]==i+1:
          return  True
     else:
          return False

def nextpage(browser):#查找下一页
     WebDriverWait(browser,5).until(
          EC.presence_of_element_located((By.CLASS_NAME,"wstitle"))
     )#设置等待时间
     time.sleep(2)
     elem=browser.find_element_by_class_name("next")
     elem.click()
     return browser

def myfind(x,y):
    return [ a for a in range(len(y)) if y[a] == x]

def gettitles(titles):
          i=myfind("|",titles)
          return titles[i[0]+1:i[1]]

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

try:
#workbook=xlrd.open_workbook(r"E:\GitHub\测试文件\2016年保险明细报表.xls")
     workbook=xlrd.open_workbook(r"E:\GitHub\测试文件\对公和小企业授信客户名称清单.xls")
except Exception as e:
     print("读取文件出现异常！请确认文件路径！")
sheets_input=workbook.sheet_by_index(0)
rows=sheets_input.nrows

#----------------------------------------------------------------------------------
dicInput={'URL': '', '文书标题': ''}
with open("E:\GitHub\测试文件\失信人测试结果\授信客户裁判文书网.csv",'a+',newline='') as csvfile:
     fieldnames=['URL','文书标题']
     writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
     writer.writeheader()

#-----------------
#初始化各项参数
url="http://wenshu.court.gov.cn/list/list/?sorttype=1&number=2LDUFQ5Y&guid=665d8a6a-7472-8349765b-8eb1da9cfb43&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:"
IPfp=r'E:\GitHub\测试文件\IP_Pool.xls'
#------保存数据的变量

#-------------------------------------



for k in range(212,rows):
     try:
          Proxy=guoxiaoyi.xiciProxies.getPoxiesRand(IPfp)
          print("已经载入代理"+str(Proxy))
          #设置请求头和获取代理池，设置代理IP
          browser=webdriver.Chrome#设置浏览器类型
          chrome_options = webdriver.ChromeOptions()
          #chrome_options.add_argument('--proxy-server=http://114.215.45.174:3128')
          chrome_options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
          browser = webdriver.Chrome(chrome_options=chrome_options)
          keyword=sheets_input.cell_value(k,0)
          pat='href="(/content/content\?DocID=.*?&amp;KeyWord='+keyword+')"'##这里非常奇葩，有时候amp这个参数你源码中看不到，但是不要忘记加
          browser.get(url+urllib.parse.quote(keyword))
          print("正在尝试查询授信客户:"+keyword)
          '''
          elem1=browser.find_element_by_id("gover_search_key")
          elem1.clear()
          elem1.send_keys(keyword)


          searchbutton=browser.find_element_by_class_name("head_search_btn")#中国裁判文书网找这个搜索按钮一定要用
          searchbutton.click()
          print("已提交查询信息，准备转向...")'''
          time.sleep(3)
          WebDriverWait(browser,300).until(
               EC.presence_of_element_located((By.ID,"resultList"))
          )#设置等待时间
          WebDriverWait(browser,300).until(
               EC.presence_of_element_located((By.CLASS_NAME,"wstitle"))
          )#设置等待时间
          data=browser.page_source#page_source方法输出的字符串，一定要Encode编码转换成二进制才能open出来
          #保存爬取的所需数据
          xpathdata=html.etree.HTML(data)
          title_count=xpathdata.xpath('//*[@id="span_datacount"]/text()')
          print("共有"+str(title_count[0])+"条数据")
          if title_count[0]==0:
               browser.close()
               break
          else:
               if int(title_count[0])%5==0:
                    pageno=int(title_count[0])//5
               else:pageno=int(title_count[0])//5+1
               print("共有"+str(pageno)+"页")

               for i in  range(0,pageno):
                    if i>=25:
                         break
                    print("正在载入"+str(i+1)+"页")
                    data=browser.page_source
                    xpathdata=html.etree.HTML(data)
                    urllist=xpathdata.xpath('//*[@id="resultList"]/div/table/tbody/tr/td/div/a[2]/@href')
                    titlelist=xpathdata.xpath('//*[@id="resultList"]/div/table/tbody/tr/td/div/input[@type="hidden"]/@value')
                    print("当前文案标题为"+str(titlelist))
                    print("urllist长度为"+str(len(urllist)))
                    with open("E:\GitHub\测试文件\失信人测试结果\授信客户裁判文书网.csv",'a+',newline='',errors='ignore') as csvfile:#encoding=这个参数一定不要忘记加哦，不然会报错
                         fieldnames=['URL','文书标题']
                         writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
                         for j in range(0,len(urllist)):
                              dicInput['URL']=str('http://wenshu.court.gov.cn')+urllist[j]
                              dicInput['文书标题']=gettitles(titlelist[j])
                              writer.writerow(dicInput)
                              print("已经写入第"+str(i*5+j+1)+"条数据")
                    del urllist#尝试清空保存数据的变量
                    del titlelist

                    if i<pageno-1 and pageno!=1:
                         browser=nextpage(browser)
                         WebDriverWait(browser,300).until(
                              EC.presence_of_element_located((By.CLASS_NAME,"wstitle"))
                         )#设置等待时间
                         time.sleep(2)
                    else:
                         break

               browser.close()
     except Exception as e:
          print(keyword+"信息采集失败！")
          browser.close()
          continue
