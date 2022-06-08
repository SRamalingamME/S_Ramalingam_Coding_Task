import time
tic=time.time()
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
# Read the data from CSV file
ScrapingData=pd.read_csv('Amazon Scraping - Sheet1.csv')
# Getting Country Column from CSV file
Country=ScrapingData['country']
CountryCode=[]
for i in range(len(Country)):
    CountryCode.append(Country[i])

# Getting Asin Column from CSV file
Asin=ScrapingData['Asin']
AsinParameter=[]
for i in range(len(Asin)):
    AsinParameter.append(Asin[i])

# Making URLs using Country and Asin data
TotalURLs=[]
for i in range(len(CountryCode)):
    URLFormat="https://www.amazon.{}/dp/{}"
    URL=URLFormat.format(CountryCode[i],AsinParameter[i])
    TotalURLs.append(URL)
# Open the URL and Scrape the Data
BrokenURLs=[]
ProductTitle=[]
ProductImageURL=[]
PriceOfTheProduct=[]
ProductDetails=[]
ValidURLs=[]
URLChoice=TotalURLs[0:100]

for i in URLChoice:
    driver=webdriver.Firefox()
    driver.get(i)

    t=driver.title
    print("Scraping Data Process in ",(i),"URL . . . ")
    if "404" in t:
        BrokenURLs.append(i)
        driver.close()
    else:
        try:
            PT=driver.find_element(By.XPATH,'//*[@id="productTitle"]').text
            ProductTitle.append(PT)
        except:
            PT="Product Title is Not Available"
            ProductTitle.append(PT)
        try:
            img=driver.find_element(By.XPATH,'//*[@id="imgBlkFront"]').get_attribute('src')
            ProductImageURL.append(img)
        except:
            img="Product Image is Not Available"
            ProductImageURL.append(img)
            
        try:
            pri=driver.find_element(By.XPATH,'//*[@id="price"]').text
            PriceOfTheProduct.append(pri)
        except:
            pri="Product Price is Not Available"
            PriceOfTheProduct.append(pri)

        try:
            prd=driver.find_element(By.XPATH,'//*[@id="detailBullets_feature_div"]/ul').text
            ProductDetails.append(prd)
            driver.close()
        except:
            prd="Product Details are Not Available"
            ProductDetails.append(prd)
            driver.close()
# Broken URLs Output in Dictionary
BrokenURLsDict = {
  'Broken URL': BrokenURLs,
}

# Scraped Data Output in Dictionary
data = {
  'Page Title': ProductTitle,
  'Image URL': ProductImageURL,
  'Product Price': PriceOfTheProduct,
  'Product Details': ProductDetails
}

# Scraped Data Output in JSON file 
with open("ScrapedDataOutput.json", "w") as outfile:
    json.dump(data, outfile)

toc=time.time()
print("Total URL Executed:",((len(BrokenURLs))+(len(ProductTitle))))
print("Execution Time: min %.2f sec" % ((toc-tic)/60))
