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
    df=tables[1]
    df.head()
    df = df.rename(columns = {0:'Diameter', 1:'Mass'})
    html_table = df.to_html()
    results['html_table'] = html_table

    # Mars Hemispheres
    url='https://marshemispheres.com/'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    results = soup.find_all('div', class_='description')
    hemisphere_image_urls=[]
    for result in results:
        if result.h3:
            title=result.h3.text
        a = result.find('a')
        if a['href']:
            page_url=a['href']
            image_url=url+page_url
            browser.visit(image_url)
            image_html=browser.html
            soup=bs(image_html, 'html.parser')
            result=soup.find_all('li')[1]
            full_image=result.a['href']
            img_url=url+full_image
        dic = dict({"title":title, "img_url":img_url})
        hemisphere_image_urls.append(dic)
    results['hemisphere_image_urls'] = hemisphere_image_urls
   
    # Quit the browser
    browser.quit()
    
    return results