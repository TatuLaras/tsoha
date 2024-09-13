function setParam(param, value) {
    let queryParams = new URLSearchParams(window.location.search);
    queryParams.set(param, value);
    history.pushState(null, null, '?' + queryParams.toString());
    window.location.reload();
}

function changeFontSize(e) {
    const size = e.target.value;
    articleElement.style.setProperty('--font-size', `${size / 100}rem`);
}

function hideThis(e) {
    e.target.classList.add('hide');
}

function routeWithOldParams(route) {
    let queryParams = new URLSearchParams(window.location.search);
    window.location.href = route + '?' + queryParams.toString();
}

const articleElement = document.querySelector('#article-content');
