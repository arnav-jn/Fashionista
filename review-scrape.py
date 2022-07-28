from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import re
import numpy as np

# The url for flipkart>tshirts OR Skirts OR Dresses. Can replace with any other product category
url = "https://www.flipkart.com/clothing-and-accessories/dresses-and-gown/dress/women-dress/pr?sid=clo,odx,maj,jhy&otracker=categorytree&otracker=nmenu_sub_Women_0_Dresses"
x = requests.get(url)
soup = bs(x.content, "html.parser")

page = soup.findAll("a", {"class": "ge-49M"})


# Getting links for all pages. Each page has 40 items
page_links = []
for p in page:
    page_links.append(p.get('href'))
page_links = ['http://flipkart.com' + p for p in page_links]

print("yes")

# Getting individual product links of all t shirts listed (400)
linkss = []
for p in page_links:
    url = p
    x = requests.get(url)
    soup = bs(x.content, "html.parser")
    links = soup.findAll("a", {"class": "IRpwTa"})
    for link in links:
        linkss.append('http://flipkart.com' + link.get('href'))

len(linkss)
#testing
print(linkss[0])

# Extracts the following features from each item and stores them in a list, to be stored as dataframe later on
urls = []
brands = []
item_names = []
disc_prices = []
mrp_prices = []
stars = []
ratings = []
reviews = []
text_reviews = []
type_ = []
sleeve_ = []
fit_ = []
fabric_ = []
neck_ = []
pattern_ = []
brand_fit_ = []
brand_color_ = []

shirts = linkss

for i in range(len(shirts)):

    try:
        print(i)
        url = shirts[i]
        x = requests.get(url)
        soup = bs(x.content, "html.parser")
        # print("starting")
        brand = soup.findAll("span", {"class": "G6XhRU"})[0].text
        # print("brand done")
        item = soup.findAll("span", {"class": "B_NuCI"})[0].text
        # print("item done")
        disc_price = soup.findAll("div", {"class": "_30jeq3 _16Jk6d"})[0].text
        # print("discount done")
        mrp = soup.findAll("div", {"class": "_3I9_wc _2p6lqe"})[0].text
        # print("mrp done")
        star = soup.findAll("div", {"class": "_3LWZlK _3uSWvT"})[0].text
        # print("star done")
        rating_number = soup.findAll("span", {"class": "_2_R_DZ"})[0].text
        ratings_num = (rating_number[0:rating_number.find('ratings') - 1])
        # print("rating done")

        reviews_num = rating_number[rating_number.find('and') + 4:rating_number.find('reviews') - 1]

        review = []
        x = soup.findAll("div", {"class": "_6K-7Co"})
        for i in range(len(x)):
            review.append(x[i].text)

        feat = soup.findAll("div", {"class": "col col-3-12 _2H87wv"})
        feat_ans = soup.findAll("div", {"class": "col col-9-12 _2vZqPX"})
        # print("product details  arrived")
        features = {}
        for x in range(len(feat)):
            features[feat[x].text] = feat_ans[x].text
        urls.append(url)
        brands.append(brand)
        item_names.append(item)
        disc_prices.append(disc_price)
        mrp_prices.append(mrp)
        stars.append(star)
        ratings.append(ratings_num)
        reviews.append(reviews_num)
        text_reviews.append(review)
        # print("product details  arrived part 2")
        type_.append(features['Type'])
        # print("type done")
        try:
            sleeve_.append(features['Sleeve'])
        except:
            sleeve_.append(features['Sleeve Length'])
        # print("sleeve done")
        # fit_.append(features['Fit'])
        fabric_.append(features['Fabric'])
        # print("fabric done")
        neck_.append(features['Neck'])
        # print("neck done")
        pattern_.append(features['Pattern'])
        # print("pattern done")
        # brand_fit_.append(features['Brand Fit'])
        # brand_color_.append(features['Brand Color'])
    except:
        print("Incomplete details for item" + str(i) + url)

# convert ratings,reviews, stars to int and floats for easy calculation later
y = [int(r.replace(',', '')) for r in ratings]
ratings = y
reviews = [(r.replace(',', '')) for r in reviews]
stars = [float(r) for r in stars]

# creating a dataframe and saving it to csv
table = {'URL': urls, 'BRAND': brands, 'ITEM': item_names, 'DISCOUNTED PRICE': disc_prices, 'MRP': mrp_prices,
         'STARS': stars, 'NUMBER OF RATINGS': ratings, 'NUMBER OF REVIEWS': reviews, 'LIST OF REVIEWS': text_reviews}
df = pd.DataFrame(table)
df.to_csv(r'dress-flipkart-final-final.csv')





