from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

def init_browser():
    executable_path = {"executable_path": "c:/bin/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News

    news_url = "http://mars.nasa.gov/news"
    # Use splinter because the site redirects.
    browser.visit(news_url)
    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")

    news_item = soup.find('div', class_='list_text')

    news_title = news_item.find('div', class_='content_title').text.strip()

    news_teaser = news_item.find('div', class_='article_teaser_body').text.strip()

    # JPL Mars Space Images

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(5)

    click_one = browser.links.find_by_partial_text('FULL IMAGE')
    click_one.click()

    click_two = browser.links.find_by_partial_text('more info')
    click_two.click()

    html = browser.html
    soup = bs(html, "html.parser")

    four = soup.find('figure', class_='lede')
    five = four.find('a')['href']
    featured_image_url = "https://jpl.nasa.gov/" + five

    # Mars Facts

    table_url = "https://space-facts.com/mars/"
    time.sleep(5)
    tables = pd.read_html(table_url)
    facts_table = tables[0]
    facts_table = facts_table.rename(columns={0:"About",1:"Mars"})

    facts_html = facts_table.to_html(index=False)
    facts_html = facts_html.replace("text-align: right;","text-align: center;")

    # Mars Hemipsheres
    
    hemi_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    time.sleep(5)

    html = browser.html
    soup = bs(html, 'lxml')

    hemispheres = soup.find_all('h3')

    hemi_images = []
    for hemisphere in hemispheres:
        hemi_dict = {}
        name = hemisphere.text
        name = name.replace(" Enhanced","")
        hemi_dict["hemi"] = name
        browser.links.find_by_partial_text(name).click()
        hemi_dict["image"] = browser.find_by_text("Sample")["href"]
        hemi_images.append(hemi_dict)
        browser.back()

    browser.quit()

    mars_dict = {"news_title":news_title,"news_teaser":news_teaser,"featured":featured_image_url,
             "facts_table":facts_html,"hemispheres":hemi_images}
    
    return mars_dict