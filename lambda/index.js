const XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest

exports.learning = async (event) => {
  var HttpClient = function() {
      this.get = function(aUrl, aCallback) {
          var anHttpRequest = new XMLHttpRequest();
          anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
          }
          anHttpRequest.open( "GET", aUrl, false );            
          anHttpRequest.send( null );
      }
  }
  var client = new HttpClient();
      client.get('http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/learning', function(response) {
      // do something with response
      return response
  });
};

exports.comment = async (event) => {
  var HttpClient = function() {
      this.get = function(aUrl, aCallback) {
          var anHttpRequest = new XMLHttpRequest();
          anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
          }
          anHttpRequest.open( "GET", aUrl, true );            
          anHttpRequest.send( {"body": {"name" : "hyungjun", "comment" : "I love this movie. I want to see it again."}} );
      }
  }
  var client = new HttpClient();
      client.get('http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/result', function(response) {
      // do something with response
      return response
  });
};

var http = require('http');

exports.handler = function(event, context, callback) {
  console.log('start request to ' + 'http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/learning')
  const request = require('sync-request')

  let res = request('GET', 'http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/learning')
  let gbody = res.getBody('utf8')
  
  // http.get('http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/learning', function(res) {
  //   console.log("Got response: " + res.statusCode);
  //   context.succeed();
  // }).on('error', function(e) {
  //   console.log("Got error: " + e.message);
  //   context.done(null, 'FAILURE');
  // });
  
  console.log('end request to ' + 'http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/learning');
  return callback(null, {
    statusCode: 200,
    body: JSON.stringify(gbody),
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

async function sleeping(){
  await sleep(15000)
}

exports.handler3 = function(event, context, callback) {
  // const request = require('request')
  const request = require('sync-request')

  let res = request('POST', 'http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/result', {
    json: {"name" : "hyungjun", "comment" : "I love this movie!"},
  })
  let gbody = res.getBody('utf8')
  // let gbody = JSON.parse(res.getBody('utf8'))
  // let gbody = null
  // request.post({
  //   headers: {'content-type' : 'application/json'},
  //   json: true,
  //   url: 'http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/result',
  //   body: {"name" : "hyungjun", "comment" : "I love this movie!"}
  // }, (e, res, body) => {
  //   // sleeping()
  //   console.log(body)
  //   gbody = body
  // })
  
  // sleeping()
  
  return callback(null, {
    statusCode: 200,
    // body: JSON.stringify({"message":"it's great"}),
    body: JSON.stringify(gbody)
  });
}


