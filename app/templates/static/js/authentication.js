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
      'redirect_uri': 'http://localhost:8000/login',
      'response_type': 'token',
      'scope': 'https://www.googleapis.com/auth/drive.metadata.readonly',
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
      'X-CSRFToken': getCookie('csrftoken')
    },
      method: 'POST',
      cache: 'default',
      body: JSON.stringify({'access_token': accessToken})
    }
    fetch('/rest-auth/google/', options)
      .then(resp=> resp.json())
      .then(token => {
        window.sessionStorage.setItem(Object.keys(token), token.key)
        if(checkCredentials()){
          window.location.href = '/'
        }
      })
  }
})()