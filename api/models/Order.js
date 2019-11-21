module.exports = mongoose => {
    // create an order queue
    const schema = mongoose.Schema(
        {
            name: { type: String, required: true, default: 'Anon' },
            options: {
                tea: { type: String, required: true, default: 'Black Tea' },
                sugar: { type: Number, required: true, default: 100 },
                ice: { type: Number, required: true, default: 100 }
            },
            endedAt: {
                type: Date
            }
        },
        { timestamps: true }
    )

    return mongoose.model('Order', schema)
}
