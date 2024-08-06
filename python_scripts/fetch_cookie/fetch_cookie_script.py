from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from azure.storage.blob import BlobClient

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

cookieDict = cookies[2]
#print(cookieDict)
# for cookie in cookies:
#     print(cookie)

#print(cookieDict["value"])

# Your blob URL and SAS token
blob_url = 'https://steamgraphsstorage.blob.core.windows.net/container-for-blob/cookie.txt'
sas_token = 'sp=rwd&st=2024-08-06T20:45:18Z&se=2025-09-10T04:45:18Z&spr=https&sv=2022-11-02&sr=c&sig=MKticGz9P9HPI7iXp1a6yuErc5Sv6P9fY%2FfCbxL0PLg%3D'

# Initialize the BlobClient with the SAS token
blob_client = BlobClient.from_blob_url(blob_url=blob_url, credential=sas_token)

# Overwrite the existing blob or create a new one if it doesn't exist
blob_client.upload_blob(cookieDict["value"], overwrite=True)

#print("Cookie has been updated.")