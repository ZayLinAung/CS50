let counter = 1;
const quantity = 10;
let total = 0;
let start = 0;
let end = 0;
let previousText = '';
let newLikes = 0;

document.addEventListener('DOMContentLoaded', function(){
    loadNext();
    document.querySelector('#next').addEventListener('click', () => loadNext());
    document.querySelector('#previous').addEventListener('click', () => loadPrev());
});


function loadNext() {


    document.querySelector('#posts').innerHTML='';

    // Set start and end post numbers, and update counter
    start = counter;
    end = start + quantity - 1;
    counter = end + 1;

    // Get new posts and add posts
    fetch(`/prototype?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        data.posts.forEach(add_post);
        if (counter == 11){
            document.querySelector('#previous').style.display = 'none';
        }
        else if (counter > 11){
            document.querySelector('#previous').style.display = 'block';
        }

        if (counter >= data.total){
            document.querySelector('#next').style.display = 'none';
        }
        else if (counter < data.total){
            document.querySelector('#next').style.display = 'block';
        }
    })
};

function loadPrev() {
    document.querySelector('#posts').innerHTML='';

    // Set start and end post numbers, and update counter
    start = counter - 20;
    end = start + quantity - 1;
    counter = counter - 10;

    // Get new posts and add posts
    fetch(`/prototype?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {

        data.posts.forEach(add_post);
        if (counter == 11){
            document.querySelector('#previous').style.display = 'none';
        }
        else if (counter > 11){
            document.querySelector('#previous').style.display = 'block';
        }

        if (counter >= data.total){
            document.querySelector('#next').style.display = 'none';
        }
        else if (counter < data.total){
            document.querySelector('#next').style.display = 'block';
        }
    })
};

function editPost(id, content){
    document.querySelector('#edit' + id).style.display = 'none';
    document.querySelector('#submit' + id).style.display = 'block';
    const editSec = document.getElementById(id);
    editSec.innerHTML = '';
    const textArea = document.createElement('textArea');
    textArea.style.width = "700px";
    textArea.innerHTML = previousText.length == 0 ? content : previousText;
    editSec.append(textArea);

    document.querySelector('#submit' + id).addEventListener('click', function(){
        fetch(`/prototype?start=${start}&end=${end}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: textArea.value,
                id: id
            })
          })
          document.querySelector('#edit' + id).style.display = 'block';
          document.querySelector('#submit' + id).style.display = 'none';
          editSec.innerHTML = textArea.value;
          previousText = textArea.value;
    })
}


// Add a new post with given contents to DOM
function add_post(contents) {

    // Create new post
    const post = document.createElement('div');
    post.id = 'post' + contents.id;
    post.className = 'section';

    if (document.querySelector('#login').value){
        post.innerHTML = `<h6 style="color: blue; width: 90px;"><a class="nav-link" href="profilePage/${contents.username}">${contents.username}</a></h6>`;
    }
    else{
        post.innerHTML = `<h6 style="color: blue">${contents.username}</h6>`;
    }
    post.innerHTML += `<br>${contents.time}`;

    const section = document.createElement('div');
    section.style.margin = "10px";
    section.innerHTML = `
        <br><br>
        <div id = ${contents.id}>${contents.content}</div> <br><br>
        <button style = 'width: 100px;' id = 'likeButton${contents.id}' data-id = 0 onclick = 'update_like(${contents.likes}, ${contents.id})'>&#128151 Like ${contents.likes}</button>
    `;

    if (document.querySelector('#logInUser').value == contents.username){
        section.innerHTML += `
        <button id = 'edit${contents.id}' onclick='editPost(${contents.id}, "${contents.content}")'>Edit</button>
        <button style = 'display: none' id = 'submit${contents.id}'>Submit</button>
        `;
    }

    post.append(section);
    document.querySelector('#posts').append(post);

};

function update_like(num_likes, id, alrLiked){
    let gave_like = '';

    button = document.querySelector('#likeButton' + id);


    if (button.getAttribute('data-id')  == 0){
        num_likes++;
        newLikes = num_likes;
        gave_like = 'true';
        button.setAttribute('data-id', 1);
        data_id = 1;
        button.style.background = '#3085C3';
        button.style.color = 'white';
        button.innerHTML = '&#128151 Likes ' + num_likes;
    }
    else{
        newLikes--;
        num_likes = newLikes;
        gave_like = 'false';
        button.setAttribute('data-id', 0);
        data_id = 0;
        button.style.background = 'transparent';
        button.style.color = '#3498db';
        button.innerHTML = '&#128151 Likes ' + num_likes;
    }
    fetch(`/prototype?start=${start}&end=${end}`, {
        method: 'PUT',
        body: JSON.stringify({
            num_likes: num_likes,
            liked: gave_like,
            id: id
        })
    })
}