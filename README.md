# moneycontrol-dl

A python script that fetches stock prices from your moneycontrol portfolio and saves it into a spreadsheet for further analysis.

### How to Run?

* Open "src/credentials.py" and put your username and password of your moneycontrol account there
* Run ./moneycontrol-dl.sh if you are linux user
* Run ./moneycontrol-dl.bat if you are windows user
  

### Dependencies

    $ pip3 install selenium
    $ pip3 install pandas
    $ pip3 install openpyxl
    $ pip3 install colorama

*   mozilla firefox

### Debugging

* Make sure you are connected to internet
* If you stuck login indefinitely then probably your credentials are wrong
* If you get error related to web driver then
  * Update your firefox browser and download the latest release of gecko web driver
  * You can download it from "https://github.com/mozilla/geckodriver/releases"
  * Extract it into the 'webdrivers/<linux/windows>' directory
  
### Optional 

* You may use windows scheduler or cron to run this script automatically on a daily basis at a specific time 