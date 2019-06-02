from pprint import pprint
import json
import os
import pandas as pd
from pandas.io.json import json_normalize
import urllib
import scrapy
from scrapy.crawler import CrawlerProcess
from os import listdir
from os.path import isfile, join
import time
import re

""" directory to run: /Users/byungjooshin/Desktop/wip/reviewstats/processing """
class RestaurantRetriever:
  """ This class retrieves the restaurants from json files that were crawled - stored in another directory"""
  response_directory = "../response_files"
  df = None
  def __init__(self):
    #Probably need to put some review function here
    self.name = "spidermonkey"

  def myfunc(self):
    print("Hello my name is " + self.name)

  # def process_json_review_files:
  #   return False
  
  def generate_dataframe_from_json(self, filename):
    """ Given a json file of resturarants, this returns a dataframe of restaurants and 
    their attributes. """
    with open(filename) as f:
        restaurants = json.load(f)
        store_dataframe_list = []
        store_id_list = []
        for store_id in restaurants:
          store_values = restaurants[store_id]
          normalized_dataframe = json_normalize(store_values)
          store_dataframe_list.append(normalized_dataframe)
          store_id_list.append(store_id)
        
        store_id_dataframe = pd.DataFrame({"id": store_id_list})
        merged_dataframe = pd.concat(store_dataframe_list)
        store_id_dataframe.reset_index(drop=True, inplace=True)
        merged_dataframe.reset_index(drop=True, inplace=True)
        
        store_id_and_data_dataframe = pd.concat([store_id_dataframe, merged_dataframe], axis = 1)
        column_values = list(store_id_and_data_dataframe.columns.values)
        """
        ['id', 'addressLines', 'businessUrl', 'categories', 'isAd', 'name', 'neighborhoods', 
        'numReviews', 'photoPageUrl', 'photoSrc', 'photoSrcSet', 'rating', 'showRecommended']
        """
        return store_id_and_data_dataframe
        
        #print(store_id_and_data_dataframe)
       
        #stored_id_dataframe = s
        #dataframe_with_id_and_values = pandas.concat([store_id_dataframe, merged_dataframe])
        #print(dataframe_with_id_and_values)
    
  def move_to_next_page(self):
    return False
  def generate_next_page_link(self, business_url):
    """ This generates the complete url of the webpage. """
    base_url = "https://www.yelp.com"
    full_url = urllib.parse.urljoin(base_url, business_url)
    return full_url
  def get_restaurant_name_and_url_dataframe(self, filepath):
    """ This generates the dataframe or business name name and http 
    url from a single page of 30 restaurants"""

    df = self.generate_dataframe_from_json(filepath)
    df_bus_name_and_url = pd.DataFrame(columns=['name', 'url'])
    for index, row in df.iterrows():
      name = row['name']
      businessUrl = row['businessUrl']
      full_url = self.generate_next_page_link(businessUrl)

      df_bus_name_and_url = df_bus_name_and_url.append\
         ({'name': name, 'url': full_url}, ignore_index=True)

    return df_bus_name_and_url
    # for businessUrl in df['businessUrl']:
    #   full_url = self.generate_next_page_link(businessUrl)
    #   print(full_url)
      

    # should probably use this for formatting
    # pprint(data)
    # with open("test_pretty", "wt") as out:
    #   pprint(data, stream=out)


  def import_datafile_to_pandas(self, filename):
    data = json.loads(filename)




class ReviewSpider(scrapy.Spider):
    # Your spider definition
    name = "yelp"
    response_directory = "../../response_files"
    anchor_url = ""
    rate = 30
    def __init__(self, anchor_url=None, rest_name = None):
      self.anchor_url = anchor_url
      self.rest_name = rest_name
      self.download_delay = 1/float(self.rate)
      super().__init__()  # python3

    def start_requests(self):

      #per every review page, yelp increments by 20 reviews
      PARAMS = {
              "start": 0
      } 

      # I put to put a regular exrpression here. end with: mapState
      #starting with: {"iconName":"IconBizhouse24","platform":"desktop" 
      #ending with: mapState
      increment = 20

      # we need to scrape the first webpage, then do an incremental scrap on all the 
      # other webpages
      param_url_encoded = urllib.parse.urlencode(PARAMS)
      first_url = self.anchor_url + "?" + param_url_encoded

      url_info = {}
      url_info['increment'] = increment
      url_info['rest_name'] = self.rest_name
      
      yield scrapy.Request(url=first_url, callback=self.first_parse, meta=url_info)

      
      """To pass in variables to scrapy
      item = response.meta.get('hero_item')
      meta={'hero_item': item}
      """
      

    def first_parse(self, response):
      """ During the first parse, you must get the total number of reviews, then 
      crawl the remaining pages"""
      url_split_arr = response.url.split("/")
      #['https:', '', 'www.yelp.com', 'biz', 'xifu-food-brooklyn?osq=Restaurantsstart=0']
      response_body = response.body
      decoded_response_body = response_body.decode("utf-8")

      #Section 1: Get the number of reviews
      # you need to remember that you have to get the link to go to the next page...
      num_reviews_matching_expression = "name=\"description\" content=\"[0-9]+"
      result= re.search(num_reviews_matching_expression,decoded_response_body)
      num_reviews_match_string = result.group(0)
      split_by_quotes = num_reviews_match_string.split("\"")
      
      #last split element is the number of reviews
      num_reviews_str = split_by_quotes[-1]
      num_reviews = int(num_reviews_str)
      print(num_reviews)
      #Section 2: Get the all the text of reviews

      review_match_expression = "{\"aggregateRating\".*}"
      review_result = re.search(review_match_expression,decoded_response_body)
      review_match_json_string = review_result.group(0)
      

      #create a folder for that restaurant name

      url_info = {}
      url_info['num_reviews'] = num_reviews


      increment = response.meta.get('increment')

      """ I guess one option is to make an item pipeline to aggregreate this into a single file
      But I don't think this is worth the hassle write now. I'm just going to write out all
      the reviews grouped into 20 pieces"""

      """ make the restaurant directory by name and save the first review json file  
      that has the first 20 reviews"""

      rest_name = response.meta.get('rest_name')
      try: 
        rest_directory = "../rest_reviews" + "/" + response.meta.get('rest_name')
        os.makedirs(rest_directory)
      except Exception as e: 
        print(e)
      

      filename = rest_name + "-" + "0.json"
      path_to_save = os.path.join(rest_directory, filename)
      with open(path_to_save, 'wb') as f:
          encoded_string = review_match_json_string.encode()
          f.write(encoded_string)


      #parse all the other files 

      PARAMS = {
         "start": 0
      } 
      url_info['rest_directory'] = rest_directory
      url_info['rest_name'] = rest_name

      indexes_to_parse = [80,
              780,
              980,
              580,
              600,
              840,
              860,
              620,
              660,
              820,
              800,
              640,
              680,
              100,
              120,
              880,
              480,
              140,
              720,
              1000,
              960,
              560,
              20,
              540,
              940,
              700,
              740,
              40,
              500,
              900,
              920,
              60,
              520,
              760]
      
      for i in range(20, num_reviews, increment):
          # url = urls_to_hunt[i]
          # url_info = url_info_list[i]
          if i in indexes_to_parse:
            PARAMS['start'] = i
            param_url_encoded = urllib.parse.urlencode(PARAMS)
            url = self.anchor_url + "&" + param_url_encoded
            url_info['start'] = i
            yield scrapy.Request(url=url, callback=self.parse, meta=url_info)

       
    def parse(self, response):
        # you need to remember that you have to get the link to go to the next page...
      print("URL: " + response.request.url)
      rest_name = response.meta.get('rest_name')
      start = response.meta.get('start')
      rest_directory = response.meta.get('rest_directory')

      filename = '%s-%s.json' % (rest_name, start)
      
      path_to_save = os.path.join(rest_directory, filename)

      with open(path_to_save, 'wb') as f:
          response_body = response.body
          decoded_response_body = response_body.decode("utf-8")

          review_match_expression = "{\"aggregateRating\".*}"
          review_result = re.search(review_match_expression,decoded_response_body)
          review_match_json_string = review_result.group(0)
          
          encoded_string = review_match_json_string.encode()
          f.write(encoded_string)
      self.log('Saved file %s' % filename)
      






def crawl_one_url(single_url, name):
  process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
  })
  process.crawl(ReviewSpider, anchor_url= single_url, rest_name = name)
  process.start() 

if __name__ == '__main__':
  reviewprocessor = RestaurantRetriever()

  mypath = "../response_files"
  onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
  print(onlyfiles)
  print(len(onlyfiles))

  """ Because it was 16 pages of reviews, I separated them out by idx of the list
  However, this is not scalable. Either you use a process outside of this file, 
  or abstract out the crawler logic to uses a different crawler class.
  """

  

#did 9 - 10, start with 10 - 11
  # for file_idx in range(0, 16, 1):
  #   filename = onlyfiles[file_idx]
  #   if filename == "test-www.yelp.com-0.json":
  #     continue
  #   complete_path = os.path.join(reviewprocessor.response_directory, filename)

  #   rest_name_and_url_df = reviewprocessor.get_restaurant_name_and_url_dataframe(complete_path)
  #   process = CrawlerProcess({
  #       'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
  #     })
  #   for index, row in rest_name_and_url_df.iterrows():
  #     single_url = row['url']
  #     name = row['name']
  #     if index == 0:
  #       continue
  # process = CrawlerProcess({
  #   'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
  # })

  #     process.crawl(ReviewSpider, anchor_url= single_url, rest_name = name)
  # process.start() # the script will block here until the crawling is finished
  missing_url = 'https://www.yelp.com/biz/julianas-pizza-brooklyn-5?osq=Restaurants'
  name = 'Juliana’s Pizza'
  crawl_one_url(missing_url, name)



"""
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-80.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-780.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-980.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-580.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-600.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-840.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-860.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-620.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-660.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-820.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-800.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-640.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-680.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-100.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-120.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-880.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-480.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-140.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-720.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-1000.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-960.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-560.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-20.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-540.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-940.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-700.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-740.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-40.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-500.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-900.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-920.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-60.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-520.json
../rest_reviews/Juliana’s Pizza/Juliana’s Pizza-760.json
  def crawl_one_restaurant():
"""
