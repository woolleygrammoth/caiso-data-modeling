from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class Driver: 
    """
    Creates a webdriver that downloads to a particular path
    """
    
    def __init__(self, prefs): 
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("prefs", prefs)

    
    
    def __call__(self): 
        driver = webdriver.Chrome(service=Service('./chromedriver 2'), options=self.options) # navigate to chromedriver executable 
        driver.maximize_window()
        return driver

