// function that check if a user is authenticated to render the comment form
(function toggleFormCommentsVisibility(){
    if(checkCredentials()){
        const commentForm = document.querySelector('.comment-form')
        commentForm.classList.remove('d-none')
    }else{
        const messageArea = document.querySelector('.message-area')
        messageArea.innerHTML = '<h4>You need login to make a new comment<h4>'
    }
})()

// function that creates a comment element on dom
function createCommentElementDOM(commentData) {
    const commentElement = 
    `
        <li class="media">
            <div class="media-body">
                <strong class="text-success">${commentData.author}</strong>
                <p>
                ${commentData.comment}
                </p>
            </div>
        </li>
        <hr>
    `
    return commentElement
}

// function to append each comment
function appendComment(comment) {
    const commentArea = document.querySelector('.media-list')
    commentArea.innerHTML += createCommentElementDOM(comment)
}

// function to render the comments
function renderComments(comments){
    const commentArea = document.querySelector('.panel-heading')
    if(comments.count > 0){
        commentArea.innerHTML += `<h4>${comments.count} comment(s)</h4>`
        comments.results.forEach(comment => {
            appendComment(comment)
        });
    }else{
        commentArea.innerHTML += '<h4>No comments yet</h4>'
    }
}

// function to fetch comments
function fetchComments(postId, endpoint){
    fetch(`${endpoint}?post_id=${postId}`)
        .then(resp => resp.json())
        .then(comments => renderComments(comments))
}

// Post and endpoint definition
const post_id = window.location.href.split('/').at(-1)
const endpoint = '/api/comments'

// Fetching comments on load
fetchComments(post_id, endpoint)

function commentSuccess(resp) {
    const alertArea = document.querySelector('#alert-area')
    alertArea.classList.remove('d-none')
    alertArea.classList.add('alert-success')
    alertArea.innerHTML = 'Comment added successfuly'
    resp.json().then(json => {
        appendComment(json)
    })
}
function commentError() {
    const alertArea = document.querySelector('#alert-area')
    alertArea.classList.remove('d-none')
    alertArea.classList.add('alert-danger')
    alertArea.innerHTML = 'An error has occurred'
}

// function to post a comment to comments endpoint
function addComment(post_id, endpoint, comment) {
    token = window.sessionStorage.getItem('key') || window.localStorage.getItem('key')
    options = {
        method: 'POST',
        cache: 'default',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
        },
        body: JSON.stringify(comment)
    }
    fetch(`${endpoint}?post_id=${post_id}`, options)
        .then(resp => {
            switch(resp.status) {
                case 201:
                    commentSuccess(resp)
                    break
                default:
                    commentError()
            }
        })
}

// function to make a new comment
function comment() {
    const comment_value = document.querySelector('#comment-input').value
    addComment(post_id, endpoint, {comment: comment_value})
}

// add comment function to click of the button
commentBtn = document.querySelector('#comment-btn')
commentBtn.addEventListener('click', e=>{
    e.preventDefault()
    comment()
})
