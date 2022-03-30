function generatePostHTML(title, publishedDate, author, summary, _id) {
    const post = `
        <!-- Post preview-->
        <div class="post-preview" id="${_id}">
            <a href="post.html">
                <h2 class="post-title">${title}</h2>
                <h3 class="post-subtitle">${summary.substring(0,100)}...</h3>
            </a>
            <p class="post-meta">
                ${author ? `Posted by <a href="#!">${author}</a>` : ''}
                
                On ${publishedDate}
            </p>
        </div>
        <!-- Divider-->
        <hr class="my-4" />
    `
    return post
}
function renderArticles(articles){
    const containerPosts = document.querySelector("#container-posts")
    containerPosts.innerHTML = ''
    articles.forEach(({title, author, release_date, extract,id}) => {
        const post = generatePostHTML(title, release_date, author, extract, id)
        containerPosts.innerHTML += post
    })
}
function fetchPosts(link){
    let posts;
    fetch(link)
    .then(response => response.json())
    .then(data => {
        renderArticles(data.results)
    })
}
fetchPosts('api/posts')