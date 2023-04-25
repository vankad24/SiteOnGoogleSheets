
function build_card(article_id, html_content) {
	const card = document.createElement("div")

	card.innerHTML = `<div>${html_content}</div><div class="fade"></div><div class="arrow"><img src="icons/arrow_open.svg"></div>`
	card.onclick = function(event) {
		open_article(article_id)
	}

	return card
}

async function display_front_page() {
	const article = document.querySelector("article")
	const cards = document.createElement("div")

	cards.classList.add("cards")
	article.replaceChildren()
	article.append(cards)

	const front_page_objs = await fetch_titles()

	for (let obj of front_page_objs) {
		const card = build_card(obj.id, obj.head)

		cards.append(card)
	}
}

async function fetch_titles() {
	return [
		{
			id: 1,
			head: "<h1>Articles</h1><p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Facilis, impedit quis. Eaque placeat, velit quidem exercitationem vitae illum? Rerum recusandae eligendi quos minima, sed veniam! Nihil earum nemo magni impedit?</p>"
		}
	]
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
