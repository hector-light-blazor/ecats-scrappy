#Author: Hector Chapa
#Program Name: ECAT Scrappy
#Date: 10-16-2020
#Purpose: The program visits a website name texas ecats, once on the website it automates a report and save it a Database
import configparser
from json import loads
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from SysMod import *
from WebMod import *
from SQLMod import *




# INITIAL GET THE CONFIG Parser
config = configparser.ConfigParser()
config.read(os.getcwd() + "/config/config.init")

       
#Get All Logical Drives from computer
drives = getAllDrives()

#The size of the disks
selectedDrive = getBigDrive(drives)

# FOlder destination
newFolder = selectedDrive['letter'] + config['WEB']['cache']

# Call the module if folder not available create one
createFolderForCache(newFolder)



# Setup the initial Chrome settings..
#options = webdriver.ChromeOptions()
#options.add_argument("user-data-dir=" + newFolder)
web = setup(newFolder, config['WEB']['driver_loc'])
web.get(config['WEB']['url'])
delay = 10 # seconds


# Wait until web driver is ready
WebDriverWait(web, delay).until(EC.presence_of_element_located((By.ID, 'Body')))

# get current window handle
main_tab = web.current_window_handle

while True:
    # RE read configuration maybe something change
    config.read(os.getcwd() + "/config/config.init")
    arr_reports = loads(config['AGENCIES']['ARRAY'])
    #Call the module to sign in to the ecats website.
    # Only if needed..
    signInEcats(web, config['WEBLOGINCTRLS'], config['WEBLGNVALUE']) #logInPage_form_keys, log_in_values)

    #Next we going to press the ad hoc to view the reporting..
    #Only if needed..
    goToAdhoc(web, config['WEBMAIN']['adhoc'])

    # Wait until web driver is ready
    WebDriverWait(web, delay).until(EC.presence_of_element_located((By.ID, 'Body')))

    for report in arr_reports:
    # Fetch the appropriate report
        print("")
        print("--------------------------")
        print("NAME REPORT: ", report['LBL'])
        print("Phone: ", report['PHONE'])
        getReportAdHoc(web, report['LBL'])

        # Filled the date and RUN THE REPORT
        runReport(web)

        # Sleep in order to get the new tabs
        sleep(2)

        # Switch TAB from current window...
        tabs = web.window_handles

        for tab in tabs:
            if tab != main_tab:
                web.switch_to.window(tab)
                break
        try:
            # Wait until web driver is ready
            WebDriverWait(web, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'reportTable')))
        except TimeoutException:
            print("TIMED OUT WAITING")

        data = waitAndFetchData(web)
        print("Total DATA: ", len(data))
        print("")
        print("------------------------")
        #Save it into DB
        insertData(data, report['PHONE'])
        #Close Current Tab
        print("CLOSING TAB")
        web.close()
        print("GOING HOME")
        web.switch_to.window(main_tab)
        goToAdhoc(web, config['WEBMAIN']['adhoc'])



