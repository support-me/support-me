/* globals fetch */
const $ = require('jquery')
const Cookies = require('js-cookie')
const merge = require('deepmerge')

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

$(document).ready(() => {
  console.log('loaded')
  request('/api/fittings')
    .then(response => {
      if (!response.ok) {
        throw Error(response.statusText)
      }
      return response.json()
    })
})
