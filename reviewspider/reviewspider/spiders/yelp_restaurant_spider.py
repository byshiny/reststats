import scrapy
import urllib.parse
import re
import os
import json
"""
Given a list of restaurant links, this scraper gets all the reviews and organizes them by 
name
"""

class RestaurantSpider(scrapy.Spider):
    name = "restaurant"
    response_directory = "../../response_files"

    def start_requests(self):

        PARAMS = {'find_desc': "Restaurants",
                #'find_loc': "Downtown Brooklyn",
                "start": 0,
                "end": 1000,
                "l": "g:-73.9982414246,40.6838924509,-73.9726638794,40.7034156679"
        } 

        # I put to put a regular exrpression here. end with: mapState
        #starting with: {"iconName":"IconBizhouse24","platform":"desktop" 
        #ending with: mapState

        start_range = 0
        stop_range = 1000
        increment = 30
        urls_to_hunt = []


        
        #Yelp  has 30 resturants per page
        url_info_list = []

        for i in range(start_range, stop_range, increment):
            PARAMS["start"] = i
            param_url_encoded = urllib.parse.urlencode(PARAMS)
            URL = 'https://www.yelp.com/search?' + param_url_encoded
            # sending get request and saving the response as response object 
            urls_to_hunt.append(URL)
            url_info = {}
            url_info['website'] = 'yelp'
            url_info['type'] = 'restaurants'
            url_info['start_range'] = i
            url_info_list.append(url_info)

        
        
        #'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Downtown%20Brooklyn%2C%20Brooklyn%2C%20NY&l=g%3A-73.9982414246%2C40.6838924509%2C-73.9726638794%2C40.7034156679&start=0&end=450'
        """To pass in variables to scrapy
        item = response.meta.get('hero_item')
        meta={'hero_item': item}
        """
        
        for i in range(0, len(url_info_list), 1):
            url = urls_to_hunt[i]
            url_info = url_info_list[i]
            print(url_info)
            yield scrapy.Request(url=url, callback=self.parse, meta=url_info)

    def parse(self, response):
        page = response.url.split("/")[-2]
        # you need to remember that you have to get the link to go to the next page...
       
        start_range = response.meta.get('start_range')
        filename = 'test-%s-%s.json' % (page, start_range)
        print(self.response_directory)
        path_to_save = os.path.join(self.response_directory, filename)

        import json

d = json.loads(j)

        with open(path_to_save, 'wb') as f:
            response_body = response.body
            decoded_response_body = response_body.decode("utf-8")
            result= re.search("\"hovercardData\":.*\"mapState",decoded_response_body)
            result_string_with_mapstate = result.group(0)
            parsable_json_string = result_string_with_mapstate.replace(",\"mapState","")
            parsable_json_string = parsable_json_string.replace("\"hovercardData\":", "")
            encoded_string = parsable_json_string.encode()
            f.write(encoded_string)
        self.log('Saved file %s' % filename)




