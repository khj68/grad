const ps = require('python-shell')
const path = require('path')

const options = {
  mode: 'text',
  pythonOptions: ['-u'],
  pythonPath: 'D:\\Python\\Python36\\python.exe',
  scriptPath:'D:\\grad\\',
  args:['aaa','bbb','ccc']
}

ps.PythonShell.run('a.py', options, (err, result) => {
  if(err) console.log('err msg : ', err)
  console.log('results: %j', result)
})
