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
        if (category) {
            fetch(`/api/products?category=${category}`)
                .then(res => res.json())
                .then(data => {
                    this.products = data["products"]
                    for (let i = 1; i <= data["paging_info"]["page_count"]; i++) {
                        this.pages.push(i);
                    }
                });
        } else if (gender) {
            fetch(`/api/products?gender=${gender}`)
                .then(res => res.json())
                .then(data => {
                    this.products = data["products"]
                    for (let i = 1; i <= data["paging_info"]["page_count"]; i++) {
                        this.pages.push(i);
                    }
                });
        } else if (gender && catagory) {
            fetch(`/api/products?gender=${gender}&category=${category}`)
                .then(res => res.json())
                .then(data => {
                    this.products = data["products"]
                    for (let i = 1; i <= data["paging_info"]["page_count"]; i++) {
                        this.pages.push(i);
                    }
                });
        } else {
            fetch("/api/products")
                .then(res => res.json())
                .then(data => {
                    this.products = data["products"]
                    for (let i = 1; i <= data["paging_info"]["page_count"]; i++) {
                        this.pages.push(i);
                    }
                });
        }
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
            if (category) {
                fetch(`/api/products?category=${category}&page=${page}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"]
                    });
            } else if (gender) {
                fetch(`/api/products?gender=${gender}&page=${page}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"]
                    });
            } else if (gender && catagory) {
                fetch(`/api/products?gender=${gender}&category=${category}&page=${page}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"]
                    });
            } else {
                fetch(`/api/products?page=${page}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"];
                    });
            }
        }
    }
})