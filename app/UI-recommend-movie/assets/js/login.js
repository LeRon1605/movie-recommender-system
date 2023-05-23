const usernameInput = document.getElementById("username");
const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", (e) => {
    e.preventDefault();

    fetch("http://167.172.93.75:7000/login", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: usernameInput.value }),
    })
        .then((res) => res.json())
        .then((data) => {
            localStorage.setItem("user_id", data.user_id);
            window.location = "/movie-recommender-system/app/UI-recommend-movie/index.html";
        })
        .catch((error) => console.log(error));
});
