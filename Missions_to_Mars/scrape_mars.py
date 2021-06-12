#dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    results = {}
    #NASA Mars News
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    results['news_title'] = news_title
    results['news_p'] = news_p

    # Scraping https://spaceimages-mars.com/
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html=browser.html
    soup=bs(html, 'html.parser')
    result = soup.find('a', class_='showimg fancybox-thumbs')
    href= result['href']
    featured_image_url = 'https://spaceimages-mars.com/' + href
    results['featured_image_url'] = featured_image_url

    ## Mars Fact
    url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url)
    df = tables[0]
    df = df.rename(columns = {0:'Description', 1:'Mars', 2:'Earth'})
    df.set_index('Description', inplace=True)
    html_table = df.to_html()
    results['html_table']=html_table

    # Mars Hemispheres
    url='https://marshemispheres.com/'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    images = soup.find_all('div', class_='description')
    hemisphere_image_urls=[]
    for image in images:
        if image.h3:
            title=image.h3.text
            a = image.find('a')
        if a['href']:
            page_url=a['href']
            image_url=url+page_url
            browser.visit(image_url)
            image_html=browser.html
            soup=bs(image_html, 'html.parser')
            image=soup.find_all('li')[0]
            full_image=image.a['href']
            img_url=url+full_image
            dic = dict({"title":title, "img_url":img_url})
            hemisphere_image_urls.append(dic)
    results["image_urls"]=hemisphere_image_urls
    
        # Quit the browser
    browser.quit()
    return results