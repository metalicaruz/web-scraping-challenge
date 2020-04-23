#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import dependencies
from splinter import Browser
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import time


# # NASA Mars News

# In[ ]:


# Launch site and use BeautifulSoup to parse
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:


# Visit Nasa news url through splinter module
url_news = "https://mars.nasa.gov/news/"
browser.visit(url_news)


# In[ ]:


# HTML Object
html_news = browser.html
soup = bs(html_news, "html.parser")

# Scrape the latest News Title and Paragraph Text
news_date = soup.find("div", class_ = "list_date").text
news_title = soup.find("div", class_ = "content_title").text
news_paragraph = soup.find("div", class_ = "article_teaser_body").text

# Display scrapped news 
print(news_date)
print(news_title)
print(news_paragraph)


# # JPL Mars Space Images - Featured Image

# In[ ]:


# Visit JPL Featured Space Image url through splinter module
url_spaceimage = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url_spaceimage)


# In[ ]:


# HTML Object
img_html = browser.html
img_soup = bs(img_html, "html.parser")


# In[ ]:


# Find image url to the full size
featured_image = img_soup.find("article")["style"].replace('background-image: url(','').replace(');', '')[1:-1]

# Display url of the full image
featured_image_url = f"https://www.jpl.nasa.gov{featured_image}"
print("JPL Featured Space Image")
print("-----------------------------------------")
print(featured_image_url)


# # Mars Weather - Twitter

# In[ ]:


# Visit the Mars Weather twitter account through splinter module
# Scrape the latest Mars weather tweet from the page
url = "https://twitter.com/marswxreport?lang=en"
response = requests.get(url)
soup = bs(response.text, 'html.parser')
mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print("Mars Weather")
print("------------------------------------------------------------------------")
print(mars_weather)


# # Mars Facts

# In[ ]:


# Visit the Mars Facts webpage and use Pandas to scrape the table
url_facts = "https://space-facts.com/mars/"

# Use Pandas - read_html - to scrape tabular data from a page
mars_facts = pd.read_html(url_facts)
mars_facts


# In[ ]:


mars_df = mars_facts[0]

# Create Data Frame
mars_df.columns = ["Description", "Value"]

# Set index to Description
mars_df.set_index("Description", inplace=True)

# Print Data Frame
mars_df


# In[ ]:


# Save html code to a file
html_table = mars_df.to_html()

# Strip unwanted newlines to clean up the table
html_table.replace("\n", '')

# Save html code
mars_df.to_html("mars_facts_data.html")


# In[ ]:


html_table = mars_df.to_html(classes = 'table table-striped')
print(html_table)


# # Mars Hemispheres

# In[ ]:


# Visit the USGS Astrogeology site
hem_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
hem_response = requests.get(hem_url)
hem_soup = bs(hem_response.text, 'html.parser')

results = hem_soup.find_all('div', class_='item')
print(results)


# In[ ]:


hem_img_urls = []

for result in results:
    
    title = result.find('h3').text
    
    single_url = 'https://astrogeology.usgs.gov' + result.find('a', class_='itemLink product-item')['href']
    single_response = requests.get(single_url)
    single_soup = bs(single_response.text, 'html.parser')
    
    img_url = single_soup.find('img', class_='wide-image')['src']
    
    hem_img_urls.append({"title" : title, "img_url" : f'https://astrogeology.usgs.gov{img_url}'})
    
# Store data in a dictionary
    mars_data = {
        "news_date":news_date,
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": html_table,
        "hem_img_urls": hem_img_urls}

# Close the browser after scraping
browser.quit()        