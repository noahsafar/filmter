// Monitor user activity
let userActive = false;

function setUserActive() {
    userActive = true;
}

document.addEventListener("click", setUserActive);
document.addEventListener("keydown", setUserActive);
