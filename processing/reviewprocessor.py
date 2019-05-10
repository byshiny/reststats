from pprint import pprint
import json
import os
import pandas
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
  
  def process_json_reviewfile(self, filename):
    with open(filename) as f:
        data = json.load(f)
        
    pprint(data)
    with open("test_pretty", "wt") as out:
      pprint(data, stream=out)
  def import_datafile_to_pandas(self, filename):
    data = json.loads(filename)

# print("hello")
reviewprocessor = ReviewProcessor()
filename = "test-www.yelp.com.json"
complete_path = os.path.join(reviewprocessor.response_directory, filename)
reviewprocessor.process_json_reviewfile(complete_path)

  