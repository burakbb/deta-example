window.onload = start;

function start() {
    let submitButton = document.getElementById("submit");
    submitButton.addEventListener("click", submitForm);
}

function submitForm() {
    let firstname = document.getElementById("firstname");
    let lastname = document.getElementById("lastname");
    let email = document.getElementById("email");

    let data = {
        firstname: firstname.value,
        lastname: lastname.value,
        email: email.value,
    };

    fetch("/submit", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(res => {
        if (res.ok) {
            let successDiv = document.createElement("div");
            successDiv.className = "subtitle";
            successDiv.innerHTML = "Form submitted successfully";
            let formDiv = document.getElementsByClassName("form")[0];
            formDiv.appendChild(successDiv)
            setTimeout(function () {
                successDiv.remove();
                firstname.value = "";
                lastname.value = "";
                email.value = "";
            }, 1000)
        }

    });
}
