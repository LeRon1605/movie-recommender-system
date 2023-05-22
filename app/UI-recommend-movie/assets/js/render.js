const root = document.getElementById("root");
const root1 = document.getElementById('root1');
const root3 = document.getElementById('root3');
const searchField = document.getElementById('search-field');
let movies = null;
const modalImage = document.getElementById('modal-image');
const modalName = document.getElementById('modal-name');
const modalId = document.getElementById('modal-id');
const modalRate = document.getElementById('modal-rate');
const modalForm = document.getElementById('modal-form');

const render = (data) => {
    let html = "";
    data.forEach((item) => {
        html += `
            <div class="col c-2" onclick="getRelatedMovie('${item.id}')" data-bs-toggle="modal" data-bs-target="#exampleModal">
                <div class="movie">
                <img src="${item.poster}" alt="" class="movie-image" />
                <div class="description">
                    <p class="movie-name">${item.name}</p>
                    <span class="movie-score"><i class="fa-solid fa-star star_icon"></i> ${item.score}</span>
                </div>
                </div>
            </div>
        `;
    });
    return html;
};

const renderNotModal = (data) => {
    let html = "";
    data.forEach((item) => {
        html += `
            <div class="col c-2" onclick="getRelatedMovie('${item.id}')">
                <div class="movie">
                <img src="${item.poster}" alt="" class="movie-image" />
                <div class="description">
                    <p class="movie-name">${item.name}</p>
                    <span class="movie-score"><i class="fa-solid fa-star star_icon"></i> ${item.score}</span>
                </div>
                </div>
            </div>
        `;
    });
    return html;
}

window.addEventListener("load", () => {
    fetch('http://127.0.0.1:5000/movies')
        .then(res => res.json())
        .then(data => {
            movies = data;
            data = data.slice(0, 12);
            root1.innerHTML = render(data);
            searchField.addEventListener('input', e => {
                if (e.target.value == '') {
                    root1.innerHTML = render(movies.slice(0, 12));
                } else {  
                    const filtered = movies.filter(x => x.name.includes(e.target.value)).slice(0, 12);
                    root1.innerHTML = render(filtered);
                }
            });
        })
        ;

    fetch("http://127.0.0.1:5000/matrix-factorization", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id: localStorage.getItem("user_id") }),
    })
        .then((res) => res.json())
        .then((data) => {
            root.innerHTML = render(data.reverse());
        })
        .catch((error) => console.log(error));
});

const getRelatedMovie = (item) => {
    item = movies.filter(x => x.id == item)[0];
    modalImage.src = item.poster;
    modalName.innerText = item.name;
    
    modalId.value = item.id;
    fetch("http://127.0.0.1:5000/content-based", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ movie_id: item.id }),
    })
    .then(res => res.json())
    .then(res => {
        root3.innerHTML = renderNotModal(res.reverse());
    });
}

const logout = document.getElementById("logout");

logout.addEventListener("click", () => {
    window.location = "http://127.0.0.1:5500/app/UI-recommend-movie/login.html";
});

modalForm.addEventListener('submit', e => {
    e.preventDefault();

    fetch("http://127.0.0.1:5000/rate", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            movie_id: modalId.value,
            rate: modalRate.value,
            user_id: localStorage.getItem('user_id')
        }),
    })
})