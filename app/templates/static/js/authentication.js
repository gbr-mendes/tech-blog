function checkCredentials() {
    if(window.sessionStorage.getItem('key') || window.localStorage.getItem('key')) {
        return true
    }
    return false
}

(function toggleLoginLogoutBtnVisibility() {
    const btns = document.querySelectorAll('[data-toggle-visibility]').forEach(btn => {
        if(btn.dataset.toggleVisibility === 'login' || btn.dataset.toggleVisibility === 'register'){
            checkCredentials() ? btn.classList.add('d-none') : btn.classList.remove('d-none')
        }
        if(btn.dataset.toggleVisibility === 'logout'){
            checkCredentials() ? btn.classList.remove('d-none') : btn.classList.add('d-none')
        }

    })
})()

// Function to deal with errors on post credentials
function postFail(json) {
  let alertArea = document.querySelector('#alert-area')
  alertArea.classList.remove('d-none')
  const ul = document.createElement('ul')
  alertArea.appendChild(ul)
  alertArea = document.querySelector('#alert-area ul')
  alertArea.innerHTML = ''
  for(let value in json){
    if(value === "non_field_errors"){
      json[value].forEach(error =>  alertArea.innerHTML += `<li>${error}</li>`)
    }else{
      alertArea.innerHTML += `<li>${value}: ${json[value]}</li>`
    }
  }
  const btnSubmit = document.querySelector('#btn-submit')
  btnSubmit.disabled = false

}

// Function to post data to login and register endpoints
function postDataAuthentication(functionSuccess, functionError, url, credentials){
  const options = {
    method: "POST",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(credentials)
  }
  const checkBox = credentials.checkbox
  fetch(url, options)
      .then(resp=> {
        if(resp.status >= 200 && resp.status < 300){
          resp.json().then(json=> functionSuccess(json, checkBox))
        }else{
          resp.json().then(json=> functionError(json))
        }
      })

}

// Function to deal with the key after login request
function loginUser(json, checkBox) {
  checkBox ? window.localStorage.setItem(Object.keys(json)[0], json.key) : window.sessionStorage.setItem(Object.keys(json)[0], json.key)
  window.location.href = '/'
}

// Add login function to click on button in login page
if(window.location.href.includes('/login')){
    if(checkCredentials()){
      window.location.href = '/'
    }
    const form = document.querySelector('#login-form')
    const btnLogin = document.querySelector('#btn-submit')
    btnLogin.addEventListener('click', e=> {
      e.preventDefault()
      e.target.disabled = true
      const credentials = {email: form.email.value,password: form.password.value, checkbox: form.checkbox.checked}
      postDataAuthentication(loginUser, postFail, '/rest-auth/login/', credentials)
    })
}

// Add register function to click on button in register page
if(window.location.href.includes('/register')){
  if(checkCredentials()){
    window.location.href = '/'
  }
  const form = document.querySelector('#register-form')
  const btnLogin = document.querySelector('#btn-submit')
  btnLogin.addEventListener('click', e=> {
    e.preventDefault()
    e.target.disabled = true
    const credentials = {name:form.name.value, email: form.email.value, password1: form.password2.value, password2: form.password2.value}
    postDataAuthentication(loginUser, postFail, 'rest-auth/registration/register/', credentials)
  })
}

// Function to logout an authenticated user
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

// Add logout function to logout button
const btnLogout = document.querySelector('[data-toggle-visibility="logout"]')
btnLogout.addEventListener('click',e=> {
    e.preventDefault()
    logoutUser()
})

//Google Social Login
 
/*
* Create form to request access token from Google's OAuth 2.0 server.
*/
function oauthSignIn() {
  // Google's OAuth 2.0 endpoint for requesting an access token
  var oauth2Endpoint = 'https://accounts.google.com/o/oauth2/v2/auth';

  // Create <form> element to submit parameters to OAuth 2.0 endpoint.
  var form = document.createElement('form');
  form.setAttribute('method', 'GET'); // Send as a GET request.
  form.setAttribute('action', oauth2Endpoint);

  // Parameters to pass to OAuth 2.0 endpoint.
  var params = {
    'client_id': document.getElementsByName('google-signin-client_id')[0].content,
    'redirect_uri': `${window.location.origin}/login`,
    'response_type': 'token',
    'scope': 'https://www.googleapis.com/auth/userinfo.email&https://www.googleapis.com/auth/userinfo.profile&https://www.googleapis.com/openid',
    'include_granted_scopes': 'true',
    'state': 'pass-through value'
  };

  // Add form parameters as hidden input values.
  for (var p in params) {
    var input = document.createElement('input');
    input.setAttribute('type', 'hidden');
    input.setAttribute('name', p);
    input.setAttribute('value', params[p]);
    form.appendChild(input);
  }

  // Add form to page and submit it to open the OAuth 2.0 endpoint.
  document.body.appendChild(form);
  form.submit()
}
(function checkSocialAuthentication(){
  const queryString = window.location.hash
  const urlParams = new URLSearchParams(queryString.split('#')[1])
  const accessToken = urlParams.get('access_token')
  if(accessToken) {
    const options = {
      headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
      'Authorization': `Bearer ${accessToken}`
    },
      method: 'POST',
      cache: 'default',
      body: JSON.stringify({'access_token': accessToken})
    }
    fetch('/rest-auth/google/', options)
      .then(resp=> resp.json())
      .then(json => {
        window.sessionStorage.setItem(Object.keys(json), json.key)
        if(checkCredentials()){
          window.location.href = '/'
          return
        }
        else if (json.non_field_errors){
          const msg = json.non_field_errors[0]
          const messageArea = document.querySelector('#alert-area')
          messageArea.classList.remove('d-none')
          messageArea.innerText = msg
        }
      })
  }
})()
