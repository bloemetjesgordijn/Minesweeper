from selenium.common.exceptions import NoSuchElementException 

def check_exists_by_class_name(driver, classname):
    try:
        driver.find_element_by_class_name(classname)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_css_selector(driver, classnames):
    try:
        driver.find_element_by_css_selector(classnames)
    except NoSuchElementException:
        return False
    return True   

def check_exists_by_id(driver, id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True
