function openArticle(article_id) {
    var queryParams = new URLSearchParams(window.location.search);
    queryParams.set('article', article_id);
    history.replaceState(null, null, '?' + queryParams.toString());
    window.location.reload();
}

function changeFontSize(e) {
    const size = e.target.value;
    articleElement.style.setProperty('--font-size', `${size / 100}rem`);
}

const articleElement = document.querySelector('#article-content');
