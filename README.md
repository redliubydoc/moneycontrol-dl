# moneycontrol-dl

A python script that fetches stock prices from your moneycontrol portfolio and saves it into a spreadsheet for further analysis.

### How to Run?

* Open "src/credentials.py" and put your username and password of your moneycontrol account there
* Update your firefox browser
* Download the latest release of gecko web driver form https://github.com/mozilla/geckodriver/releases
* Extract it into the 'webdrivers/linux and Run ./moneycontrol-dl.sh if you are linux user
* Extract it into the 'webdrivers/windows and Run ./moneycontrol-dl.bat if you are windows user
  

### Dependencies

    pip3 install selenium
    pip3 install pandas
    pip3 install openpyxl
    pip3 install colorama

*   mozilla firefox

### Debugging

* Make sure you are connected to internet
* If you get stuck in login for a long time then probably your credentials are wrong
  
### Optional 

* You may use windows scheduler or cron to run this script automatically on a daily basis at a specific time