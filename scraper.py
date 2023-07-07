from bs4 import BeautifulSoup
import requests
import csv
import re

def get_name(product):
    try:
        name = product.find("span", attrs={"class":'a-size-medium a-color-base a-text-normal'}).string.strip()
    except AttributeError:
        name = ""
    return name


def get_url(product):
    url = "https://www.amazon.in"
    try:
        url += product.find("a", attrs={"class":'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
    except AttributeError:
        url += ""
    return url

def get_price(product):
    try:
        price = product.find("span", attrs={'class':'a-offscreen'}).text.strip()
    except AttributeError:
        price = ""
    return price


def get_rating(product):
	try:
		rating = product.find("i", attrs={'class':'a-icon a-icon-star-small a-star-small-4 aok-align-bottom'}).text.strip()
	except AttributeError:
		try:
			rating = product.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

def get_review_count(product):
	try:
		review_count = product.find("span", attrs={'class':'a-size-base s-underline-text'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

def get_description(product_page):
    try:
        description = product_page.find("ul", attrs={'class':'a-unordered-list a-vertical a-spacing-mini'}).text.strip()
    except AttributeError:
        description = ""
    return description

def get_asin(product_page):
    try:
        asin = product_page.find('input', {'id': 'ASIN'})['value']
    except AttributeError:
        asin = ""
    return asin

def get_product_description(product_page):
    try:
        product_description = product_page.find(id='productDescription').get_text().strip()
    except AttributeError:
        product_description=""
    return product_description

def get_manufacturer(product_page):
    try:
        manufacturerSearch = product_page.find_all(text=lambda text: 'Manufacturer' in text)
        for manufacturer_word in manufacturerSearch:
            manufacturer = manufacturer_word.find_next().get_text().strip()     
            
    except AttributeError:
        manufacturer = "Manufacturer not found"
    return manufacturer


if __name__ == '__main__':
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36','Accept-Language': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'})
    URL = "https://www.amazon.in/s?k=bags&page="

    csvFile = open('results.csv', 'wt', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)

    productCount = 1

    for page in range(1,21):
        
        req = requests.get(URL + str(page), headers=HEADERS)
        soup = BeautifulSoup(req.text, 'lxml')

        products = soup.find_all('div', attrs={'data-component-type': 's-search-result'})
        
        for product in products:
            
            csvRow = []

            # Scraping details for Part 1
            product_price = get_price(product)
            product_rating = get_rating(product)
            product_url = get_url(product)
            product_name = get_name(product)
            product_review_count = get_review_count(product)

            product_req = requests.get(product_url, headers=HEADERS)
            product_page = BeautifulSoup(product_req.text, 'lxml')

            # Scraping details for Part 2
            description = get_description(product_page)
            asin = get_asin(product_page)
            product_description = get_product_description(product_page)
            manufacturer = get_manufacturer(product_page)

            # Adding Part 1 details
            csvRow.append(product_url)
            csvRow.append(product_name)
            csvRow.append(product_price)
            csvRow.append(product_rating)
            csvRow.append(product_review_count)
            
            # Adding Part 2 details
            csvRow.append(description)
            csvRow.append(asin)
            csvRow.append(product_description)
            csvRow.append(manufacturer)

            # print(productCount)
            # print(product_url)
            # print(product_name)
            # print(product_price)
            # print(product_rating)
            # print(product_review_count)
            # print(description)
            # print(asin)
            # print(product_description)
            # print(manufacturer)
            # print()

            productCount += 1

            # Entering all product details to csv file
            writer.writerow(csvRow)
        
        print(f'Page {page} scraped')

    csvFile.close()

