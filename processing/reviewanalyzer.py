
from os import listdir
from os.path import isfile, isdir, join
import pandas as pd
import json
#This brings you to a review directory with all the 
review_directory = "../rest_reviews"

directories = [f for f in listdir(review_directory) if isdir(join(review_directory, f))]

review_df = pd.DataFrame(columns=['restaurant_name', 'ratingValue', 'datePublished', 'description', 'author'])

incomplete_data = []

for directory in directories:
    directory_path = join(review_directory, directory)
    files = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    # print(files)
    """ Sample review looks like this:
    "review": [{"reviewRating": {"ratingValue": 3}, "datePublished": "2019-04-05", 
    "description": "I saw this chain featured on a \"Best Pizzas in NY\" 
    YouTube video and am glad I got to stop in for a couple slices just before closing! 
    Amazing thin crust cheese with really sweet tomato sauce. \n\n3 *'s \n+$1 slice\n-
    Sweeeeeet Sauce\n\nYT Erik Wade", "author": "Haywood J."}, 
    """

    for filename in files:
        filepath = join(directory_path, filename)
        with open(filepath, 'r') as f:
            
            json_content = f.read()
            # print(json_content)
            try: 
                json_review_collection = json.loads(json_content)
            except Exception as exception:
                print(filepath)
            # reviews = json_review_collection['review']
            # for review in reviews:
            #     reviewRating = review['reviewRating']
            #     datePublished = review['datePublished']
            #     description = review['description']
            #     author = review['author']
            #     review_df = review_df.append({'restaurant_name':directory, 'ratingValue':reviewRating, 'datePublished':datePublished, 'description':description, 'author':author}, ignore_index=True)

 
    # d = json.loads(j)
    # review_df = review_df.append\
    #       ({'restaurant_name':, 'ratingValue', 'datePublished', 'description', 'author']}, ignore_index=True)

review_df.to_pickle('bridge_street_rest_data.pkl') 
