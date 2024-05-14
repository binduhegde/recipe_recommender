import time
from config import chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

recipes = {}

with open('recipe_links.txt', 'r') as file:
    links = file.readlines()

for i in range(len(links)):
    links[i] = links[i][:-1]

i = 0
for link in links[900:]:

    chrome_driver.get(url=link)
    wait = WebDriverWait(chrome_driver, 15)

    try:
        name = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'recipe-name'))
        ).text
    except:
        name = None

    try:
        # Similarly, wait for other elements to be present
        likes = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'tips-score-heading'))
        ).text
    except:
        likes = None

    try:
        time = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'recipe-time-container'))
        ).text
    except:
        time = None

    try:
        servings = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'servings-display'))
        ).text
    except:
        servings = None

    try:
        ingredients = wait.until(
            EC.visibility_of_all_elements_located(
                (By.CLASS_NAME, 'ingredient'))
        )
        ingredients = '; '.join([i.text for i in ingredients])

    except:
        ingredients = None

    try:
        nutri_button = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'nutrition-button'))
        )
        nutri_button.click()

        # Wait for the nutrition details to be present
        nutritions_div = wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'nutrition-details'))
        )
        nutritions_lst = nutritions_div.find_elements(
            By.CLASS_NAME, 'list-unstyled')
        nutritions = [i.text for i in nutritions_lst][0]
    except:
        nutritions = None

    recipes[name] = {
        'likes': likes,
        'time': time,
        'servings': servings,
        'ingredients': ingredients,
        'nutritions': nutritions,
        'link': link
    }
    print(i)
    i += 1
    # print('name')
    # print(name)
    # print('-'*20)
    # print()

    # print('likes')
    # print(likes)
    # print('-'*20)
    # print()

    # print('time')
    # print(time)
    # print('-'*20)
    # print()

    # print('servings')
    # print(servings)
    # print('-'*20)
    # print()

    # print('ingredients')
    # print(ingredients)
    # print('-'*20)
    # print()

    # print('nutritions')
    # print(nutritions)
    # print('-'*20)

df = pd.DataFrame(recipes).T
df.to_csv('recipes10.csv')
