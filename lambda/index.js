const XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest
var http = require('http');

exports.learning = function(event, context, callback) {
  console.log('start request to ' + 'http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/learning')
  const request = require('sync-request')

  let res = request('GET', 'http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/learning')
  let gbody = res.getBody('utf8')
  
  console.log('end request to ' + 'http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/learning');
  return callback(null, {
    statusCode: 200,
    body: JSON.stringify(gbody),
  });
}


exports.comment = function(event, context, callback) {
  // const request = require('request')
  const request = require('sync-request')

  let res = request('POST', 'http://ec2-18-191-88-64.us-east-2.compute.amazonaws.com:8080/result', {
    json: {"name" : "hyungjun", "comment" : "I love this movie!"},
  })
  let gbody = res.getBody('utf8')
  
  return callback(null, {
    statusCode: 200,
    body: JSON.stringify(gbody)
  });
}


