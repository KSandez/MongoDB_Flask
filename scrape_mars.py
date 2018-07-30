# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from selenium import webdriver
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    browser = init_browser()
    mars = {}

# # Step 1- Scraping for... 

# # NASA Mars News

# URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    response = requests.get(nasa_url)
    print(response)

    soup = bs(response.text, 'html.parser')
    print(soup)

# Print latest headline
    title = soup.find_all('div', class_="content_title")[0].text.strip()
    title

#  Print latest headline's paragraph
    paragraph = soup.find_all("div", class_="rollover_description_inner")[0].text.strip()
    paragraph


# # JPL Mars Space Images - Featured Image

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    items = soup.find("div",{"class":"carousel_items"})
    featured_img = items.find("article")
    featured_image_url = 'http://www.jpl.nasa.gov'+featured_img['style'].split(':')[1].split('\'')[1]
    print(featured_image_url)


# # Mars Weather

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')

    mars_twitter = weather_soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    mars_weather = []
    for twitter in mars_twitter:
        if "Sol" in str(twitter):
            mars_weather.append(twitter.text)
    mars_weather[0]


# # Mars Facts

    marsfacts_url = "https://space-facts.com/mars/"

    mars_html = requests.get(marsfacts_url)
    soup = bs(mars_html.text, 'html.parser')
    
    table_scrape = soup.find_all("table", id="tablepress-mars")[0]

    table_dict = []

    for x in table_scrape.find_all("tr"):
       entry = x.text.strip().split(":")
       table_dict.append({
            "Description": entry[0],
            "Value": entry[1]
          })

    table_df = pd.DataFrame(table_dict)

    # tables = pd.read_html(marsfacts_url)
    # tables

    # type(tables)

    # table_dict = pd.DataFrame(tables[0], columns = ['Description','Fact'])
    # table_dict

    # html_table = table_dict.to_html('mars_facts.html', index=False, border = '1', justify = 'center')
    # html_table

# # Mars Hemispheres

    hemisphere_urls  = [
       "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced",
       "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced",
       "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced",
       "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"]

    hemisphere_image_urls = []

    for url in hemisphere_urls:
        html = requests.get(url)
        soup = bs(html.text, 'html.parser')
    
        img_url = "https://astrogeology.usgs.gov" + soup.find_all("img", class_="wide-image")[0].attrs["src"]
        title = soup.find_all("h2", class_="title")[0].text[:-9]
    
        hemisphere_image_urls.append({
            "title": title,
            "img_url": img_url
        })
    hemisphere_image_urls

# Dictionary for mars scraped data from mission to mars notebook
    mars = {
        "title": title,
        "paragraph": paragraph,
        "featured_image": featured_image_url,
        "weather": mars_weather,
        "mars_facts": table_dict,
        "hemispheres": hemisphere_image_urls
      }
    return mars