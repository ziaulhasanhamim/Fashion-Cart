function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken')

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
        // zipCode: null,
        street: null,
        isDisabled: false,
        errors: [],
        subTotal: sub_total,
        shippingCharge: 0,
        placeOrderDisabled: true,
        isPlaceOrderShown: true,
        submitting: false
    },
    methods: {
        submitShippingAddress(e) {
            e.preventDefault()
            this.errors = []
            // this.zipCode = parseInt(this.zipCode)
            // if(isNaN(this.zipCode)) {
            //     this.errors.push("Zip Code Should be An Integer number")
            // }
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
            // if(!this.zipCode) {
            //     this.errors.push("Zip Code Is required")
            // }
            if(!this.street) {
                this.errors.push("Street Is required")
            }
            if(this.paymentOption == "bkash" && !this.bkashNumber) {
                this.errors.push("BKash Number Is required")
            }
            if (this.errors.length == 0) {
                fetch("/api/shipping_charge", {
                    method: 'POST', // *GET, POST, PUT, DELETE, etc.
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        state: this.state,
                        city: this.city,
                    })
                })
                .then(res => res.json())
                .then(data => {
                    this.shippingCharge = data["charge"]
                    this.placeOrderDisabled = false
                    this.isDisabled = true
                });
                document.getElementById("order-summary").scrollIntoView()
                return;
            }
            document.getElementById("div-contain-error").scrollIntoView()
        },
        placeOrder(e) {
            this.isPlaceOrderShown = false
            this.submitting = true
            fetch("/api/place_order", {
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    state: this.state,
                    city: this.city,
                    street: this.street,
                    name: this.name,
                    paymentOption: this.paymentOption,
                    phone: this.phone,
                    bkashNumber: this.bkashNumber
                })
            })
            .then(res => res.json())
            .then(data => {
                 window.location= "/"
            });
        }
    }
})