from pprint import pprint
import json
import os
import pandas as pd
from pandas.io.json import json_normalize
import urllib
import scrapy
from scrapy.crawler import CrawlerProcess

""" directory to run: /Users/byungjooshin/Desktop/wip/reviewstats/processing """
class ReviewProcessor:
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
        print(store_id_and_data_dataframe['businessUrl'])
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
  def get_restaurant_name_and_url(self, filepath):
    """ This generates the review urls from a single page of 30 restuarants"""

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
    #for filename in os.listdir(path):


    
    #print(normalized_data)




class ReviewSpider(scrapy.Spider):
    # Your spider definition
    name = "yelp"
    response_directory = "../../response_files"
    anchor_url = ""
    def __init__(self, anchor_url):
      self.anchor_url = anchor_url
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
      urls_to_hunt = []

      # we need to scrape the first webpage, then do an incremental scrap on all the 
      # other webpages
      param_url_encoded = urllib.parse.urlencode(PARAMS)
      URL = self.anchor_url + param_url_encoded

      url_info = []

      url_info_list = []
      
      retVal = scrapy.Request(url=url, callback=self.parse, meta=url_info)
      
      """To pass in variables to scrapy
      item = response.meta.get('hero_item')
      meta={'hero_item': item}
      """
      
      # for i in range(0, len(url_info_list), 1):
      #     url = urls_to_hunt[i]
      #     url_info = url_info_list[i]
      #     print(url_info)
      #     yield scrapy.Request(url=url, callback=self.parse, meta=url_info)

    def parse(self, response):
        url_split_arr = response.url.split("/")
        print(url_split_arr)
        # you need to remember that you have to get the link to go to the next page...
       
        # start_range = response.meta.get('start_range')
        # filename = 'test-%s-%s.json' % (page, start_range)
        # print(self.response_directory)
        # path_to_save = os.path.join(self.response_directory, filename)

        # with open(path_to_save, 'wb') as f:
        #     response_body = response.body
        #     decoded_response_body = response_body.decode("utf-8")
        #     result= re.search("\"hovercardData\":.*\"mapState",decoded_response_body)
        #     result_string_with_mapstate = result.group(0)
        #     parsable_json_string = result_string_with_mapstate.replace(",\"mapState","")
        #     parsable_json_string = parsable_json_string.replace("\"hovercardData\":", "")
        #     encoded_string = parsable_json_string.encode()
        #     f.write(encoded_string)
        # self.log('Saved file %s' % filename)


if __name__ == '__main__':
  reviewprocessor = ReviewProcessor()
  filename = "test-www.yelp.com-0.json"
  complete_path = os.path.join(reviewprocessor.response_directory, filename)
  reviewprocessor.process_reviews(complete_path)
  # process = CrawlerProcess({
  #   'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
  # })
  # process.crawl(ReviewSpider)
  # process.start() # the script will block here until the crawling is finished

