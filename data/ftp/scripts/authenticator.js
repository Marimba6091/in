const b = document.getElementById("log-btn");
const b1 = document.getElementById("hide-btn");
const l1 = document.getElementById("log1");
const l2 = document.getElementById("log2");
const img = document.getElementById("hide-img");
const t = document.getElementById("errorMessage");

document.cookie = "$login="

let hide = true;

b.addEventListener("click", e)
b1.addEventListener("click", h)
l1.addEventListener("input", r)
l2.addEventListener("input", r)

async function e()
{
    let email = l1.value;
    let pass = await sha256(l2.value);
    let json = {
        login: email,
        password: pass,
        method: "log_in"
    };
    console.log(pass);
    let response = await fetch("submit",
        {
            method: "POST",
            headers: {'Content-Type': 'application/json;charset=utf-8'},
            body: JSON.stringify(json)
        }
    );
    let res = await response.json()
    
    if (res.succes)
    {
        window.location.href = "/";
        document.cookie = `login=${email};`;
        document.cookie = `password=${pass};`
    }
    else
    {
        t.style.display = "block";
    }
}

function r()
{
    t.style.display = "none";
}

function h()
{
    hide = !hide;
    if (hide)
    {
        l2.type = "password";
        img.src = "icons/close-eye.png";
    }
    else
    {
        l2.type = "text";
        img.src = "icons/open-eye.png";
    }
}

