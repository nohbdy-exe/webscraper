from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re
import json

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--insecure-ssl")


driver = webdriver.Chrome(options=options)
driver.get("https://usi.edu/directory")



def get_option_texts(driver):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    select_element = soup.find("select", id="deptSelect")
    option_texts = [option.text.strip() for option in select_element.find_all("option")]
    return option_texts




print(driver.title)

def are_buttons_present(driver, timeout=15):  # Increased timeout
  wait = WebDriverWait(driver, timeout)
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-faculty]")))

old_element = ""
def wait_for_element_with_staleness(driver,locator, timeout=10): {
    while True:
        if old_element:
            wait = WebDriverWait(driver,timeout).until(EC.staleness_of(old_element))
        element = WebDriverWait(driver,timeout).until(EC.presence_of_element_located(locator))
        old_element = element
        return element
    except TimeoutException:
        print("Element not found after waiting.")
        return None
}

# Wait for the element to load (adjust wait time as needed)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, "deptSelect")))


options_texts = get_option_texts(driver)
for option_text in options_texts[1:]:
    script = f"""
    var dropdown = document.getElementById("deptSelect");
    var options = dropdown.options;
    for (var i = 0; i < options.length-1; i++) {{
    if (options[i].text == '{option_text}') {{
        options[i].selected = true;
        dropdown.dispatchEvent(new Event('change'));
    }}
    }}
    """
    try:
        wait = WebDriverWait(driver,10)
        wait.until(EC.presence_of_element_located((By.ID, "deptSelect")))
        driver.execute_script(script)
    except:
        # Handle selection error (e.g., print a message)
        print(f"Error selecting option: {option_text}")
    

    wait = WebDriverWait(driver, 10)
    data_div = wait.until(EC.presence_of_element_located((By.ID, "directory")))

    if not data_div:
        print(f"Error with data_div")
        continue
    
    wait = WebDriverWait(driver,10)
    wait.until(EC.visibility_of(data_div))
    
    
    buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[data-faculty]")))
    
    if buttons:
        for button in buttons:
            faculty_data = json.loads(button.get_attribute('data-faculty'))
            position = faculty.data[0]["Positions"][0]
            phone_number = position["Phone"].strip()
            print(f"Phone number for {option_text}:{phone_number}")

driver.quit()