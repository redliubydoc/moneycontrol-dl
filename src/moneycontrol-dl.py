# do not edit this file
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options

import datetime
import pandas as pd
import os

# internal module import
from config import geckodriver, geckodriver_log, spreadsheet_path, spreadsheet_backup_path, base_url, stock_tab_url, data_directory_path
from credentials import username, password
from io_util import IoUtil
from console_util import Console


class MoneyControl:

    def __init__(self):

        Console()

        self.today = str(datetime.date.today()).strip()
        self.all_ok = True
        self.io_thread = None
        self.driver = None
        self.start_io_thread(msg="launching webdriver")

        options = Options()
        options.add_argument("--headless")
        options.add_argument('--incognito')
        options.add_argument('--disable-notifications')

        try:
            self.driver = webdriver.Firefox(
                firefox_profile=None,  # default
                firefox_binary=None,  # default
                timeout=30,  # default
                capabilities=None,  # default
                proxy=None,  # default
                executable_path=geckodriver,
                options=options,
                service_log_path=geckodriver_log,
                firefox_options=None,  # deprecated argument for options
                service_args=None,  # default
                desired_capabilities=None,  # default
                log_path=None,  # deprecated argument for service_log_path
                keep_alive=True  # default
            )
            self.stop_io_thread(lmsg="launched webdriver")

        except Exception as e:
            self.stop_io_thread(lmsg="unable to launch webdriver", rmsg='[error]', level='DANGER')

    def start_io_thread(self, msg, end='\r', level='INFO'):
        msg = msg.capitalize()
        self.io_thread = IoUtil(msg=msg, end=end, level=level)
        self.io_thread.start()

    def stop_io_thread(self, lmsg="", rmsg="[ok]", end='\n', level='SUCCESS'):
        self.io_thread.exit_flag = True
        self.io_thread.join()
        if level == "DANGER":
            self.all_ok = False
        if len(lmsg) > 0:
            Console.print_verbose(lmsg=lmsg.capitalize(), rmsg=rmsg, level=level, end=end)

    def login(self):
        if not self.all_ok:
            return
        try:
            self.start_io_thread(msg="signing in")
            # opening baseurl
            self.driver.get(base_url)

            # maximize window
            self.driver.maximize_window()

            # login payload
            input_uname = WebDriverWait(self.driver, 900).until(
                expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".PR > #email")))
            input_uname.click()
            input_uname.send_keys(username)

            input_pwd = WebDriverWait(self.driver, 900).until(
                expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".usepwd > #pwd")))
            input_pwd.click()
            input_pwd.send_keys(password)

            button_login = WebDriverWait(self.driver, 900).until(
                expected_conditions.element_to_be_clickable((By.ID, "ACCT_LOGIN_SUBMIT")))
            button_login.click()

            # login payload ends here
            while True:
                if self.driver.title == "Portfolio Management, Portfolio Investment, Portfolio Tracker, Mutual Fund/Stock Portfolio Manager – Moneycontrol":
                    self.stop_io_thread(lmsg="sign in successful")

                    try:

                        self.start_io_thread(msg="opening stock tab")
                        self.driver.get(stock_tab_url)
                        self.stop_io_thread(lmsg="opened stock tab")

                    except Exception as error:
                        self.stop_io_thread(lmsg="unable to open stock tab", rmsg="[error]", level="DANGER")
                        self.driver.quit()
                    break
                else:
                    pass

        except Exception as error:
            self.stop_io_thread(lmsg="sign in unsuccessful", rmsg="[error]", level="DANGER")
            self.driver.quit()

    def fetch_record(self):  # pull record from website and store in dataframe
        if not self.all_ok:
            return

        row = 1  # w.r.t website table
        df = pd.DataFrame(columns=['NAME', self.today])

        # scroll down to button
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

        while True:
            try:
                col_1 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, '//*[@id="myTableSort"]/tbody/tr[' + str(row) + ']/td[1]'))).text.split('\n')[0]
                col_2 = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located(
                    (By.XPATH, '//*[@id="myTableSort"]/tbody/tr[' + str(row) + ']/td[2]'))).text.split('\n')[0]

                msg = "Fetching records"
                caps_pos = row % len(msg)
                decorated_msg = msg[:caps_pos] + msg[caps_pos:caps_pos + 2].upper() + msg[caps_pos + 2:]
                Console.print_verbose(lmsg=decorated_msg, rmsg="[" + str(row) + "]", end='\r')

                index = col_1.find('(')
                if index != -1:
                    col_1 = col_1[:(index - 1)].strip()

                df = df.append({'NAME': col_1, self.today: col_2}, ignore_index=True)
                row += 1

            except Exception as error:
                if row == 1:  # row value doesn't changed
                    Console.print_verbose(lmsg="Unable To Fetched Records", rmsg="[error]",
                                          level="DANGER")
                    self.driver.quit()
                    self.all_ok = False
                    return
                Console.print_verbose(lmsg=str(row - 1) + " Records Fetched", rmsg="[ok]",
                                      level="SUCCESS")
                break

        for i in range(len(df)):  # converting dataFrame['NAME'] to uppercase
            df.iloc[i, 0] = str(df.iloc[i, 0]).upper()

        df.sort_values('NAME')  # sorting records in ascending order of company name.
        return df

    def save_record(self, df_today):  # process and store record in spreadsheet and backup spreadsheet files
        if not self.all_ok:
            return

        self.start_io_thread(msg="saving records")

        # if spreadsheet and spreadsheet_backup exist
        if os.path.exists(spreadsheet_path) and os.path.exists(spreadsheet_backup_path):

            try:  # try to read dataframe from spreadsheet_backup
                df_bakup = pd.read_excel(spreadsheet_backup_path)
            except Exception as e:
                self.stop_io_thread(lmsg="unable to save records", rmsg="[error]", level="DANGER")
                return

            # if today's record already exist
            if str(df_bakup.columns[-1]).strip() == str(df_today.columns[-1]).strip():
                self.stop_io_thread(lmsg="today's (" + df_today.columns[-1] + ") record already exist", rmsg="[!]",
                                    level="EXCEPTION")
                return

            try:  # try to merge df_today onto df_bakup
                df_tmp = pd.merge(
                    left=df_bakup,
                    right=df_today,
                    how="outer",  # outer join or union
                    on='NAME',  # join key col
                    left_on=None,  # default
                    right_on=None,  # default
                    left_index=False,
                    right_index=False,  # default
                    sort=True,  # sort in lexicographical order
                    suffixes=("_x", "_y"),  # default
                    copy=True,  # default
                    indicator=False,  # default
                    validate='one_to_one'
                )
                df_today = df_tmp

            except Exception as error:  # if there is an error wile merging
                self.stop_io_thread(lmsg="unable to save records", rmsg="[error]", level="DANGER")
                return

        else:
            if not os.path.exists(data_directory_path):
                os.mkdir(data_directory_path)

        try:  # try to saving dataframes to respective spreadsheets
            # open
            spreadsheet_writer = pd.ExcelWriter(spreadsheet_path)
            spreadsheet_bakup_writer = pd.ExcelWriter(spreadsheet_backup_path)

            # write
            df_today.to_excel(spreadsheet_writer, index=False)
            df_today.to_excel(spreadsheet_bakup_writer, index=False)

            # save
            spreadsheet_writer.save()
            spreadsheet_bakup_writer.save()

            self.stop_io_thread(lmsg="records saved in '" + "moneycontrol-dl" + spreadsheet_path[2:] + "'")
            return

        except Exception as error:
            self.stop_io_thread(lmsg="unable to save records", rmsg="[error]", level="DANGER")
            return


# driver code starts here
if __name__ == '__main__':
    obj = MoneyControl()
    obj.login()
    if obj.all_ok:
        table = obj.fetch_record()
        obj.driver.quit()
        if obj.all_ok and table.size != 0:
            Console.print_table(table)
            obj.save_record(table)

    print()
    Console.print_centre_aligned("* * * press enter to exit * * *")
    input()
# driver code ends here
