const mongoose = require('mongoose')

mongoose.Promise = global.Promise

const options = {
    useNewUrlParser: true,
    useFindAndModify: false,
    useUnifiedTopology: true
}

mongoose.connect(
    process.env.MONGO_URI || 'mongodb://localhost:27017/mindstorms-development',
    options
)

mongoose.set('useCreateIndex', true)

const Order = require('../models/Order')(mongoose)

module.exports = { Order: Order }
