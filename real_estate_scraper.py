from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import random

# Initialize WebDriver with Anti-Detection
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    # Apply stealth settings to mimic human behavior and bypass detection
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

# Define fixed columns (mapped to extracted data fields)
fixed_columns = [
    "المساحة",         # Area
    "عمر العقار",       # Property Age
    "الدور",           # Floor
    "دورات المياه",     # Bathrooms
    "الصالات",         # Living Rooms
    "غرف النوم",        # Bedrooms
    "الواجهة",         # Facade
    "مدخل سيارة",       # Parking
    "مصعد",            # Elevator
    "توفر الماء",       # Water Supply
    "توفر الكهرباء",    # Electricity Supply
    "توفر صرف صحي",     # Sewage Availability
    "سطح خاص",         # Private Roof
    "مدخلين",          # Two Entrances
    "المنطقة",          # Region
    "المدينة",          # City
    "الحي",            # Neighborhood
    "الشارع",          # Street
    "الرمز البريدي",     # Postal Code
    "رقم المبنى",        # Building Number
    "الرقم الإضافي",     # Additional Number
    "تاريخ الإضافة",     # Published Date
    "السعر",            # Price
    "Apartment Link",
]


# Scrape apartment links and details
def scrape_links_and_details(base_url, csv_filename, max_pages=200, max_apartments_per_page=10):
    """
    Main function to scrape links and details from multiple pages.
    Note: The data extraction relies on the website's HTML structure, which can change.
    """
    current_page = 1
    while current_page <= max_pages:
        try:
            driver = init_driver()  # Reopen the browser for every page
            print(f"Scraping links from page {current_page}...")
            page_url = f"{base_url}/{current_page}"
            driver.get(page_url)
            time.sleep(random.uniform(5, 10))  # Random delay for loading

            apartment_links = []
            links = driver.find_elements(By.XPATH, "//a[div[contains(@class, '_listingCard__PoR_B')]]")
            for link in links[:max_apartments_per_page]:
                href = link.get_attribute("href")
                if href and href not in apartment_links:
                    apartment_links.append(href)

            print(f"Scraped {len(apartment_links)} links from page {current_page}.")

            for url in apartment_links:
                scrape_apartment_details(url, csv_filename)

            current_page += 1

        except Exception as e:
            print(f"Error on page {current_page}: {e}")
            break
        finally:
            driver.quit()

# Scrape apartment details
def scrape_apartment_details(url, csv_filename):
    """
    Scrapes details for a single apartment. 
    Note: Extraction depends on the website structure; selectors may need updates.
    """
    driver = init_driver()
    try:
        print(f"Processing URL: {url}")
        driver.get(url)
        time.sleep(random.uniform(5, 10))  # Delay for page load

        apartment_data = {col: None for col in fixed_columns}
        apartment_data["Apartment Link"] = url

        # Scrape price
        try:
            apartment_data["السعر"] = driver.find_element(By.CLASS_NAME, "_price__EH7rC").text
        except:
            apartment_data["السعر"] = None

        # Scrape property details
        try:
            details_elements = driver.find_elements(By.CLASS_NAME, "_item___4Sv8")
            for detail in details_elements:
                label = detail.find_element(By.CLASS_NAME, "_label___qjLO").text
                value = detail.find_element(By.CLASS_NAME, "_value__yF2Fx").text
                if label in fixed_columns:
                    apartment_data[label] = value
        except:
            pass

        # Scrape Boolean features
        try:
            feature_container = driver.find_element(By.CLASS_NAME, "_newSpecCard__hWWBI._boolean__waHdB")
            feature_elements = feature_container.find_elements(By.CLASS_NAME, "_label___qjLO")
            for feature in feature_elements:
                if feature.text.strip() in fixed_columns:
                    apartment_data[feature.text.strip()] = True
        except:
            pass

        # Scrape "Published Date"
        try:
            info_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'معلومات الإعلان')]"))
            )
            info_tab.click()
            time.sleep(2)

            info_elements = driver.find_elements(By.CLASS_NAME, "_item___4Sv8")
            for info in info_elements:
                label = info.find_element(By.CLASS_NAME, "_label___qjLO").text
                if label == "Published Date":
                    value = info.find_elements(By.TAG_NAME, "span")[-1].text
                    apartment_data[label] = value
        except:
            pass

        # append_to_csv(apartment_data, csv_filename)
        
        print(f"Scraped data: {apartment_data}")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")
    finally:
        driver.quit()

# Append data to CSV
def append_to_csv(data, filename):
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fixed_columns)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

# Main function
def main():
    base_url = "https://sa.aqar.fm/شقق-للبيع/الدمام"  # Apartments for sale in Dammam city
    csv_filename = "test_apartment_data.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        pass
    scrape_links_and_details(base_url, csv_filename)

if __name__ == "__main__":
    main()
