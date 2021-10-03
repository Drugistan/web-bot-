from typing import FrozenSet
from selenium import webdriver
import csv
from urllib.request import urlopen
from time import sleep
from sys import exit


class Dashboard:

    def __init__(self):
        self.itDashboardUrl = "https://itdashboard.gov/"       # Website Link 
        self.pathForDriver = "/home/dar-night/Desktop/Scrapping/chromedriver"  # Google Driver 
        self.dirverController = webdriver.Chrome(executable_path=self.pathForDriver) 
        self.downloadsLinks = []
        

    def checkConnection(self):
                                                # Check Internet Connection
        try:
            urlForConnection = "https://itdashboard.gov/"
            url_open = urlopen(urlForConnection)
            print(" Connection Stable ", url_open)
            self.BotScraper()
        except ConnectionError as err:
            print(err)
            exit()

    def BotScraper(self):
        self.dirverController.get(self.itDashboardUrl)
        sleep(10)           # Wait for load javascript properly  
        ListOfagency = []
        ListOfagencyPrice = []
        nameOfagency = self.dirverController.find_elements_by_xpath(
            '//span[contains(@class,"w200")]')                 #Xpath for Name agencies 
        priceOfagency = self.dirverController.find_elements_by_xpath(
            '//span[contains(@class,"w900")]') #Xpath for  Price

        for value in nameOfagency:
            ListOfagency.append(value.text)

        for value in priceOfagency:
            ListOfagencyPrice.append(value.text)

        self.cleanList(ListOfagency, ListOfagencyPrice)

        # Agency links

        agency = self.dirverController.find_elements_by_xpath(
            '//div[@id="nav-agencies"]//a')   # Xpath for agencies 
        listOfagency = []
        for element in agency:
            listOfagency.append(element.get_attribute("href"))

        

        for value in listOfagency:
            self.callNewPage(value)

    def cleanList(self, ListOfagency, ListOfagencyPrice): 
        AgencyName = []                                        # clean data  
        AgencyNamePrice = []
        for index in ListOfagency:
            if index == "" or index == '–Government-wide':
                pass
            else:
                AgencyName.append(index)

        for index in ListOfagencyPrice:
            if index == "":
                pass
            else:
                AgencyNamePrice.append(index)
        self.writeIntoFile(AgencyName, AgencyNamePrice)

    def callNewPage(self, link):
        self.dirverController.get(link)                 # call newPages
        sleep(10)                                     # again sleep for load javascript 
        tableList = []
        tableData = self.dirverController.find_elements_by_xpath(
            '//table[@id="investments-table-object"]//tr//td')   # Xpath for table data 
        for value in tableData:
            tableList.append(value.text)
        
        linksDowload = self.dirverController.find_elements_by_xpath(
            '//td[contains(@class,"left sorting_2")]//a')            # Xpath for pdf links 
        for element in linksDowload:
            self.downloadsLinks.append(element.get_attribute("href"))
            
        self.writeIntoSecondFile(tableList)
        for index in self.downloadsLinks:
            self.pdfDownloader(index)

    def writeIntoFile(self, AgencyName, AgencyNamePrice):
                                                        
        with open('Agencies.csv', 'w') as Filewriter:                # Write agencies data in file
            writerPoniter = csv.writer(Filewriter)
            writerPoniter.writerows(zip(AgencyName, AgencyNamePrice))

    def writeIntoSecondFile(self, tableList=None):
        print(tableList)
        if tableList != None:             # write table data in file
            with open('IndividualInvestments.csv', 'a+', newline='\n') as Filewriter:
                writerPoniter = csv.writer(Filewriter)
                writerPoniter.writerow(tableList)
    
    def pdfDownloader(self, link):
        self.dirverController.get(link)             #  download pdf on link 
        sleep(20)
        self.dirverController.find_element_by_xpath("//div[@id = 'business-case-pdf']/a[@href]").click()
        sleep(20)


if __name__ == "__main__":
    objecForDashboard = Dashboard()
    objecForDashboard.checkConnection()
