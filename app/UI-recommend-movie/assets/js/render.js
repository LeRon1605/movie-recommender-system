const root = document.getElementById("root");

window.addEventListener("load", () => {
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
            const render = (data) => {
                let html = "";
                data.forEach((item) => {
                    html += `
                <div class="col c-2">
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
            root.innerHTML = render(data);
        })
        .catch((error) => console.log(error));
});

const logout = document.getElementById("logout");

logout.addEventListener("click", () => {
    window.location = "http://127.0.0.1:5500/app/UI-recommend-movie/login.html";
});
