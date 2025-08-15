from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# Open webpage with iframe
iframe_url = '<iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2FABA.Bank.Cambodia%2Fposts%2Fpfbid02WWbgbTkGydMu2E5EFjMkLvdAKhvZFDvyMrVVvdP9L4CKqXyy5s5NQuNJcLLVXVXFl&show_text=true&width=500" width="500" height="738" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>'

driver.get(iframe_url)

# Switch to iframe
iframe = driver.find_element(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframe)

# Try locating elements (depends on iframe's content accessibility)
try:
    comments = driver.find_elements(By.CSS_SELECTOR, ".comment-class")
    for comment in comments:
        print(comment.text)
except Exception as e:
    print(f"Error: {e}")

driver.quit()
