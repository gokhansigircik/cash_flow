// const key = 'pu the api key'

// const getCity = async (city) => {

//     const base = 'http://dataservice.accuweather.com/locations/v1/cities/search';
//     const query = ?apikey={key}&q=${city};

//     const response = await fetch(base + query)
//     const data = await response.json();

//     return (date[0]);

// }
// getCity('London')
//     .then(data => console.log(data))
//     .catch(err => console.log(err));


const axios = require("axios");

const options = {
  method: 'GET',
  url: 'https://wft-geo-db.p.rapidapi.com/v1/geo/cities',
  headers: {
    'X-RapidAPI-Key': '6d066a5a08msh16ee73b456205f5p1c8173jsnf33a0fb821e9',
    'X-RapidAPI-Host': 'wft-geo-db.p.rapidapi.com'
  }
};

axios.request(options).then(function (response) {
	console.log(response.data);
}).catch(function (error) {
	console.error(error);
});