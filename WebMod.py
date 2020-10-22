from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
import os
#MODULE: IF folder doesnt exists create
def createFolderForCache(location):
    if not os.path.exists(location):
        os.mkdir(location)

# MODULE: Handles the log in to the ecats website...
def signInEcats(web, frmID, frmVAL):
    if web.find_elements_by_id(frmID['username']):
        username = web.find_element_by_id(frmID['username'])
        password = web.find_element_by_id(frmID['password'])
        submit = web.find_element_by_id(frmID['submit'])
        chckLogin = web.find_element_by_id(frmID['checkbox'])
        username.send_keys(frmVAL['username'])
        password.send_keys(frmVAL['password'])
        chckLogin.click()
        submit.click()


# MODULE: Redirect to Add HOC Reporting...
def goToAdhoc(web, key):
    if web.find_elements_by_id(key):
        buttonEle = web.find_element_by_id(key)
        buttonEle.click()

# MODULE: Find the report in question
def getReportAdHoc(web, REPORT):
    table = web.find_elements(By.TAG_NAME, "table")
    if len(table) > 0:
        rptTable = table[10]
        rows = rptTable.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            reportName = row.text
            if REPORT in reportName:
                inEle = row.find_elements(By.TAG_NAME, "input")
                if inEle:
                    for img in inEle:
                        is_edit = "edit" in img.get_attribute("src").lower()
                        if is_edit:
                            img.click()
                            return

# MODULE: get today date start and end
def getTodayDate():
    today = date.today()
    tdStr = today.strftime("%m/%d/%Y")
    start = tdStr + " 00:00:00"
    end   = tdStr + " 23:59:59"
    return start, end

def updateValue(web, ele, value):
    web.execute_script("arguments[0].value = arguments[1]", ele, value)


# MODULE: Process the report..
def runReport(web):
    listInputs = web.find_elements(By.TAG_NAME, "input")
    start, end = getTodayDate()
    #Change the input report
    for input in listInputs:
        name = input.get_attribute("name").lower()
        if "startdate" in name:
            print("START DATE:", start)
            updateValue(web, input, start)
        elif "enddate" in name:
            print("END DATE: ", end)
            updateValue(web, input, end)
    #Click on the report to generate.
    for btn in listInputs:
        is_generate = "generate" in btn.get_attribute("name").lower()
        if is_generate:
            btn.click()
            return



# MODULE: Grab all the table data to save to server..
def getDataFromReport(browser, tables):
    print("GETTING DATA")
    final_data = []
    psaps  = browser.find_elements_by_class_name("PSAPName")
    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "td")
        count = 0
        hold_data = []
        for (idx, row) in enumerate(rows):
            index = idx + 1
            mod   = index % 11
            rowValue = row.text
            if "no records found" not in rowValue.lower():
                if mod != 0:
                    hold_data.append(rowValue)
                elif mod == 0:
                    hold_data.append(rowValue)
                    hold_data.append(hold_data[0])
                    tup = tuple(hold_data)
                    hold_data = []
                    final_data.append(tup)
            else:
                break
    print("DONE DATA")
    print("")
    return final_data

# MODULE: will loop until it finds the reportTables class then process the data..
def waitAndFetchData(web):
    notfound = True
    while notfound:
        tables = web.find_elements_by_class_name("reportTable")
        notfound = False if len(tables) > 0 else True
    return getDataFromReport(web, tables)


# MODULE: Setup the WEB Drive 
def setup(folder, driver):
    # Setup the initial Chrome settings..
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("user-data-dir=" + folder)
    web = webdriver.Chrome(driver, options = options)
    return web