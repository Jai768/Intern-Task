from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def scrape(case_type, case_no):
    URL = "https://dhcmisc.nic.in/pcase/guiCaseWise.php"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(URL)

        try:
            case_type_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "ctype"))))
            available_types = [opt.text.strip() for opt in case_type_dropdown.options]
            if case_type not in available_types:
                return {"error": f"Invalid case type '{case_type}'."}
            case_type_dropdown.select_by_visible_text(case_type)
        except TimeoutException:
            return {"error": "Case type dropdown not found on the page."}

        try:
            case_no_input = wait.until(EC.presence_of_element_located((By.ID, "regno")))
            captcha_label = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/form/table[1]/tbody/tr[10]/td[2]/div/label/font")
            ))
            captcha_input = driver.find_element(By.NAME, "captcha_code")
            case_no_input.send_keys(case_no)
            captcha_input.send_keys(captcha_label.text)
        except TimeoutException:
            return {"error": "Form fields not found (case number or captcha)."}

        driver.find_element(By.NAME, "Submit").click()

        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/center/form/table[1]")))
        except TimeoutException:
            return {"error": f"No results found for {case_type} {case_no}"}

        case_details = {
            "case_no": f"{case_type} {case_no}",
            "cnr": driver.find_element(By.XPATH, "/html/body/center/form/table[1]/tbody/tr[3]/td[2]/font").text,
            "status": driver.find_element(By.XPATH, "/html/body/center/form/table[1]/tbody/tr[5]/td[2]/font").text,
            "date_of_filing": driver.find_element(By.XPATH, "/html/body/center/form/table[1]/tbody/tr[1]/td[5]/font").text,
            "date_of_registration": driver.find_element(By.XPATH, "/html/body/center/form/table[1]/tbody/tr[3]/td[5]/font").text,
            "date_of_disposal": driver.find_element(By.XPATH, "/html/body/center/form/table[1]/tbody/tr[5]/td[5]/font").text,
            "petitioner": driver.find_element(By.XPATH, "/html/body/center/form/table[2]/tbody/tr[1]/td/font/b").text,
            "respondent": driver.find_element(By.XPATH, "/html/body/center/form/table[2]/tbody/tr[2]/td/font/b").text,
            "dealing_assistant": driver.find_element(By.XPATH, "/html/body/center/table[3]/tbody/tr[1]/td[2]/font").text,
            "filing_advocate": driver.find_element(By.XPATH, "/html/body/center/table[3]/tbody/tr[3]/td[2]/font").text
        }

        driver.find_element(By.ID, "filing").click()
        filing_rows = driver.find_elements(By.XPATH, "/html/body/center/table[5]/tbody/tr[position()>1]")
        filing_details = [
            {"srl_no": c[0], "date": c[1], "details": c[2]}
            for row in filing_rows if (c := [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]) and len(c) >= 3
        ]

        driver.find_element(By.ID, "listing").click()
        listing_rows = driver.find_elements(By.XPATH, "/html/body/center/table[5]/tbody/tr[position()>1]")
        listing_details = []
        for row in listing_rows:
            cells = []
            for cell in row.find_elements(By.TAG_NAME, "td"):
                link = cell.find_elements(By.TAG_NAME, "a")
                if link:
                    cells.append(link[0].text.strip())
                    cells.append(link[0].get_attribute("href"))
                else:
                    cells.append(cell.text.strip())

            if len(cells) >= 4:
                listing_details.append({
                    "srl_no": cells[0],
                    "date": cells[1],
                    "link": cells[2],
                    "details": cells[3]
                })

        return {
            "case_details": case_details,
            "filing_details": filing_details,
            "listing_details": listing_details
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()
