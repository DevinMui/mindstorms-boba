var express = require('express')

var db = require('./config/db')
var Order = db.Order

var app = express()

// Basic logging middleware
app.use((req, res, next) => {
    console.log(req.body)
    next()
})

app.use(express.json())

app.get('/', (req, res) => {
    res.json({ hello: 'world' })
})

app.get('/queue', (req, res) => {
    // descending
    Order.find({ endedAt: { $exists: false } })
        .sort({ createdAt: -1 })
        .exec((err, orders) => {
            res.json(orders)
        })
})

app.post('/queue', (req, res) => {
    new Order(req.body).save(err => {
        res.json({ success: true })
    })
})

app.patch('/queue/:id', (req, res) => {
    Order.findByIdAndUpdate(
        req.params.id,
        { $set: { endedAt: new Date() } },
        { new: true },
        (err, order) => {
            res.json(order)
        }
    )
})

app.listen(process.env.port || 3000, process.env.host, () => {
    console.log('Server running on port 3000')
})

