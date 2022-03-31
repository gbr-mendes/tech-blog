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

function renderPosts(articles){
    const containerPosts = document.querySelector("#container-posts")
    containerPosts.innerHTML = ''
    articles.forEach(({title, author, release_date, extract,id}) => {
        const post = generatePostHTML(title, release_date, author, extract, id)
        containerPosts.innerHTML += post
    })
}

function fetchPosts(url){
    fetch(url)
    .then(response => response.json())
    .then(data => {
        renderPosts(data.results)
        generatePaginationElement(data)
    })
}

function generatePaginationElement(data) {
    const paginationSection = document.querySelector('#pagination-section')
    const {previous, next} = data
    paginationSection.innerHTML = `
        <nav class="d-flex justify-content-center">
            <ul class="pagination">
                ${previous ? `<li class="page-item"><a class="page-link" href="#" onClick="fetchPosts('${previous}')">Previous</a></li>` : ''}
                ${next ? `<li class="page-item"><a class="page-link" href="#" onClick="fetchPosts('${next}')">Next</a></li>` : ''}
            </ul>
        </nav>
    `
}

fetchPosts('api/posts')