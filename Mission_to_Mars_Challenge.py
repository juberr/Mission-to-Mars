#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as soup

import pandas as pd


# In[2]:


executable_path = {'executable_path':'/Users/justinberry/Downloads/chromedriver'}
browser = Browser('chrome', **executable_path)


# In[3]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url)
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[10]:


browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[14]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df.to_html()


# ### Mars Weather

# In[15]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[16]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[17]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# ### D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[18]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[94]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# visit the url with the images we need and parse the html
# for links that lead to the high-res jpgs. save to a list.
html = browser.html
hemi_soup = soup(html,'html.parser')
hemi_links = hemisphere_soup.find_all('div', class_='item')
hemi_links = [i.find('a').get('href') for i in hemi_links]

# visit each link, save the high-res url and title to a list as a dictionary.
for i in hemi_links:
    browser.visit('https://astrogeology.usgs.gov'+ i)
    hi_res_html = browser.html
    hi_res_soup = soup(hi_res_html, 'html.parser')
    image_link = hi_res_soup.find('div',class_='downloads').find('a').get('href')
    title = hi_res_soup.find('div',class_='content').find('h2').get_text()
    hemisphere_image_urls.append({'img_url':image_link, 'title':title})
    


# In[95]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[ ]:


# 5. Quit the browser
browser.quit()

