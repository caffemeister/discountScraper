from bs4 import BeautifulSoup
from selenium import webdriver
from scraper.utils.textstyle import TextStyle
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument("--disable-search-engine-choice-screen")
options.add_argument("--headless")  # Makes browser not open
driver = webdriver.Chrome(options=options)


class DataParser:
    soup = None
    url = None

    def __init__(self):
        pass

    @classmethod
    def get_soup(cls, url):
        cls.url = url
        driver.get(url)
        cls.soup = BeautifulSoup(driver.page_source, "html.parser")

    @staticmethod
    def get_game_picture() -> str:
        driver.get(DataParser.url)
        picture_link = driver.find_element(By.XPATH, '//*[@id="gamepageSlider"]/div[1]/a').get_attribute('href')
        return picture_link

    @staticmethod
    def get_codes_and_coupons():
        xpath_list_discount_percentages, xpath_list_coupon_names = [], []
        finish = 6
        i = 1
        while i <= finish:
            try:
                xpath_list_discount_percentages.append(
                    driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]/div[5]/div/div/div/span[1]').text)
                xpath_list_coupon_names.append(driver.find_element(By.XPATH,
                                                                   f'// *[ @ id = "offers_table"] / div[{i}] / div[5] / div / div / div / span[2]').text)
            except NoSuchElementException:
                if driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]').get_attribute(
                        'class') == 'offers-table-row-gift-card':
                    xpath_list_discount_percentages.append('--')
                    xpath_list_coupon_names.append('--')
                    i += 2
                    finish += 1
                    continue
                else:
                    xpath_list_discount_percentages.append('--')
                    xpath_list_coupon_names.append('--')
            i += 1
        return xpath_list_discount_percentages, xpath_list_coupon_names

    @staticmethod
    def get_merchants():
        merchant_names, available_regions, final_prices, links = [], [], [], []

        i = 1
        finish = 6
        while i <= finish:
            try:
                merchant_names.append(
                    driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]/div[1]/div[1]/span[2]').text)
                available_regions.append(
                    driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]/div[2]/a/div[2]').text)
                final_prices.append(driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]/div[6]').text)
                links.append(
                    driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]/div[6]/a[1]').get_attribute(
                        'href'))
            except NoSuchElementException:
                try:
                    merchant_names.append(
                        driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]/div[1]/div[2]/span[2]').text)
                    available_regions.append(
                        driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]/div[2]/a/div[2]').text)
                    final_prices.append(driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]/div[6]').text)
                    links.append(
                        driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]/div[6]/a[1]').get_attribute(
                            'href'))
                except NoSuchElementException:
                    try:
                        if driver.find_element(By.XPATH, f'//*[@id="offers_table"]/div[{i}]').get_attribute(
                                'class') == 'offers-table-row-gift-card':
                            finish += 1
                            i += 1
                            continue
                    except NoSuchElementException:
                        raise Exception(f"{TextStyle.RED}Critical error encountered when parsing merchant information. "
                                        f"Report issue or check for typos when entering game name.{
                                        TextStyle.RESET}")
            i += 1
        return merchant_names, available_regions, final_prices, links

    @staticmethod
    def update_links(old_links):
        new_links = []
        for link in old_links:
            driver.get(link)
            try:
                new_link = driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div[3]/a').get_attribute('href')
                new_links.append(new_link)
            except NoSuchElementException:
                new_links.append(link)
        return new_links

    @staticmethod
    def parse() -> list[dict]:
        coupons = []
        merchant_names, available_regions, final_prices, links = DataParser.get_merchants()
        xpath_list_discount_percentages, xpath_list_coupon_names = DataParser.get_codes_and_coupons()
        new_links = DataParser.update_links(links)
        for i in range(len(merchant_names)):
            new_dict = {
                'Merchant': merchant_names[i],
                'Region': available_regions[i],
                'Discount': xpath_list_discount_percentages[i],
                'Coupon code': xpath_list_coupon_names[i],
                'Final price': final_prices[i],
                'Link': new_links[i],
            }
            coupons.append(new_dict)
        return coupons
