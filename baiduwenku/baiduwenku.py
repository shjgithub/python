from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import re
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#tempStr = 'line-height:226px;top:11518px;left:6822px;'




reTopVal = re.compile(r'top:(\d+)px')

#print(reTopVal.search(tempStr).group())



def getYpos(e):
    """获取一个字符block的style里面的top属性，相关的regex在函数外面已经compile完成"""
    a1 = e.get('style')
    mo = reTopVal.search(a1)
    return mo.group()
def lineMerging(elems):
    """根据位置top信息判断是否属于一行，如果是新的一行加上换行符以后再连接文字"""
    topTemp = ""
    rstString = ""
    for e in elems:
        if topTemp == getYpos(e):
            rstString += e.text
        else:
            topTemp = getYpos(e)
            rstString += '\n' + e.text
    #rstString=rstString.replace('  \n','{newline}')
    #rstString=rstString.replace('\n','')
    #rstString=rstString.replace('{newline}','\n')
    return rstString
def printText(html):
	#html = driver.page_source
	bf1 = BeautifulSoup(html, 'lxml')
	result = bf1.find_all(class_='ie-fix')
	for each_result in result:
		bf2 = BeautifulSoup(str(each_result), 'lxml')
		texts = bf2.find_all('p')
		print(lineMerging(texts))



driver = webdriver.Chrome();

driver.get('https://wenku.baidu.com/view/b1fd7b22ad51f01dc381f192.html')

while True:
	page = driver.find_element_by_xpath("//div[@class='banner-core-wrap']")
	driver.execute_script("arguments[0].scrollIntoView(true);", page)
	printText(driver.page_source)
	nextPage = driver.find_element_by_xpath("//span[@class='moreBtn goBtn']");
	if nextPage.is_displayed():
		WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//span[@class='moreBtn goBtn']"))).click()
		time.sleep(3)
		printText(driver.page_source)
	else :
		break



#driver.execute_script('window.scrollTo(0, 0)')
#page1 = driver.find_element_by_xpath("//div[@class='top-search-box']")
#driver.execute_script("arguments[0].scrollIntoView(true);", page1)

while True:

	pageNumEle = driver.find_element_by_xpath("//input[@class='page-input']")
	pageNum = pageNumEle.get_attribute('value')
	pageNum = '/' + pageNum
	pageCountEle = driver.find_element_by_xpath("//span[@class='page-count']")
	pageCount = pageCountEle.text

	if pageNum == pageCount: 
		break

	driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
	time.sleep(3)
	printText(driver.page_source)
driver.close()
	
	






