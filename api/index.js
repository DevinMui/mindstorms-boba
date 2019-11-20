var express = require('express')
var app = express()

app.use((req, res, next) => {
    console.log(req.body)
    next()
})
app.use(express.json())

var state = 0

app.get('/', (req, res) => {
    res.json({ hello: 'world' })
})

app.get('/state', (req, res) => {
    res.json({ state: state })
})

app.post('/state', (req, res) => {
    state = req.body.state
    res.json({ state: state })
})

app.listen(process.env.port || 3000, process.env.host, () => {
    console.log('Server running on port 3000')
})

