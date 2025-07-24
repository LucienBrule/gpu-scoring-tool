var items = []
var container = document.querySelectorAll("article.str-item-card")
container.forEach((item) => {
    items.push({
        "title": item.querySelector("h3.str-card-title").innerText,
        "link": item.querySelector("a").href,
        "price": item.querySelector("div.str-item-card__signals").innerText,
        "image": item.querySelector("picture.str-image > source").srcset
    })
})
items