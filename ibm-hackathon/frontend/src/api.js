import { reset } from "ansi-colors";

const base = 'http://feedbackaggregation.mybluemix.net/api'


const log = (args) => { console.log(args); return args }

function get(endpoint, query) {
  let uri = base + endpoint

  if (query && query !== {}) {
    const params = Object.entries(query)
      .map(([ key, value ]) => `${key}=${value}`)
      .join('&')
    uri += '?' + params
  }

  return fetch(uri).then(res => res.json())
}

export function getBusinesses() {
  return get('/businesses')
}

export function getReviews(bid, page=0) {
  return get(`/business/${bid}/reviews`, { page }).then(log)
}