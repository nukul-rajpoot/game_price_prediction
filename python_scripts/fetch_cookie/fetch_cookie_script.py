import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from azure.storage.blob import BlobClient

# Specify the path to your Firefox profile
# profile_path = "C:/Users/Nukul/AppData/Roaming/Mozilla/Firefox/Profiles/nezbuhz8.default-release-1"
#profile_path = "C:/Users/Nukul/AppData/Roaming/Mozilla/Firefox/Profiles/9pr1ty3r.SteamCookieProfile"
profile_path = "/Users/jyoutirraj/Library/Application Support/Firefox/Profiles/37tkq59q.SteamProfile"

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

# print(cookieDict)
cookie_pos = 0
longest_cookie = 0
for i, cookie in enumerate(cookies):
    #print(cookie)
    current_cookie_length = len(cookie['value'])
    if current_cookie_length > longest_cookie:
        cookie_pos = i
        longest_cookie = current_cookie_length

cookie_dict = cookies[cookie_pos]

# print(cookie_dict)

# print(cookie_dict["value"])

# Your blob URL and SAS token
blob_url = 'https://steamgraphsstorage.blob.core.windows.net/container-for-blob/cookie.txt'
sas_token = 'sp=rwd&st=2024-08-06T20:45:18Z&se=2025-09-10T04:45:18Z&spr=https&sv=2022-11-02&sr=c&sig=MKticGz9P9HPI7iXp1a6yuErc5Sv6P9fY%2FfCbxL0PLg%3D'

# Initialize the BlobClient with the SAS token
blob_client = BlobClient.from_blob_url(blob_url=blob_url, credential=sas_token)

# Overwrite the existing blob or create a new one if it doesn't exist
blob_client.upload_blob(cookie_dict["value"], overwrite=True)

print("Cookie has been updated.")

sys.exit(0)

