var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        min_price: 0,
        max_price: null,
        pagingInfo: {},
        products: []
    },
    mounted() {
        fetch("api/products")
        .then(res => res.json())
        .then(data => {
            this.pagingInfo = data["paging_info"],
            this.products = data["products"]
        });
    },
    methods: {
        max_changed() {
            if (this.max_price < 0) {
                this.max_price = 0
            }
        },
        min_changed() {
            if (this.min_price < 0) {
                this.min_price = 0
            }
        }
    }
})