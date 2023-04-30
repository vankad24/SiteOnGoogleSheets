"use strict"

// Элементы с изменяемым содержимым/атрибутами
const app = {
	main: document.querySelector("main"),
	front: document.querySelector(".front"),
	editor: document.querySelector(".editor"),
	article: document.querySelector(".article"),
	loading_screen: document.querySelector(".loading_screen")
}

// Отобразить главную страницу
async function display_front_page() {
	display_loading_screen()

	const { titles } = await sendRequest("get_all_titles")

	app.front.replaceChildren()

	for (let obj of titles) {
		const id = obj.id
		const html = parse(obj.head ?? `<h1>${obj.title}</h1>`)
		const card = build_card(id, html)

		app.front.append(card)
	}

	app.front.append(build_new_post_card())

	app.main.classList.remove("two-panel")
	app.front.classList.remove("hide")
	app.editor.classList.add("hide")
	app.article.classList.add("hide")
	app.loading_screen.classList.add("hide")
}

// Отобразить публикацию
async function display_article(id) {
	display_loading_screen()

	const { post } = await sendRequest("get_post", {id})
	const controls = build_post_control_panel(post)
	const contents = document.createElement("div")

	contents.innerHTML = parse(post.content)

	app.article.replaceChildren(controls, contents)

	app.main.classList.remove("two-panel")
	app.front.classList.add("hide")
	app.editor.classList.add("hide")
	app.article.classList.remove("hide")
	app.loading_screen.classList.add("hide")
}

// Отобразить редактор
async function display_editor(id) {
	display_loading_screen()

	const { post } = await sendRequest("get_post", {id})
	const controls = build_editor_control_panel(post)
	const textarea = document.createElement("textarea")
	const preview = build_preview_hint_panel()
	const parsed = document.createElement("div")

	textarea.value = post.content
	parsed.innerHTML = parse(post.content)

	textarea.oninput = function(event) {
		parsed.innerHTML = parse(textarea.value)
	}

	app.editor.replaceChildren(controls, textarea)
	app.article.replaceChildren(preview, parsed)

	app.main.classList.add("two-panel")
	app.front.classList.add("hide")
	app.editor.classList.remove("hide")
	app.article.classList.remove("hide")
	app.loading_screen.classList.add("hide")
}

async function display_loading_screen() {
	app.main.classList.remove("two-panel")
	app.front.classList.add("hide")
	app.editor.classList.add("hide")
	app.article.classList.add("hide")
	app.loading_screen.classList.remove("hide")
}

// ============================================================================
// Функции для генерации элементов
// ============================================================================

// Карточка для главной страницы
function build_card(article_id, html_content) {
	const card = document.createElement("div")

	card.innerHTML = `<div>${html_content}</div><div class="fade"></div><div class="arrow"><img src="icons/arrow_open.svg"></div>`
	card.onclick = function(event) {
		display_article(article_id)
	}

	return card
}

// Карточка для создания нового поста
function build_new_post_card() {
	const card = document.createElement("div")

	card.innerHTML = `<div><img src="icons/add.svg"><div>Добавить</div></div>`
	card.onclick = async function(event) {
		const { id } = await sendRequest('add_new_post', {title: "New post"})
		display_editor(id)
	}

	card.classList.add("add-card")

	return card
}

// Панель с кнопками публикации/скрытия + редактирования + удаления
function build_post_control_panel(post) {
	const strip = document.createElement("div")
	const info = document.createElement("div")

	const unhide = document.createElement("button")
	const hide = document.createElement("button")
	const edit = document.createElement("button")
	const del = document.createElement("button")

	unhide.onlick = function() {
		unhide_article(post.id)
		display_article(post.id) // Спровоцировать обновление панели управления
	}

	hide.onlick = function() {
		hide_article(post.id)
		display_article(post.id)
	}

	edit.onclick = function() {
		display_editor(post.id)
	}

	del.onclick = async function() {
		const id = post.id

		if (confirm("Точно удалить?")) {
			const response = await sendRequest('delete_post', { id } )
			display_front_page()
		}
	}

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

// Панель с кнопками отмены + сохранения
function build_editor_control_panel(post) {
	const strip = document.createElement("div")
	const info = document.createElement("div")

	const abort = document.createElement("button")
	const save = document.createElement("button")

	abort.onclick = function() {
		display_article(post.id)
	}

	save.onclick = async function() {
		const content = app.editor.children[1].value
		const id = post.id

		const response = await sendRequest('change_content', { id, content } )

		display_article(post.id)
	}

	info.innerHTML = "Режим редактирования"
	abort.innerHTML = `<img src="icons/close.svg"><span>Отмена</span>`
	save.innerHTML = `<img src="icons/done.svg"><span>Сохранить</span>`

	strip.classList.add("controls")
	strip.append(info)
	strip.append(abort)
	strip.append(save)

	return strip
}

// Панель с надписью "Предпросмотр"
function build_preview_hint_panel() {
	const strip = document.createElement("div")
	const info = document.createElement("div")

	info.innerHTML = "Предпросмотр"

	strip.classList.add("controls")
	strip.append(info)

	return strip
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
