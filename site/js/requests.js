async function sendRequest(action, params = {}) {
	const url = 'apitest/';

	const requestOptions = {
		method: 'POST',
		body: JSON.stringify({ action, ...params }),
	};

	return (await fetch(url, requestOptions)).json();
}

/*
// get all titles
sendRequest('get_all_titles', {}, data => console.log(data));

// add new post
sendRequest('add_new_post', { title: 'New Post Title', content: 'New Post Content' }, data => console.log(data));

// get post
sendRequest('get_post', { id: 1 }, data => console.log(data));

// change title
sendRequest('change_title', { id: 1, title: 'New Title' }, data => console.log(data));

// change content
sendRequest('change_content', { id: 1, content: 'New Content' }, data => console.log(data));

// delete post
sendRequest('delete_post', { id: 1 }, data => console.log(data));
*/
