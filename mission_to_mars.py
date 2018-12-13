
#Get dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import re

def scrape():

    #Set path to chromedriver
    executable_path = {"executable_path": "/chromedriver"}

    #Use Splinter and Beautiful soup for scraping
    browser = Browser("chrome", **executable_path, headless=False)

    #Website for news
    mars_news_url = 'https://mars.nasa.gov/news/'

    #Get HTML from browser
    browser.visit(mars_news_url)
    raw_html_news = browser.html

    #Use Beautiful Soup to parse HTML
    soup_news = BeautifulSoup(raw_html_news, 'lxml')

    #Close browser
    browser.quit()

    #Get title and text for the first news item
    news_title = soup_news.find('div', class_='content_title').get_text()
    news_p = soup_news.find('div', class_='article_teaser_body').get_text()

    #Scrape for featured image
    browser = Browser("chrome", **executable_path, headless=False)

    #Website for featured image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    raw_html_image = browser.html
    soup_image = BeautifulSoup(raw_html_image, 'lxml')
    browser.quit()

    # Get image URL
    featured_image = soup_image.find('a', class_='fancybox')
    featured_image_url = "https://www.jpl.nasa.gov/" + featured_image["data-fancybox-href"]

    browser = Browser("chrome", **executable_path, headless=False)

    #Scrape Twitter account
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    raw_html_twitter = browser.html
    soup_twitter = BeautifulSoup(raw_html_twitter, 'lxml')
    browser.quit()

    # Get weather data 
    mars_weather = soup_twitter.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()

    #Scrape Mars fact table using pandas
    mars_facts_df = pd.read_html('https://space-facts.com/mars/')
    mars_facts = str(mars_facts_df[0].to_html(index=False, header=False, border="0"))

    # Scrape the USGS Astrogeology website for Martian Hemisphere images
    #Use Splinter and Beautiful soup for scraping
    browser = Browser("chrome", **executable_path, headless=False)

    #Scrape Astrogeology website
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    raw_html_hemispheres = browser.html
    soup_hemispheres = BeautifulSoup(raw_html_hemispheres, 'lxml')

    hemispheres = soup_hemispheres.findAll('div', class_='description')
    browser.quit()

    #Loop through initial links to find download links.
    hemisphere_links = []
    for sphere in hemispheres:
        hemisphere_links.append('https://astrogeology.usgs.gov' + sphere.find('a')["href"])

    #Loop through links and download landing pages and search for full image links
    
    hemisphere_image_urls = []

    for link in hemisphere_links:
        browser = Browser("chrome", **executable_path, headless=False)
        browser.visit(link)
        html_h = browser.html
        soup_h = BeautifulSoup(html_h, 'lxml')
        temp_h = soup_h.find("div", class_="content") 
        #print(temp_h)
        hemisphere_image_urls.append({
                "title" : temp_h.find('h2').get_text(),
                "img_url" : temp_h.find('a', href=re.compile('^http://astropedia.astrogeology.usgs.gov/download/Mars/Viking'))["href"]
            })
        browser.quit()


    mars_dict = {
        "data" : True,
        "featured_image_url" : featured_image_url,
        "news_title" : news_title,
        "news_p" : news_p,
        "mars_weather" : mars_weather,
        "hemisphere_image_urls" : hemisphere_image_urls,
        "mars_facts_html" : mars_facts
    }

    return mars_dict
