
from os import listdir
from os.path import isfile, isdir, join
import pandas as pd
import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    review_df = pd.read_pickle('bridge_street_rest_data.pkl')
    #print(review_df['ratingValue'][0]['ratingValue'])

    #This is a tech debt item - need to remove later.
    mean = review_df.ratingValue.apply(lambda x : sum(x.values())).mean()
    #mean rating is a 3.709987361406331
    stdev = review_df.ratingValue.apply(lambda x : sum(x.values())).std()

    for index, row in review_df.iterrows():
        rating = row['ratingValue']['ratingValue']
        row['ratingValue'] = float(rating)
    #1.3200255144385469
    
    restaurants_and_ratings = review_df[['restaurant_name', 'ratingValue']]
    restaurants_and_ratings = restaurants_and_ratings.convert_objects(convert_numeric=True)
    restaurant_average_rating = restaurants_and_ratings.groupby('restaurant_name').mean().reset_index()
    # restaurant_average_rating = restaurant_average_rating.set_index(['restaurant_name', 'ratingValue'])
    # print(restaurant_average_rating.keys())
    restaurant_average_rating_sorted = restaurant_average_rating.sort_values(by = 'ratingValue', ascending=False)

    rating_count_dict = {}
    for index, row in restaurant_average_rating_sorted.iterrows():
        rating = row['ratingValue']
        rating = round(rating * 2) / 2
        if rating not in rating_count_dict:
            rating_count_dict[rating] = 0
        else:
            rating_count_dict[rating] += 1

    print(rating_count_dict)

    # plt.xlabel('Review Ratings to Nearest 0.5')
    # plt.ylabel('Review Count')
    # plt.title('Average Restaurant Rating of 1 Mile Radius of Downtown Brooklyn')
    # plt.bar(rating_count_dict.keys(), rating_count_dict.values(), align='edge', width=0.3)
    # plt.show()
    # plt.bar(restaurant_average_rating_sorted_rounded.keys(), restaurant_average_rating_sorted_rounded.values(), align='center')
    # restaurant_average_rating_sorted_rounded.plot.bar(x='restaurant_name', y='ratingValue', rot=0)
    # # plt.show()

    print(restaurant_average_rating_sorted[['restaurant_name', 'ratingValue']].head(50).to_csv())
    # restaurant_average_rating_sorted_rounded.plot.line()
    # # restaurant_average_rating_sorted.plot.bar(restaurant_average_rating)
    # print(restaurant_average_rating_sorted.head(20))
    # restaurants_and_ratings['ratingValue'] = restaurants_and_ratings['ratingValue']['ratingValue']
    # print(type(review_df['ratingValue'][0]))
    # print(type(restaurants_and_review[0]))
    # print(restaurants_and_review_counts.keys())
    # plt.xlabel('Review Ratings')
    # plt.ylabel('Average Restaurant Review')
    # plt.title('Restaurants 1 Mile Radius of Downtown Brooklyn')
    # sorted_ascending_restaurants_and_review_counts = restaurants_and_review_counts.sort_values(ascending=False)
    # print(sorted_ascending_restaurants_and_review_counts.head(20).to_csv())
    # plt.plot()
    # plt.show()
    # plt.xlabel('Restaurants')
    # plt.ylabel('Number of Reviews')
    # plt.title('Restaurants 1 Mile Radius of Downtown Brooklyn')
    # plt.bar(restaurants_and_review_counts.keys(), restaurants_and_review_counts.values(), align='center')
    # plt.show()





def generate_histogram_of_all_reviews():
    rating_map = {}
    for index, row in review_df.iterrows():
        rating = row['ratingValue']['ratingValue']
        if rating not in rating_map:
            rating_map[rating] = 1
        else:
            rating_map[rating] += 1
    plt.xlabel('Review Rating')
    plt.ylabel('Number of Reviews')
    plt.title('Reviews in a 1 Mile Radius of Downtown Brooklyn')
    plt.bar(rating_map.keys(), rating_map.values(), align='center')
    plt.show()


def generate_review_dataframe_and_save():
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
                json_review_collection = json.loads(json_content)
                reviews = json_review_collection['review']
                for review in reviews:
                    reviewRating = review['reviewRating']
                    datePublished = review['datePublished']
                    description = review['description']
                    author = review['author']
                    review_df = review_df.append({'restaurant_name':directory, 'ratingValue':reviewRating, 'datePublished':datePublished, 'description':description, 'author':author}, ignore_index=True)

    
        # d = json.loads(j)
        # review_df = review_df.append\
        #       ({'restaurant_name':, 'ratingValue', 'datePublished', 'description', 'author']}, ignore_index=True)

    review_df.to_pickle('bridge_street_rest_data.pkl') 
