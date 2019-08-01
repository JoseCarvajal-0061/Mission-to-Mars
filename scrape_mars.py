from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
import requests
import pandas as pd
import time

##setting up mongodb

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
mars_data = client.mars_db



def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe' }
    browser = Browser('chrome', **executable_path, headless=False)



def mars_scrape():
    print("---scraping mars news website---")
    browser = init_browser()

    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)

    mars_html = browser.html
    soup = BeautifulSoup(mars_html, 'html.parser')
    
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    print(news_title)
    print(news_p)

    print("---scraping jet propulsion library images---")


    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    jpl_image = browser.html
    soup = BeautifulSoup(jpl_image, 'html.parser')

    featured_image_url  = soup.find('article', class_= "carousel_item")['style'] 
    print(featured_image_url)

    img_url = featured_image_url.split("'")[1]

    url = 'https://www.jpl.nasa.gov'
    jpl_featured_image_url = url + img_url
    
    print(jpl_featured_image_url)

    print("---scraping mars weather twitter")

    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)

    mars_html_weather = browser.html
    
    soup = BeautifulSoup(mars_html_weather, 'html.parser')

    latest_mars_weather_tweet = soup.find_all('p', class_='TweetTextSize') 
    
    for tweet in latest_mars_weather_tweet:
        mars_weather = tweet.text 
        print(mars_weather)
    break
    
    else:
        pass

    print("---scraping mars facts---")

    url = 'https://space-facts.com/mars/'
    
    mars_table = pd.read_html(url)

    mars_table[1]

    mars_table_df = pd.DataFrame(mars_table[1])

    mars_table_df.columns=['Record', 'Figures']
    
    mars_table_df

    marsfacts_html = mars_table_df.to_html(header=False, index=False)
    marsfacts_html

    print("---scraping mars hemisphere images---")

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html_hemispheres = browser.html
    hemisphere_parser = BeautifulSoup(html_hemispheres, 'html.parser')

    hemisphere_info = hemisphere_parser.find_all('div', class_='item')

    hemisphere_image_urls = []

    for item in hemisphere_info:
        title = item.find('h3').text    
        
        images_link = item.find('a', class_='itemLink product-item')['href']
        
        hemisphere_url = 'https://astrogeology.usgs.gov'
    
        browser.visit(hemisphere_url + images_link)
    
        hemisphere_images_html = browser.html
    
        image_parser = BeautifulSoup(hemisphere_images_html, "html.parser")
    
        img_first_step = image_parser.find("div", class_="downloads")                                         
    
        img_urls =  img_first_step.find("a")["href"]
        
        all_hemisphere_img_urls = hemisphere_url +  img_urls
    
        hemisphere_image_urls.append({"title": title, "Image_Links":  all_hemisphere_img_urls })
    
    print(hemisphere_image_urls)

    mars_scraped_data = {
    'news_title': news_title,
    'news_blurb': news_p,
    'featured_image': jpl_featured_image_url,
    'mars_weather_text': mars_weather,
    'mars_facts': mars_table_df,
    'mars_hemispheres_imgs': hemisphere_image_urls
    }
        
    return mars_scraped_data

## adding the scraped data to my mongo database 
db.insert(mars_data)













    