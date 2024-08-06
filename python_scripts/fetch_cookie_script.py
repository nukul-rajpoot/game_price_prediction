from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Specify the path to your Firefox profile
# profile_path = "C:/Users/Nukul/AppData/Roaming/Mozilla/Firefox/Profiles/nezbuhz8.default-release-1"
profile_path = "C:/Users/Nukul/AppData/Roaming/Mozilla/Firefox/Profiles/9pr1ty3r.SteamCookieProfile"

# Set up Firefox profile with Selenium
firefox_options = Options()
firefox_options.profile = webdriver.FirefoxProfile(profile_path)
firefox_options.add_argument("--headless")

# Create a Firefox Profile object and set the preference to disable images
firefox_options.set_preference("permissions.default.image", 2)  # Disable images

# Assign the profile to the options
# Initialize the browser driver with the profile
driver = webdriver.Firefox(options=firefox_options)

# Open the webpage
driver.get("https://www.steamcommunity.com")  # Make sure to use HTTPS for secure sites

# Retrieve browser cookies
cookies = driver.get_cookies()

# Close the browser
driver.quit()
# end_time = time.time()  # Record the end time
# duration = end_time - start_time  # Calculate the duration

cookieDict = cookies[2]
#print(cookieDict)
# for cookie in cookies:
#     print(cookie)

print(cookieDict["value"])

# print(f"The program took {duration} seconds to run.")
with open('cookie.txt', 'w') as file:
    file.write(cookieDict["value"])