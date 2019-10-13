const express = require('express')
const router = express.Router()
const ps = require('python-shell')



router.get('/', (req,res) => {
    res.render('index')
})

router.post('/result', (req,res) => {
    const options = {
        mode: 'text',
        pythonOptions: ['-u'],
        //pythonPath: 'D:\\Python\\Python36\\python.exe',
        scriptPath:'/home/ubuntu/grad/',
        args: [req.body.name, req.body.comment]
    }
    ps.PythonShell.run('html_interactive.py', options, (err, result) => {
        if(err) console.log('err msg : ', err)
        console.log(req.body.comment)
        console.log('results: %j', result)
        // res.send(result)
        res.render('result', {
            name: req.body.name,
            comment: req.body.comment,
            mood: result[3],
            precision: result[4],
        })
    })
})

router.get('/learning', (req,res) => {
    const options = {
        mode: 'text',
        pythonOptions: ['-u'],
        //pythonPath: 'D:\\Python\\Python36\\python.exe',
        scriptPath:'/home/ubuntu/grad/',
        // args: [req.body.name, req.body.comment]
    }
    ps.PythonShell.run('skl_sentiment_analysis3.py', options, (err, result) => {
        if(err) console.log('err msg : ', err)
        console.log('results: %j', result)
        // res.send(result)
        res.render('learning', {
            learning_time : result[3],
            precision : result[4]
        })
    })
})

router.get('/batch', (req,res) => {
    const options = {
        mode: 'text',
        pythonOptions: ['-u'],
        //pythonPath: 'D:\\Python\\Python36\\python.exe',
        scriptPath:'/home/ubuntu/grad/',
        // args: [req.body.name, req.body.comment]
    }
    ps.PythonShell.run('batch_learning.py', options, (err, result) => {
        if(err) console.log('err msg : ', err)
        console.log('results: %j', result)
        // res.send(result)
        res.render('batch', {
            data_size : result[0],
            cur_num : result[1],
            learning_time : result[4],
            precision : result[5]
        })
    })
})

module.exports = router
