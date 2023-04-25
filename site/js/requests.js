function sendRequest(action, params, callback) {
  const url = 'http://server-url.com';

  const requestOptions = {
    method: 'POST',
    body: JSON.stringify({ action, ...params }),
  };

  fetch(url, requestOptions)
    .then(response => response.json())
    .then(data => callback(data));
}

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