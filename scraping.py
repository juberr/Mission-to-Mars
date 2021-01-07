from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try: 
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None


    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    return df.to_html(classes=('table')).replace("dataframe ", "")

def hemi_images(browser):

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls = []
    # visit the url with the images we need and parse the html
    # for links that lead to the high-res jpgs. save to a list.
    html = browser.html
    hemi_soup = soup(html,'html.parser')

    try:
        hemi_links = hemi_soup.find_all('div', class_='item')
    except AttributeError:
        return None

    hemi_links = [i.find('a').get('href') for i in hemi_links]

    # visit each link, save the high-res url and title to a list as a dictionary.
    for i in hemi_links:
        browser.visit('https://astrogeology.usgs.gov'+ i)
        hi_res_html = browser.html
        hi_res_soup = soup(hi_res_html, 'html.parser')
        image_link = hi_res_soup.find('div',class_='downloads').find('a').get('href')
        title = hi_res_soup.find('div',class_='content').find('h2').get_text()
        hemisphere_image_urls.append({'img_url':image_link, 'title':title})

    return hemisphere_image_urls

def scrape_all():
    exec_path = {'executable_path':'/Users/justinberry/Downloads/chromedriver'}
    browser = Browser("chrome", **exec_path, headless=True)
    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemi_images(browser),
        "last_modified": dt.datetime.now()
    }
    
    browser.quit()

    return data

if __name__ == "__main__":
    print(scrape_all())

