var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#actual-app',
    data: {
        name: null,
        phone: null,
        bkashNumber: null,
        paymentOption: "bkash",
        state: null,
        city: null,
        zipCode: null,
        street: null,
        isDisabled: true,
        errors: []
    },
    methods: {
        submitShippingAddress(e) {
            e.preventDefault()
            this.errors = []
            if(!this.name) {
                this.errors.push("Name Is required")
            }
            if(!this.phone) {
                this.errors.push("Phone Number Is required")
            }
            if(!this.state) {
                this.errors.push("State Is required")
            }
            if(!this.city) {
                this.errors.push("City Is required")
            }
            if(!this.zipCode) {
                this.errors.push("Zip Code Is required")
            }
            if(!this.street) {
                this.errors.push("Street Is required")
            }
            if(this.paymentOption == "bkash" && !this.bkashNumber) {
                this.errors.push("BKash Number Is required")
            }
        }
    }
})