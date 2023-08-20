from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date
import os


def save_asx200_stocks_info():
    print("Getting ASX200 stocks info from Trading View")

    dr = webdriver.Firefox()
    dr.get("https://www.tradingview.com/symbols/ASX-XJO/components/")
    dr.implicitly_wait(10)

    # Find button to view all 200 companies
    # button = dr.find_element(By.CLASS_NAME, "loadButton-Hg5JK_G3")
    button = dr.find_element(By.CLASS_NAME, "loadButton-SFwfC2e0")

    # Use Javascript to click the button rather than a "natural click" implemented by Selenium which has issues
    dr.execute_script("arguments[0].click();", button)

    # Wait for the table to fully load, this line checks to see that the button becomes invisible
    # elem = WebDriverWait(dr, 10).until(ec.invisibility_of_element_located((By.CLASS_NAME, "loadButton-Hg5JK_G3")))
    elem = WebDriverWait(dr, 10).until(ec.invisibility_of_element_located((By.CLASS_NAME, "loadButton-SFwfC2e0")))

    # Use the webdriver to save the html source (after the table has loaded with all ASX200 companies)
    html = dr.page_source
    # Save the html file as a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')

    # Verifying tables and their classes
    # This will also save the last table found as the variable 'table'
    # print('Classes of each table:')
    for table in soup.find_all('table'):
    #     print(table.get('class'))
        pass

    # Defining of the dataframe
    df = pd.DataFrame(columns=['Ticker', 'Price', 'Chg % 1D', 'Chg 1D', 'Technical Rating 1D', 'Vol 1D', 'Volume * Price 1D', 'Market cap', 'P/E(TTM)', 'EPS(TTM)', 'Employees', 'Sector'])

    rows = []
    for row in table.tbody.find_all('tr'):
        # Find all data for each column
        columns = row.find_all('td')

        # If column cell is not empty, save to respective register
        if(columns != []):
            ticker = columns[0].text[0:3]
            price = columns[1].text.strip("AUD")
            chg_pct = columns[2].span.contents[0]
            chg_1d = columns[3].text
            rating = columns[4].text
            vol_1d = columns[5].text
            vol_price_1d = columns[6].text
            market_cap = columns[7].text
            pe = columns[8].text
            eps = columns[9].text
            employees = columns[10].text
            sector = columns[11].text

            # Create a new row and append data dict to the rows list
            row = {'Ticker': ticker, 'Price': price, 'Chg % 1D': chg_pct, 'Chg 1D': chg_1d, 'Technical Rating 1D': rating, 'Vol 1D': vol_1d, 'Volume * Price 1D': vol_price_1d, 'Market cap': market_cap, 'P/E(TTM)': pe, 'EPS(TTM)': eps, 'Employees': employees, 'Sector': sector}
            rows.append(row)

    # Concatenate the rows to the existing dataframe
    df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

    # Return dataframe
    # return df

    # Call function to retrieve data
    # asx200 = save_asx200_stocks_info()

    # Get current date
    date_today = str(date.today())

    # Check if Results folder exists, if not create it
    if os.path.exists('Results'):
        pass
    else:
        os.makedirs('Results')

    # Create filename with path
    asx200_filename = os.path.join("Results", (date_today + '_ASX200.csv'))
    # Save dataframe to csv
    df.to_csv(asx200_filename)

    print("ASX200 data for today's date " + date_today + " saved to " + asx200_filename)
