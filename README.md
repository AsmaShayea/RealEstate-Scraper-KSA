# RealEstate-Scraper-KSA

This project is a web scraping tool designed to gather prices and detailed property information for apartments listed for sale in Dammam, Saudi Arabia (KSA).

The data is collected from a popular real estate platform in Saudi Arabia, focusing on apartments for sale over the last three years. The tool organizes the scraped data into a structured CSV file with the following details:

## Property Details:
- **المساحة (Area)**  
- **عمر العقار (Property Age)**  
- **الدور (Floor)**  
- **دورات المياه (Bathrooms)**  
- **الصالات (Living Rooms)**  
- **غرف النوم (Bedrooms)**  
- **الواجهة (Facade)**  

## Boolean Features (True/Null):
- **مدخل سيارة (Parking)**  
- **مصعد (Elevator)**  
- **توفر الماء (Water Supply)**  
- **توفر الكهرباء (Electricity Supply)**  
- **توفر صرف صحي (Sewage Availability)**  
- **سطح خاص (Private Roof)**  
- **مدخلين (Two Entrances)**  

## Location Details:
- **المنطقة (Region)**  
- **المدينة (City)**  
- **الحي (Neighborhood)**  
- **الشارع (Street)**  
- **الرمز البريدي (Postal Code)**  

## Other Details:
- **Price**  
- **Page Number**  
- **Page Link**  
- **Apartment Link**  
- **Published Date**  

This tool provides valuable insights into the real estate market for apartments in Dammam, KSA, with comprehensive and structured data for analysis.

---

## Key Highlights

### Bot Detection Handling
- **Integrated selenium-stealth** to mimic human browser behavior.
- **Reinitialized the browser** after every page and apartment to clear cookies.
- **Used randomized user agents and headless mode** for additional stealth.

```python
from selenium import webdriver
from selenium_stealth import stealth

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Enable headless mode for stealth
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

```


### Dynamic Data Loading
- **Managed collapsible tabs** (e.g., location details) by dynamically interacting with clickable elements.
- **Used WebDriverWait with expected_conditions** to ensure that elements were fully loaded and clickable before interacting.

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_location_details(driver):
    try:
        # Wait for and click the "Location Details" tab
        location_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'تفاصيل الموقع')]"))
        )
        location_tab.click()
        time.sleep(2)  # Allow time for the location details to load

        # Extract location details
        location_details = {}
        location_elements = driver.find_elements(By.CLASS_NAME, "_item___4Sv8")
        for location in location_elements:
            label = location.find_element(By.CLASS_NAME, "_label___qjLO").text
            value = location.find_elements(By.TAG_NAME, "span")[-1].text
            location_details[label] = value
        return location_details
    except Exception as e:
        print(f"Error scraping location details: {e}")
        return {}
```

