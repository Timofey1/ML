import pandas as pd

#DataFrame example its like a table
pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})

pd.DataFrame({'Bob': ['I liked it.', 'It was awful.'], 'Sue': ['Pretty good.', 'Bland.']})

pd.DataFrame({'Bob': ['I liked it.', 'It was awful.'], 
              'Sue': ['Pretty good.', 'Bland.']},
             index=['Product A', 'Product B'])

#Series example like a list
pd.Series([1, 2, 3, 4, 5])
pd.Series([30, 35, 40], index=['2015 Sales', '2016 Sales', '2017 Sales'], name='Product A')

#---------------------------------------------------------------
wine_reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv")
#checking how large is data frame
wine_reviews.shape
#view the top 5 of dataFrame
wine_reviews.head()
#---------------------------------------------------------------
#Accsess to values column(list)
reviews['country']
#Accsess to values column(element)
reviews['country'][0]
#acsess to row
reviews.iloc[0]
#acsess to all rows, equals to reviews['country']
reviews.iloc[:, 0]
#acsess to first three rows
reviews.iloc[:3, 0]

#---------------------------------------------------------------
#Label-based selection
reviews.loc[0, 'country']
#all rows three columns
reviews.loc[:, ['taster_name', 'taster_twitter_handle', 'points']]
#---------------------------------------------------------------
#setting title column as index
reviews.set_index("title")
#---------------------------------------------------------------
#conditions
reviews.country == 'Italy'
#choosing every row where column is Italy
reviews.loc[reviews.country == 'Italy']
#choosing every row where column is Italy AND points more than 90
reviews.loc[(reviews.country == 'Italy') & (reviews.points >= 90)]
#OR
reviews.loc[(reviews.country == 'Italy') | (reviews.points >= 90)]
# country is france or italy
reviews.loc[reviews.country.isin(['Italy', 'France'])]
#price not null
reviews.loc[reviews.price.notnull()]
#---------------------------------------------------------------
#looking at describtion of price, You can also look at NON INT elements
reviews.points.describe()
#mean
reviews.points.mean()
#unique values of non int column
reviews.taster_name.unique()
#counting how many elements does each unique value have
reviews.taster_name.value_counts()
#---------------------------------------------------------------
#transforming info whithout changing it in main data frame
review_points_mean = reviews.points.mean()
reviews.points.map(lambda p: p - review_points_mean)

#same as map but apply func
def remean_points(row):
    row.points = row.points - review_points_mean
    return row

reviews.apply(remean_points, axis='columns')






