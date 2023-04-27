"use strict"

function build_card(article_id, html_content) {
	const card = document.createElement("div")

	card.innerHTML = `<div>${html_content}</div><div class="fade"></div><div class="arrow"><img src="icons/arrow_open.svg"></div>`
	card.onclick = function(event) {
		display_article(article_id)
	}

	return card
}

function build_controls_strip() {
	const strip = document.createElement("div")
	const info = document.createElement("div")

	const unhide = document.createElement("button")
	const hide = document.createElement("button")
	const edit = document.createElement("button")
	const del = document.createElement("button")

	info.innerHTML = "Управление"
	unhide.innerHTML = `<img src="icons/visibility.svg"><span>Опубликовать</span>`
	hide.innerHTML = `<img src="icons/visibility_off.svg"><span>Спрятать</span>`
	edit.innerHTML = `<img src="icons/edit.svg"><span>Редактировать</span>`
	del.innerHTML = `<img src="icons/delete.svg"><span>Удалить</span>`

	strip.classList.add("controls")
	strip.append(info)
	strip.append(hide)
	strip.append(edit)
	strip.append(del)

	return strip
}

async function display_front_page() {
	const article = document.querySelector("article")
	const cards = document.createElement("div")

	cards.classList.add("cards")
	article.replaceChildren()
	article.append(cards)

	const front_page_objs = await sendRequest("get_all_titles")

	for (let obj of front_page_objs) {
		const id = obj.id
		const html = parse(obj.head)
		const card = build_card(id, html)

		cards.append(card)
	}
}

async function display_article(id) {
	const article = document.querySelector("article")
	const post = await sendRequest("get_post", {id})

	const controls = build_controls_strip()
	const contents = document.createElement("div")

	contents.innerHTML = parse(post.content)

	article.replaceChildren()
	article.append(controls)
	article.append(contents)
}

display_front_page()

// fetch("https://functions.yandexcloud.net/d4ekq68eemul40pdvpc9", {
//   "headers": {
//     "accept": "*/*",
//     "accept-language": "ru,en;q=0.9",
//     "content-type": "text/plain;charset=UTF-8",
//     "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"YaBrowser\";v=\"23\"",
//     "sec-ch-ua-mobile": "?0",
//     "sec-ch-ua-platform": "\"Windows\"",
//     "sec-fetch-dest": "empty",
//     "sec-fetch-mode": "cors",
//     "sec-fetch-site": "cross-site"
//   },
//   "referrerPolicy": "strict-origin-when-cross-origin",
//   "body": "{\"status\":\"ok\",\"cards\":[{\"count\":1,\"color\":2,\"shape\":3,\"fill\":2},{\"count\":2,\"color\":2,\"shape\":3,\"fill\":3},{\"count\":2,\"color\":3,\"shape\":2,\"fill\":3},{\"count\":1,\"color\":2,\"shape\":2,\"fill\":3},{\"count\":3,\"color\":2,\"shape\":2,\"fill\":2},{\"count\":3,\"color\":1,\"shape\":3,\"fill\":3},{\"count\":1,\"color\":1,\"shape\":2,\"fill\":3},{\"count\":2,\"color\":3,\"shape\":2,\"fill\":2},{\"count\":2,\"color\":1,\"shape\":1,\"fill\":1},{\"count\":2,\"color\":2,\"shape\":1,\"fill\":3},{\"count\":3,\"color\":3,\"shape\":1,\"fill\":1},{\"count\":2,\"color\":1,\"shape\":1,\"fill\":3}]}",
//   "method": "POST",
//   "mode": "cors",
//   "credentials": "omit"
// }).then(response => response.text())
//   .then(result => console.log(result))
//   .catch(error => console.log('error', error));
