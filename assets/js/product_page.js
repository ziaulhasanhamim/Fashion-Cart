var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        min_price: 0,
        max_price: null,
        pages: [],
        currentPage: 1,
        products: []
    },
    mounted() {
        fetch("api/products")
            .then(res => res.json())
            .then(data => {
                this.products = data["products"]
                for (let i = 1; i <= data["paging_info"]["page_count"]; i++) {
                    this.pages.push(i);
                }
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
        },
        changeCurrentPage(page) {
            this.currentPage = page;
            fetch(`api/products?page=${page}`)
                .then(res => res.json())
                .then(data => {
                    this.products = data["products"];
                });
        }
    }
})