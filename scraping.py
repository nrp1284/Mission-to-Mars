# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 


# set executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# assign the url and instruct the browser to visit it.
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page, 
# This is searching for elements with a specific combination of tag (div) and attribute (list_text). 
browser.is_element_present_by_css('div.list_text', wait_time=1)


# set up the HTML parser
# assigned slide_elem as the variable to look for the <div /> tag and its descendent 
# The . is used for selecting classes, such as list_text,
# so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text.
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# we need to get just the text, and the extra HTML stuff isn't necessary
# Use the parent element to find the first `a` tag , create new variable for the title and save it as `news_title` 
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text,
# output should only be the summary of the article.

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images
# scraping code will be to gather the featured images from the Jet Propulsion Laboratory's Space Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# look at the button's HTML tags and attributes with the DevTools.
# the <button> element has a two classes (btn and btn-outline-light) and a string reading "FULL IMAGE".

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image.
# Find the relative image url
# An img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image.
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# scrape the entire table with Pandas' .read_html() function
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# convert our DataFrame back into HTML-ready code using the .to_html() function
df.to_html()

# turning off browser while not using to scrap data
browser.quit() 






