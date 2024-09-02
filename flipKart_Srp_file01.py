from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pnds

#initialize chrome driver
driver = webdriver.Chrome()
driver.maximize_window()

#Stroing list Product Data and Scrap data
all_product_link = []
all_data = []

#loop for first 10 pages
for all_page in range (1,10):
    driver.get(f"https://www.flipkart.com/footwear/kids-infant-footwear/infants/pr?sid=osp%2Cmba%2Cqzr&otracker=nmenu_sub_Baby+%26+Kids_0_Baby+Footwear&otracker=nmenu_sub_Baby+%26+Kids_0_Infant+Footwear&page={all_page}")
    
    all_url = driver.find_elements(By.XPATH, "//a[@class='rPDeLR']")
    
    for url in all_url:
        urls = url.get_attribute("href")
        
        single_url ={
            "Links": urls
        }
        
        all_product_link.append(single_url)
        
df = pnds.DataFrame(all_product_link)
df.to_excel("ab.xlsx", index = False)

#trying to Read the saved Excel file
exccel_file = "ab.xlsx"

pandas_kahini = pnds.read_excel(exccel_file)

for sheet_url in pandas_kahini["Links"]:
    driver.get(sheet_url)
    time.sleep(2)
    
    try:
        name = driver.find_element(By.XPATH, "//h1/span").text.strip()
    except:
        name = ""
        
    try:
        price = driver.find_element(By.XPATH, "//div[@class='Nx9bqj CxhGGd']").text
    except:
        pass
    
    #finding all available sizes
    sizes = ""
    try:
        all_size = driver.find_elements(By.XPATH, "//ul[@class='hSEbzK']//li//a")
        
        for size in all_size:
            size_kahini = size.text
            sizes += size_kahini + ", "
    except:
        sizes = ""
        
    try:
        rating = driver.find_element(By.XPATH, "//div[@class='XQDdHH _1Quie7']").text
    except:
        rating = " "
        
    try:
        seller = driver.find_element(By.XPATH, "//div[@id='sellerName']/span").text
    except:
        seller = " "
    
    #dictionary of the scraped data
    excel_list = {
        "Name": name,
        "Price": price,
        "Size": sizes,
        "Rating": rating,
        "Seller": seller 
    }
    
    all_data.append(excel_list)
    #Checking scraping data
    print(f"Done{len(all_data)}")
    
    #Break when done 45 product data scraping
    if len(all_data) == 45:
        break
    
scraping = pnds.DataFrame(all_data)
scraping.to_excel("f1.xlsx", index = False)

#Close the browser
driver.quit()
        
    
        
        
        
    
    
    
        
