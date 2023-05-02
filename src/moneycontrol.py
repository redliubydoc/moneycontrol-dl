from pathlib import Path

from colorama import Fore

from threading import Thread

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from console import Console

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

    console = Console(primary_foreground_color=Fore.RED)
    console.print_moneycontrol_ascii_art()

    # create directory structure
    try:
        console_io_thread = Thread(target=console.print, kwargs={
            "msg": "create directory structure",
            "msg_type": "PROGRESS",
            "end": "\r"
        })
        console_io_thread.start()
        create_directory_structure(directories=[
            Path("webdrivers"),
            Path("data"),
            Path("logs")
        ])

    except Exception as e:
        console.show_circular_cursor_animation = False
        console_io_thread.join()
        console.print(msg="create directory structure", msg_type="ERROR")
        print_errs and print(e)
        all_ok = False

    else:
        console.show_circular_cursor_animation = False
        console_io_thread.join()
        console.print(msg="create directory structure", msg_type="SUCCESS")

    if all_ok:
        # launch firefox
        try:
            console_io_thread = Thread(target=console.print, kwargs={
                "msg": "launch firefox",
                "msg_type": "PROGRESS",
                "end": "\r"
            })
            console_io_thread.start()
            options = Options()
            options.add_argument("--profile")
            options.add_argument(config["browser"]["firefox"]["profile_path"])
            options.add_argument("--url")
            options.add_argument(config["moneycontrol"]["stock_tab_url"])
            config["browser"]["firefox"]["headless"] and options.add_argument("--headless")
            service = Service(log_path=str(config["browser"]["firefox"]["log_path"]))

            driver = Firefox(options=options, service=service)

        except Exception as e:
            console.show_circular_cursor_animation = False
            console_io_thread.join()
            console.print(msg="launch firefox", msg_type="ERROR")
            print_errs and print(e)
            cleanup(driver)
            all_ok = False

        else:
            console.show_circular_cursor_animation = False
            console_io_thread.join()
            console.print(msg="launch firefox", msg_type="SUCCESS")

    if all_ok:
        # scrap stock data
        try:
            console_io_thread = Thread(target=console.print, kwargs={
                "msg": "scrap records",
                "msg_type": "PROGRESS",
                "end": "\r"
            })
            console_io_thread.start()
            df_today = scrap_stock_data(driver)

        except Exception as e:
            console.show_circular_cursor_animation = False
            console_io_thread.join()
            console.print(msg="scrap records", msg_type="ERROR")
            print_errs and print(e)
            cleanup(driver)
            all_ok = False

        else:
            console.show_circular_cursor_animation = False
            console_io_thread.join()
            console.print(msg="scrap records", msg_type="SUCCESS")

    if all_ok:
        # save records
        try:
            console_io_thread = Thread(target=console.print, kwargs={
                "msg": "save records",
                "msg_type": "PROGRESS",
                "end": "\r"
            })
            console_io_thread.start()
            save_records(df_today, spreadsheet_path, spreadsheet_backup_path)

        except Exception as e:
            console.show_circular_cursor_animation = False
            console_io_thread.join()
            console.print(msg="save records", msg_type="ERROR")
            print_errs and print(e)
            cleanup(driver)
            all_ok = False

        else:
            console.show_circular_cursor_animation = False
            console_io_thread.join()
            console.print(msg="save records", msg_type="SUCCESS")

    cleanup(driver)
    console.print_exit_message()
    input()
