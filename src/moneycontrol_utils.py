from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import pandas
import datetime

def cleanup(driver):
    driver is not None and driver.quit()


def scrap_stock_data(driver):

    # wait until target table is not loaded
    WebDriverWait(driver, 900).until(expected_conditions.presence_of_element_located((By.ID, "myTableSort")))

    html = driver.execute_script("return document.querySelector(\"#myTableSort\").outerHTML;")
    document = BeautifulSoup(html, "html5lib")
    stock_elements = document.select("table#myTableSort > tbody > tr > td:nth-child(1) > span.asset_info")

    stocks = []
    for stock_element in stock_elements:
        stocks.append({
            "id": stock_element.get("asset-id"),
            "name": stock_element.get("data-name"),
            "price": stock_element.get("live-price")
        })

    df = pandas.DataFrame(stocks).rename(columns={
        "id": "ID",
        "name": "NAME",
        "price": str(datetime.date.today()).strip()
    })

    return df


def save_records(df_today, spreadsheet_path, backup_spreadsheet_path):

    if df_today is None or df_today.empty:
        raise Exception("df_today is empty")

    if backup_spreadsheet_path.exists():

        df_backup = pandas.read_excel(backup_spreadsheet_path)

        if str(df_backup.columns[-1]).strip() == str(df_today.columns[-1]).strip():
            raise Exception(f"record for \"{str(df_backup.columns[-1]).strip()}\" already exists")

        df = pandas.merge(
            left=df_backup,
            right=df_today,
            how="outer",
            on='ID',
            sort=True,
            suffixes=("_L", "_R"),
            validate='one_to_one'
        )

        # update stocks names code starts here
        for i, row in df.iterrows():
            if not pandas.isnull(row["NAME_R"]):
                df.at[i, "NAME_L"] = row["NAME_R"]

        df.drop(columns="NAME_R", inplace=True)
        df.rename(columns={"NAME_L": "NAME"}, inplace=True)
        # update stocks names code starts ends here

    else:
        df = df_today

    df.to_excel(spreadsheet_path, index=False)
    df.to_excel(backup_spreadsheet_path, index=False)
