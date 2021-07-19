import selenium
from selenium import webdriver
import pandas as pd

url = 'https://factcheck.snu.ac.kr/'

driver = webdriver.Chrome(executable_path='D:\\chromedriver_win32\\chromedriver')
driver.get(url=url)

#팝업페이지 오늘 하루동안 열지 않기 버튼 클릭
button1 = driver.find_element_by_xpath("/html/body/div[5]/div[2]/label")
button1.click()
button2 = driver.find_element_by_xpath("/html/body/div[4]/div[2]/label")
button2.click()

#검색하기
search = driver.find_element_by_xpath('//*[@id="gnb"]/div/div/form/fieldset/input')
keyword = "커피"
search.send_keys(keyword)
search.submit()

#제목,카테고리,스피커,진위여부 리스트 초기화
titles = []
categories = []
speakers = []
veracities = []

#3페이지까지
for page in range(3):
    #제목
    title = driver.find_elements_by_xpath("//div[@class='prg fcItem_li']/p")
    for i in range(len(title)):
        if i%2 == 0:
            titles.append(title[i].text)
    #카테고리
    category = driver.find_elements_by_xpath("//div[@class='prg fcItem_li']/ul")
    for i in range(len(category)):
        categories.append(category[i].text)
        
    #스피커, 진위여부
    for i in range(5):
        speaker = driver.find_elements_by_class_name('name')
        speakers.append(speaker[i].text)
        veracity = driver.find_elements_by_class_name('meter-label')
        veracities.append(veracity[i].text)
        
    if page == 0:
        next_page = driver.find_element_by_xpath('//*[@id="pagination"]/div/a[4]')
    next_page = driver.find_element_by_xpath('//*[@id="pagination"]/div/a[5]')
    next_page.click()

#카테고리 2개로 나누기
category1 = []
category2 = []
for i in categories:
    a, b = i.split('\n')
    category1.append(a)
    category2.append(b)

#컬럼 명 지정
col = ["title", "category1", "category2", "speaker", "veracity"]

#컬럼에 맞게 데이터 정리
data = []
for i in range(len(titles)):
    row = []
    row.append(titles[i])
    row.append(category1[i])
    row.append(category2[i])
    row.append(speakers[i])
    row.append(veracities[i])
    data.append(row)

#데이터프레임 생성
df = pd.DataFrame(data, columns = col)
df.to_csv('snu_fact.csv', encoding='utf-8-sig', index=False)
