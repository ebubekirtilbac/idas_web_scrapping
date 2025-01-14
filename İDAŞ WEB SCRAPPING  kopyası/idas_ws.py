from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import csv
import time

# WebDriver'ı başlat
driver = webdriver.Chrome()

# Hedef URL'yi aç
driver.get('https://www.idas.com.tr/tr/urunler/yataklar')

# Chatbot veya pop-up'ı kapat
try:
    close_button = driver.find_element(By.ID, 'jivo_close_button')
    close_button.click()
    print("Chatbot kapatıldı.")
except:
    print("Chatbot bulunamadı veya zaten kapalı.")

# Ürün bilgilerini saklamak için bir liste oluşturalım
all_products_data = []

# Ürün linklerini toplamak için bir liste oluşturalım
product_links = []

# Ürün linklerini topla
links = driver.find_elements(By.CSS_SELECTOR, 'div.product-detail a')
for link in links:
    product_links.append(link.get_attribute('href'))

# Her ürün sayfasına gidilsin
visited_products = set()

for product_url in product_links:
    if product_url in visited_products:
        continue
    
    visited_products.add(product_url)
    
    driver.get(product_url)
# Ebat seçimi için Select elementini bulunsun
    size_select = Select(driver.find_element(By.ID, 'body_drpOlcu'))
    
    # Her ebat için işlemleri yapalım
    for index in range(len(size_select.options)):
        size_select = Select(driver.find_element(By.ID, 'body_drpOlcu'))  # Yeniden bul
        option = size_select.options[index]
        size_text = option.text
        size_select.select_by_visible_text(size_text)
        
        # Fiyatın yüklenmesi için beklenecek süre
        time.sleep(2)
        
        # Fiyatı alalım
        price = driver.find_element(By.ID, 'body_div_yeni_fiyat').text
        
        # Marka "Y", ebat ve fiyatı listeye ekleyelim
        all_products_data.append(['İdaş', size_text, price])

# CSV dosyasına kaydet
with open('idas_yatak_fiyatlari.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Marka', 'Ebat', 'Fiyat'])  # Başlıklarda Marka, Ebat ve Fiyat var
    writer.writerows(all_products_data)

print("Veriler CSV dosyasına başarıyla kaydedildi.")

# WebDriver'ı kapat
driver.quit()