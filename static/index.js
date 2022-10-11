window.onload = start;

function start() {
    let submitButton = document.getElementById("submit");
    submitButton.addEventListener("click", submitForm);
}

function submitForm() {
    let firstname = document.getElementById("firstname");
    let lastname = document.getElementById("lastname");
    let email = document.getElementById("email");
    let captcha_text = document.getElementById("captcha");
    let captcha_id = captcha_text.getAttribute("itemid")

    let data = {
        firstname: firstname.value,
        lastname: lastname.value,
        email: email.value,
        captcha_id: captcha_id,
        captcha_text: captcha_text.value
    };

    fetch("/submit", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(res => {
        if (res.ok) {
            res.json()
                .then(data => {

                    let resultDiv = document.createElement("div");
                    resultDiv.className = "subtitle";
                    resultDiv.style.textAlign = "center"

                    if (data == "OK") {
                        resultDiv.innerHTML = "Form submitted successfully";
                        let formDiv = document.getElementsByClassName("form")[0];
                        resultDiv.style.color = "green";

                        formDiv.appendChild(resultDiv)
                        setTimeout(function () {
                            resultDiv.remove();
                            firstname.value = "";
                            lastname.value = "";
                            email.value = "";
                            captcha_text.value = ""
                            location.reload();
                        }, 1000)
                    }
                    else {
                        resultDiv.innerHTML = "Wrong captcha";
                        resultDiv.style.color = "red";
                        let formDiv = document.getElementsByClassName("form")[0];
                        formDiv.appendChild(resultDiv)
                        setTimeout(function () {
                            captcha_text.value = ""
                            resultDiv.remove();
                        }, 2000)
                    }
                })



        }

    });
}
