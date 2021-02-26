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
const is_authenticated = JSON.parse(document.getElementById('is_authenticated').textContent);
let form = document.getElementById("add_cart");
let idNode = document.getElementById("productId");
let urlNode = document.getElementById("returnUrl");
let quantityNode = document.getElementById("quantity");
function add_cart(id, quantity) {
    idNode.value = parseInt(id)
    urlNode.value = window.location.pathname
    quantityNode.value = parseInt(quantity);
    form.submit()
}