from selenium import webdriver
import time
import webbrowser

chrome_driver = '/usr/local/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(chrome_driver, options=options)

file = open('followed_stocks.txt', 'r')
stocks = dict.fromkeys([ i.replace('\n', '') for i in file ])

def get_stock_price():
    return float(browser.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]').text.strip())

def check_stock(original_price, checked_price):
    return (checked_price <= (original_price - .05) or checked_price >= (original_price + .05))

i = 0
for key in stocks.keys():
    browser.switch_to.window(browser.window_handles[i])
    browser.get('https://finance.yahoo.com/quote/{0}/'.format(key))

    stocks[key] = get_stock_price()

    if i == len(stocks) - 1:
        break
    else:
        i += 1

    browser.execute_script("window.open('')")

while True:
    i = 0
    while i < len(stocks):
        browser.switch_to.window(browser.window_handles[i])

        value = list(stocks.values())[i]
        key = list(stocks.keys())[i]

        new_price = get_stock_price()

        if check_stock(value, new_price):
            print("\nPrevious Price: {0} => {1}".format(key, value))
            print("Current Price: {0} => {1}".format(key, new_price))
            price_difference = round(new_price - value, 2)
            print("Price Difference: {0}".format(price_difference))

            webbrowser.open_new(browser.current_url)

            del(stocks[key])

            browser.close()
        else:
            i += 1
    
    if len(stocks) == 0: break

    time.sleep(3)

browser.quit()

