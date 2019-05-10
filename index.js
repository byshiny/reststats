'use strict';

const yelp = require('yelp-fusion');
const fs = require('fs')

// Place holder for Yelp Fusion's API Key. Grab them
// from https://www.yelp.com/developers/v3/manage_app
var propRawByteArr = fs.readFileSync("prop.json");
var propJson = JSON.parse(propRawByteArr);
// console.log(propJson)
const apiKey = propJson["api_key"]
// console.log(apiKey)
const searchRequest = {
  term:'restaurants',
  location: '397 Bridge StBrooklyn, NY 11201'
};

const client = yelp.client(apiKey);
getRestuarantsWithinRadius(searchRequest);
// extractIDListFromFile("resp.recurse.1600.txt")

function extractIDListFromFile(filename){
  var respBodyJSON = fs.readFileSync(filename);
  var allRestJson = JSON.parse(respBodyJSON);
  var busList = allRestJson.jsonBody.businesses
  //charts.js
  //awesome-data-viz
  let itemCount = 0
  for (let bus of busList){
    console.log(bus.id)
    itemCount +=1
  }
  console.log(itemCount)
}



function getRestuarantsWithinRadius(searchReq){
  client.search(searchReq).then(response => {
    const results = response;
    const prettyJson = JSON.stringify(results, null, 4);
    console.log(prettyJson);
  }).catch(e => {
    console.log(e);
  });

}


function getReviewForResturant(resturantName){
  const searchRequest = {
    term:'restuarant',
    location: '397 Bridge StBrooklyn, NY 11201',
    radius: 1600
  };

}


// function getAllReviews()


