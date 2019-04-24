/* globals fetch */
const $ = require('jquery')
window.$ = window.jQuery = $
const Cookies = require('js-cookie')
const merge = require('deepmerge')
// sticky navBar: https://codepen.io/renduh/pen/oBBGbK
let navBar = $('.nav-bar')
let headerDiv = $('.company-title').height()

function showDiv (div) {
  div.show()
}
function hideDiv (div) {
  div.hide()
}
// https://sudo.isl.co/fetch-me-that-json-from-django/
function request (url, options) {
  if (!options) {
    options = {}
  }
  const defaultOptions = {
    headers: {
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': Cookies.get('csrftoken')
    },
    credentials: 'include'
  }
  return fetch(url, merge(defaultOptions, options))
}

// fetching fittings api and returning JSON data below
request('/api/fittings')
  .then(response => {
    if (!response.ok) {
      throw Error(response.statusText)
    }
    return response.json()
  })

// change form to slidinig form with buttons on top
// http://www.jquery-steps.com/Examples#embed

$(document).ready(() => {
  console.log('loaded')

  $(window).scroll(function () {
    if ($(this).scrollTop() > headerDiv) {
      navBar.addClass('.sticky-nav')
    } else {
      navBar.removeClass('.sticky-nav')
    }
  })
})
