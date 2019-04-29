/* globals fetch */
const $ = require('jquery')
window.$ = window.jQuery = $
const Cookies = require('js-cookie')
const merge = require('deepmerge')
// sticky navBar: https://codepen.io/renduh/pen/oBBGbK
let navBar = $('.nav-bar')
const headerDiv = $('#header').height()

function showDiv (div, type) {
  $(div).show(type)
}
function hideDiv (div, type) {
  $(div).hide(type)
}

function startFitting () {
  hideDiv('.step-two')
  hideDiv('.step-three')
  showDiv('.step-one', 'slow')

  $('.step-one-next-button').click(function () {
    hideDiv('.step-one')
    showDiv('.step-two', 'slow')
  })
  $('.step-two-next-button').click(function () {
    hideDiv('.step-two')
    showDiv('.step-three', 'slow')
  })
}

function startSuggestionForm () {
  hideDiv('.sugg-step-one')
  hideDiv('.sugg-step-two')
  hideDiv('.sugg-step-three')
  hideDiv('.sugg-step-four')

  $('.sugg-step-start-next-button').click(function () {
    hideDiv('.sugg-step-start')
    showDiv('.sugg-step-one', 'slow')
  })
  $('.sugg-step-one-next-button').click(function () {
    hideDiv('.sugg-step-one')
    showDiv('.sugg-step-two', 'slow')
  })
  $('.sugg-step-two-next-button').click(function () {
    hideDiv('.sugg-step-two')
    showDiv('.sugg-step-three', 'slow')
  })
  $('.sugg-step-three-next-button').click(function () {
    hideDiv('.sugg-step-three')
    showDiv('.sugg-step-four', 'slow')
  })
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
      navBar.addClass('sticky-nav')
    } else {
      navBar.removeClass('sticky-nav')
    }
  })

  startFitting()
  startSuggestionForm()
})

// swal('You did it! Now you know how to do your own bra fitting and get a bra size and style that supports you!')
// confirmButtonColor: '#DD6B55'
