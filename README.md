# Сайт на гугл таблицах

## План действий
- Изучить api google sheets, на питоне сделать удобные функции записи, чтения в таблицу
- Перенести это в cloud functions, затем писать обработку запросов с клиента
- Сделать взаимодействие на стороне клиента с cloud functions на js
- Найти бесплатный конструктор сайтов с возможностью экспорта. Можно посмотреть [здесь](https://timeweb.com/ru/community/articles/luchshie-konstruktory-saytov-v-2023-godu)
- Склепать там красивый дизайн. Если предыдущий шаг не удался, скачать внаглую через Ctrl+S 
- Выложить сайт на github.io
- Рассказать преподавателям какая у нашего сайта классная и мощная система облачной базы данных
- Получить 5

## В презентации с выступлением нужно будет сказать, что мы заменили:
- Хостинг сайта на github.io
- Сервер на cloud functions
- Базу данных на google sheets
- Bar guy на blood suck guy

## Каждая тема будет храниться в 3 ячейках (столбцах) нашей таблицы. Json объект будет иметь соответственно 3 поля:
{
	id: 1,
	title: "Grammar",
	content: "<html> with Markdown"
}
## Описание функций класса GoogleShitDB в js и ожидаемый ответ. (В питоне будут похожие)
### get_ids()
```
{
	ids:[1,2,3]
}
```
### get_titles()
```
{
	titles:["Dozens of grammar", "Frankenstein", "Infinity patterns"]
}
```
### get(id)
```
{
	id: 1,
	title: "Grammar",
	content: "<html> with Markdown"
}
```
### add(title, content="")
```
{
	status: true
}
```
### change_title(id, new_title)
```
{
	status: true
}
```
### change_content(id, new_content)
```
{
	status: true
}
```
### delete(id)
```
{
	status: true
}
```
