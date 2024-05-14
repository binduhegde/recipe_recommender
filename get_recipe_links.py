import time
from config import chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# website for vegan recipes
url = 'https://tasty.co/tag/vegan'

chrome_driver.get(url=url)

# will store all the links of food recipes
all_links = []

# returns a list of all the food recipe links in the current page.
# We call it after we've loaded all the items
def current_page_links():
    result = []
    # WebElement of a list item which has 'a' tag and href
    feed_items = chrome_driver.find_elements(By.CLASS_NAME, 'feed-item')

    # extracing hrefs from all the list items
    for item in feed_items:
        link_element = item.find_element(By.TAG_NAME, 'a')
        href_value = link_element.get_attribute('href')

        result.append(href_value)

    return result
    
# clicks the show more button
def load_more():
    class_name = 'show-more-button'
    show_more_button = chrome_driver.find_element(By.CLASS_NAME, class_name)
    show_more_button.click()
    # sleep for 6 secs so that the page can load before clicking this button again
    time.sleep(6)

# in one page, there are 20 food recipes.
# when we click show-more, 20 more are loaded
# so 50 times 20 would give us 1000 recipes
# plus 20 we already had
for i in range(50):
    print(i)
    load_more()

all_links += current_page_links()

# write all the links to this txt file
with open('recipe_links.txt', 'w') as f:
    for line in all_links:
        f.write(f"{line}\n")