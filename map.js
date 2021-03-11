import { styles } from './styles.js';
import { restaurants } from './missingflurry.js'

export class Map {
  constructor() {
    const montreal = { lat: 45.54, lng: -73.7 };
    this.map = new google.maps.Map(document.getElementById('map'), {
      center: montreal,
      disableDefaultUI: true,
      zoom: 11,
      styles
    });
    this.addRestaurants(restaurants);
  }

  addRestaurants(restaurants) {
    restaurants.forEach((restaurant, index) => {
      let location = {
        lat: restaurant.location.latitude,
        lng: restaurant.location.longitude
      };
      let icon = 'mcdonalds.png';
      if (restaurant.unavailable.length) {
        icon = 'mcdonalds-unavail.png';
      }
      else if (!restaurant.open) {
        icon = 'mcdonalds-closed.png';
      }
      let timeout = index * 10;
      window.setTimeout(() => {
        this.addMarker(location, restaurant.name, icon, restaurant.unavailable)
      }, timeout)
    });
  }

  addMarker(position, name, icon, unavailable) {
    let marker = new google.maps.Marker({
      position,
      map: this.map,
      icon,
    });
    let unavailable_div_content = '';
    unavailable.forEach(item => unavailable_div_content += `${item} </br>`);
    let unavailable_div = `<div>${unavailable_div_content}</div>`;
    const content =
      `<div id="content">
        <h1 id="firstHeading" class="firstHeading"> ${name} </h1>
        <div id="bodyContent">
          <p>Missing items:</p>
            ${unavailable_div} 
        </div>
      </div>`;
    const infowindow = new google.maps.InfoWindow({
      content
    });
    marker.addListener('click', () => infowindow.open(this.map, marker));
    marker.setAnimation(google.maps.Animation.DROP);
  }

}