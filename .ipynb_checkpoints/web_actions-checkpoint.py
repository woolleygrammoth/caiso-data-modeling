from driver import Driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

prefs = {"download.default_directory" : "/Users/graham/Desktop/projects/caiso-data-modeling/scraped-data/daily"} 
#Set your own download directory (absolute paths only)

DRIVER = Driver(prefs=prefs)
driver = DRIVER()
driver.get('https://www.caiso.com/TodaysOutlook/Pages/default.aspx')

def download_net_demand(date: str) -> None:
    """
    Downloads the net demand CSV from CAISO for the given date
    date: a string containing a date in MM/DD/YYYY format
    """
    from setup import correct_format
    assert correct_format(date), "date must be in MM/DD/YYYY format"
    # change the date to be downloaded
    net_demand_date_input = driver.find_element(by=By.CSS_SELECTOR, value='input.net-demand-date')
    net_demand_date_input.clear()
    net_demand_date_input.send_keys(date)
    net_demand_date_input.send_keys(Keys.RETURN) 
    # execute the download
    net_demand_download = driver.find_element(by=By.CSS_SELECTOR, value='a#downloadNetDemandCSV')
    dropdown = net_demand_download.find_element(by=By.XPATH, value='../../button')
    dropdown.click()
    net_demand_download.click()





