from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for efficiency
chrome_options.add_argument("--disable-gpu")
# service = Service("/path/to/chromedriver")  # Replace with the correct path to chromedriver

driver = webdriver.Chrome(options=chrome_options)

# iFrame source URL (embedded post)
iframe_url = '<iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2FABA.Bank.Cambodia%2Fposts%2Fpfbid02WWbgbTkGydMu2E5EFjMkLvdAKhvZFDvyMrVVvdP9L4CKqXyy5s5NQuNJcLLVXVXFl&show_text=true&width=500" width="500" height="738" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>'

# Open the iFrame URL
driver.get(iframe_url)

# Wait for the content to load
driver.implicitly_wait(10)

# Extract content from the iFrame
try:
    # Example: Extract the post content
    post_content = driver.find_element(By.CSS_SELECTOR, ".userContent").text
    print("Post Content:", post_content)

    # Example: Extract likes or comments (if available)
    likes = driver.find_element(By.CSS_SELECTOR, ".UFILikeSentenceText").text
    print("Likes:", likes)

except Exception as e:
    print("Error extracting data:", e)

# Close the browser
driver.quit()
