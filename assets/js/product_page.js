var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        min_price: 0,
        max_price: null,
        pages: [],
        currentPage: 1,
        products: [],
        category: cat,
        gender: gen,
        rating: 0,
        allProductCount: 0
    },
    mounted() {
        this.fetchData()
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
            if (this.category) {
                fetch(`/api/products?category=${this.category}&page=${page}&max=${this.max_price || 9999999999.99}&min=${this.min_price || 0}&rating=${this.rating || 0}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"]
                    });
            } else if (this.gender) {
                fetch(`/api/products?gender=${this.gender}&page=${page}&max=${this.max_price || 9999999999.99}&min=${this.min_price || 0}&rating=${this.rating || 0}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"]
                    });
            } else if (this.gender && this.catagory) {
                fetch(`/api/products?gender=${this.gender}&category=${this.category}&page=${page}&max=${this.max_price || 9999999999.99}&min=${this.min_price  || 0}&rating=${this.rating || 0}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"]
                    });
            } else {
                fetch(`/api/products?page=${page}&max=${this.max_price || 9999999999.99}&min=${this.min_price || 0}&rating=${this.rating || 0}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"];
                    });
            }
        },
        fetchData() {
            this.pages = []
            this.products = []
            this.currentPage = 1
            if (this.category) {
                fetch(`/api/products?category=${this.category}&max=${this.max_price || 9999999999.99}&min=${this.min_price || 0}&rating=${this.rating || 0}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"]
                        for (let i = 1; i <= data["paging_info"]["page_count"]; i++) {
                            this.pages.push(i);
                        }
                        this.allProductCount = data["paging_info"].product_count
                    });
            } else if (this.gender) {
                fetch(`/api/products?gender=${this.gender}&max=${this.max_price || 9999999999.99}&min=${this.min_price || 0}&rating=${this.rating || 0}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"]
                        for (let i = 1; i <= data["paging_info"]["page_count"]; i++) {
                            this.pages.push(i);
                        }
                        this.allProductCount = data["paging_info"].product_count
                    });
            } else if (this.gender && this.catagory) {
                fetch(`/api/products?gender=${this.gender}&category=${this.category}&max=${this.max_price || 9999999999.99}&min=${this.min_price || 0}&rating=${this.rating || 0}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"]
                        for (let i = 1; i <= data["paging_info"]["page_count"]; i++) {
                            this.pages.push(i);
                        }
                        this.allProductCount = data["paging_info"].product_count
                    });
            } else {
                fetch(`/api/products?max=${this.max_price || 9999999999.99}&min=${this.min_price || 0}&rating=${this.rating || 0}`)
                    .then(res => res.json())
                    .then(data => {
                        this.products = data["products"]
                        for (let i = 1; i <= data["paging_info"]["page_count"]; i++) {
                            this.pages.push(i);
                        }
                        this.allProductCount = data["paging_info"].product_count
                    });
            }
        },
        changeStar() {
            if(this.rating > 5 || this.rating < 0) {
                this.rating = 0
            }
        }
    }
})