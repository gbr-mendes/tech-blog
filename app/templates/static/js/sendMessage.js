const renderErrors = function (resp) {
    resp.json().then(json => {
        const alertSection = document.querySelector('#alert-section')
        const list = document.createElement('ul')
        alertSection.classList.add('alert-danger')
        alertSection.classList.remove('d-none')
        alertSection.classList.remove('alert-success')
        for (const property in json) {
            list.innerHTML += `<li>${property}: ${json[property]}</li>`
        }
        alertSection.appendChild(list)
    })
}

const successResp = function (resp) {
    const alertSection = document.querySelector('#alert-section')
    alertSection.classList.add('alert-success')
    alertSection.classList.remove('d-none')
    alertSection.classList.remove('alert-danger')
    alertSection.innerHTML = 'Message sended successfuly!'
    const form = document.querySelector('#contact-form')
    form.reset()
}

const btn = document.querySelector('#submit-email')
btn.addEventListener('click', e => {
    e.preventDefault()
    e.target.setAttribute('disabled', 'true')
    const data = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value,
    }

    const options = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        method: 'POST',
        mode: 'cors',
        cache: 'default',
        body: JSON.stringify(data)
    }
    const url = '/api/send-email/'
    fetch(url, options)
        .then(resp => {
            resp.status != 201 ? renderErrors(resp) : successResp(resp)
        })
})