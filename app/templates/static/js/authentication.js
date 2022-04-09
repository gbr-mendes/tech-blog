function checkCredentials() {
    if(window.sessionStorage.getItem('key') || window.localStorage.getItem('key')) {
        return true
    }
    return false
}

(function toggleLoginLogoutBtnVisibility() {
    const btns = document.querySelectorAll('[data-toggle-visibility]').forEach(btn => {
        if(btn.dataset.toggleVisibility === 'login'){
            checkCredentials() ? btn.classList.add('d-none') : btn.classList.remove('d-none')
        }
        if(btn.dataset.toggleVisibility === 'logout'){
            checkCredentials() ? btn.classList.remove('d-none') : btn.classList.add('d-none')
        }

    })
})()


const oldURL = document.referrer
if(window.location.href.includes('/login') && checkCredentials()) { /* If user is already authenticated redirect to previous page */
    window.location.href = !oldURL.includes('/login') ? oldURL : '/'
}

function loginUser() {
    const formData = new FormData(document.querySelector('#login-form'))
    const checkBox = formData.get('checkbox')
    const url = '/rest-auth/login/'
    const options = {
      method: "POST",
      body: formData
    }
    fetch(url, options)
      .then(resp=> resp.json())
      .then(json => {
        if(!json.non_field_errors){
          checkBox ? window.localStorage.setItem(Object.keys(json)[0], json.key) : window.sessionStorage.setItem(Object.keys(json)[0], json.key)
          window.location.href = oldURL
        }else {
          const alertArea = document.querySelector('#alert-area')
          alertArea.classList.remove('d-none')
          alertArea.innerHTML = json.non_field_errors
        }
      })
  }
if(window.location.href.includes('/login')){
    const btnLogin = document.querySelector('#btn-login')
    btnLogin.addEventListener('click', e=> {
      e.preventDefault()
      e.target.setAttribute('disabled', 'true')
      loginUser()
    })
}

  function logoutUser() {
      const url = '/rest-auth/logout/'
      const options = {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({
          })
        }
      fetch(url, options)
        .then(resp => resp.json())
        .then(json => {
            if(json.detail === 'Successfully logged out.'){
                window.localStorage.removeItem('key')
                window.sessionStorage.removeItem('key')
                window.location.href = '/login'
            }else{
                console.error('A problem ha ocurred!!')
            }
        })
  }
  const btnLogout = document.querySelector('[data-toggle-visibility="logout"]')
  btnLogout.addEventListener('click',e=> {
      e.preventDefault()
      logoutUser()
  })