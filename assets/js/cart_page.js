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
    el: '#app',
    data: {
        message: 'Hello Vue!',
        items : []
    },
    beforeCreate() {
        fetch("/cart_items")
        .catch(e => console.log(e))
        .then(r => r.json())
        .then(data => this.items = data)
    },
    methods: {
        async addQuantity(e, index) {
            if (this.items[index].quantity < 100) {
                this.items[index].quantity += 1;
                const res = await fetch("/cart_items", {
                    method: 'POST', // *GET, POST, PUT, DELETE, etc.
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        id: this.items[index].id,
                        op: "add",
                        quantity: 1
                    })
                });
            }
        },
        async removeQuantity(e, index) {
            if (this.items[index].quantity > 1) {
                this.items[index].quantity -= 1;
                const res = await fetch("/cart_items", {
                    method: 'POST', // *GET, POST, PUT, DELETE, etc.
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        id: this.items[index].id,
                        op: "add",
                        quantity: -1
                    })
                });
            }
        },
        async remove(e, index) {
            this.$delete(this.items, index);
            const res = await fetch("/cart_items", {
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    id: this.items[index].id,
                    op: "remove"
                })
            });
            const data = await res.json();
        },
        async removeAll(e) {
            this.items = []
            const res = await fetch("/cart_items", {
                method: 'POST', // *GET, POST, PUT, DELETE, etc.
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    op: "remove_all"
                })
            });
        }
    },
})
