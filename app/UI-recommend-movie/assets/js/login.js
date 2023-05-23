const usernameInput = document.getElementById("username");
const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", (e) => {
    e.preventDefault();

    fetch("http://127.0.0.1:5000/login", {
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
            window.location = "/app/UI-recommend-movie/index.html";
        })
        .catch((error) => console.log(error));
});
