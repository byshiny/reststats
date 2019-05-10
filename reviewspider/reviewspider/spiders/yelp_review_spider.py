import scrapy
import urllib.parse
import re
import os

"""Instructions: Go to /Users/byungjooshin/Desktop/wip/reviewstats/reviewspider/reviewspider
and run scrapy crawl yelp """

class QuotesSpider(scrapy.Spider):
    name = "yelp"
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

        param_url_encoded = urllib.parse.urlencode(PARAMS)
  
        URL = 'https://www.yelp.com/search?' + param_url_encoded
        # sending get request and saving the response as response object 
        print(URL)
        urls = [URL
        #'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Downtown%20Brooklyn%2C%20Brooklyn%2C%20NY&l=g%3A-73.9982414246%2C40.6838924509%2C-73.9726638794%2C40.7034156679&start=0&end=450'
]
        """To pass in variables to scrapy
        item = response.meta.get('hero_item')
        meta={'hero_item': item}
        """
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        # you need to remember that you have to get the link to go to the next page...
       
        filename = 'test-%s.json' % page
        print(self.response_directory)
        path_to_save = os.path.join(self.response_directory, filename)

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




