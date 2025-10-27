import re
import time
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")
options.add_argument("--disable-logging")
options.add_argument("--silent")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

BASE_URL = "https://ge.globo.com/agenda/#/futebol/"

def scrape_globo_matches():

    result = []
    try:
        today = datetime.today()
        print(today, 'today')
        for i in range(5):
            current_date = today + timedelta(days=i)
            date_str = current_date.strftime("%d-%m-%Y")
            url = f"{BASE_URL}{date_str}"
            driver.get(url)

            try:
                accept_cookies_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'div.cookie-banner-lgpd_button-box button'))
                )
                accept_cookies_button.click()
            except:
                pass

            championship_groups = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div.eventGrouperstyle__GroupByChampionshipsWrapper-sc-1bz1qr-0.gumeun'))
            )

            for championship in championship_groups:

                event_name_tag = championship.find_element(
                    By.CLASS_NAME, 'eventGrouperstyle__ChampionshipName-sc-1bz1qr-2.eDkDKF')
                event_name = event_name_tag.text if event_name_tag else None

                tournament_matches = championship.find_elements(
                    By.CSS_SELECTOR, 'a.sc-eldPxv.fdoTBT')

                for match in tournament_matches:
                    try:
                        button_where_to_watch = match.find_element(
                            By.CLASS_NAME, 'sc-hzhJZQ.SLnjU')
                        time.sleep(1.2)
                        if button_where_to_watch.text.strip() == "Onde assistir?":
                            driver.execute_script(
                                "arguments[0].scrollIntoView(true);", button_where_to_watch)
                            time.sleep(0.4)
                            driver.execute_script(
                                "arguments[0].click();", button_where_to_watch)
                            time.sleep(1.2)

                            team_1 = match.find_element(
                                By.CLASS_NAME, "sc-bmzYkS.ivQJob")
                            team_1_name_tag = team_1.find_element(
                                By.CSS_SELECTOR, "span.sc-eeDRCY.kXIsjf").text.strip()
                            team_1_name = team_1_name_tag if team_1_name_tag else None
                            team_1_image = team_1.find_element(
                                By.CSS_SELECTOR, "img").get_attribute("src")

                            team_2 = match.find_element(
                                By.CLASS_NAME, "sc-bmzYkS.epSQAH")
                            team_2_name_tag = team_2.find_element(
                                By.CSS_SELECTOR, "span.sc-eeDRCY.kXIsjf").text.strip()
                            team_2_name = team_2_name_tag if team_2_name_tag else None
                            team_2_image = team_2.find_element(
                                By.CSS_SELECTOR, "img").get_attribute("src")

                            if not team_1_name or not team_2_name:
                                try:
                                    close_button = driver.find_element(
                                        By.CSS_SELECTOR, 'button[aria-label="Fechar"]')
                                    close_button.click()
                                except Exception:
                                    pass
                                continue

                            modal_content = WebDriverWait(driver, 10).until(
                                EC.visibility_of_element_located(
                                    (By.ID, "drawer_container-agenda-modrawer"))
                            )

                            channels_match = modal_content.find_elements(
                                By.CLASS_NAME, 'sc-ewnqHT.gHsKNV')

                            channels = []

                            date_match = modal_content.find_elements(
                                By.CSS_SELECTOR, 'span.infosstyle__FooterItem-sc-pa6je2-3.eutUSD')

                            for channel_match_info in channels_match:
                                channel = channel_match_info.find_element(
                                    By.CLASS_NAME, "sc-iVCKna.lhodZX").text.strip()
                                if channel != "Cartola":
                                    channels.append(channel)

                            try:
                                hour = next((t.text.strip() for t in date_match if re.match(
                                    r'^\d{2}:\d{2}$', t.text.strip())), None)
                            except:
                                hour = None

                            result.append({
                                "date": date_str,
                                "hour": hour,
                                "event_name": event_name,
                                "team_1_name": team_1_name,
                                "team_1_img": team_1_image,
                                "team_2_name": team_2_name,
                                "team_2_img": team_2_image,
                                "channels": channels
                            })

                        try:
                            close_button = modal_content.find_element(
                                By.CSS_SELECTOR, 'button[aria-label="Fechar"]')
                            close_button.click()

                        except Exception:
                            pass

                    except NoSuchElementException:
                        continue

        return result

    finally:
        driver.quit()

