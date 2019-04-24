/* globals fetch */
const $ = require('jquery')
window.$ = window.jQuery = $
const Cookies = require('js-cookie')
const merge = require('deepmerge')

function showDiv (div) {
  $(div).show('slow')
}
function hideDiv (div) {
  $(div).hide('fast')
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
  hideDiv('.step-two')
  hideDiv('.step-three')
  showDiv('.step-one')

  $('.step-one-next-button').click(function () {
    hideDiv('.step-one')
    showDiv('.step-two')
  })
  $('.step-two-next-button').click(function () {
    hideDiv('.step-two')
    showDiv('.step-three')
  })
})
