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
}
