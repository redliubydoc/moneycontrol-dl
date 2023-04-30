from pathlib import Path

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from moneycontrol_utils import cleanup
from moneycontrol_utils import save_records
from moneycontrol_utils import scrap_stock_data

from common_utils import read_json
from common_utils import create_directory_structure


config = read_json(Path("resources", "config.json"))
spreadsheet_path = Path(config["data"]["spreadsheet_path"])
spreadsheet_backup_path = Path(config["data"]["spreadsheet_backup_path"])

print_errs = config["application"]["print_errs"]

driver = None
df_today = None
all_ok = True


if __name__ == "__main__":

    print("=============================================================================")

    # create directory structure
    try:
        print(f"[ .. ] create directory structure", end="\r")
        create_directory_structure(directories=[
            Path("webdrivers"),
            Path("data"),
            Path("logs")
        ])

    except Exception as e:
        print(f"[ er ] create directory structure")
        print_errs and print(e)
        all_ok = False

    else:
        print(f"[ ok ] create directory structure")

    if all_ok:
        # launch firefox
        try:
            print(f"[ .. ] launch firefox", end="\r")
            options = Options()
            options.add_argument("--profile")
            options.add_argument(config["browser"]["firefox"]["profile_path"])
            options.add_argument("--url")
            options.add_argument(config["moneycontrol"]["stock_tab_url"])
            config["browser"]["firefox"]["headless"] and options.add_argument("--headless")
            service = Service(log_path=str(config["browser"]["firefox"]["log_path"]))

            driver = Firefox(options=options, service=service)

        except Exception as e:
            print(f"[ er ] launch firefox")
            print_errs and print(e)
            cleanup(driver)
            all_ok = False

        else:
            print(f"[ ok ] launch firefox")

    if all_ok:
        # scrap stock data
        try:
            print(f"[ .. ] scrap records", end="\r")
            df_today = scrap_stock_data(driver)

        except Exception as e:
            print(f"[ er ] scrap records")
            print_errs and print(e)
            cleanup(driver)
            all_ok = False

        else:
            print(f"[ ok ] scrap records")

    if all_ok:
        # save records
        try:
            print(f"[ .. ] save records => [ {spreadsheet_path} ]", end="\r")
            save_records(df_today, spreadsheet_path, spreadsheet_backup_path)

        except Exception as e:
            print(f"[ er ] save records => [ {spreadsheet_path} ]")
            print_errs and print(e)
            cleanup(driver)
            all_ok = False

        else:
            print(f"[ ok ] save records => [ {spreadsheet_path} ]")

    if all_ok:
        print("=============================================================================")
        print("||||||||||||||||||||||||||||||||| COMPLETED |||||||||||||||||||||||||||||||||")

    print("=============================================================================")
    cleanup(driver)
    input()
