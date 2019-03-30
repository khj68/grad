module.exports = (app, fs) =>{
    app.get('/', (req,res) => {
        res.render('index', {
            title: "My page",
            length: 5
        })
    })

    app.get('/list', (req,res) => {
        fs.readFile( __dirname + "/../data/" + "user.json",
         'utf8', (err, data) => {
            console.log(data)
            res.end(data)
        })
    })

    app.get('/getUser/:username', (req,res) => {
        fs.readFile( __dirname + "/../data/user.json", 'utf8', 
        (err, data) => {
            const users = JSON.parse(data)
            res.json(users[req.params.username])
        })
    })

    app.post('/result', (req,res) => {
        const { spawn } = require('child_process')
        const pyProg = spawn('python', ['./html_practice.py', 'value1', 'value2'])

        pyProg.stdout.on('data', (data) => {
            console.log(data.toString())
            res.write(data)
            res.end('end')
        })
    })
}
