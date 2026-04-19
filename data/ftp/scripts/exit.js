const button = document.getElementById("exit")

button.addEventListener("click", exit_);

function exit_()
{
    document.cookie = "login=";
    document.cookie = "password=";
    window.location.reload();
}