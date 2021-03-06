// main app file
const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const session = require('express-session')
const fs = require('fs')

app.set('views', __dirname + '/views')
app.set('view engine', 'ejs')
app.engine('html', require('ejs').renderFile)

const server = app.listen(8080, function(){
    console.log("Express server has started on port 8080")
})

app.use(express.static('public'))

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended : false }))
app.use('/', require('./router/main'))

app.use(session({
    secret: '@#@$iwanttograduate#@$#$',
    resave: false,
    saveUninitialized: true
}))

