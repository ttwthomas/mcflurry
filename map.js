
let map;
function initMap() {
    const montreal = { lat: 45.54, lng: -73.7 }
    map = new google.maps.Map(document.getElementById("map"), {
        center: montreal,
        disableDefaultUI: true,
        zoom: 11,
        styles: [
            {
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#1d2c4d"
                }
              ]
            },
            {
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#8ec3b9"
                }
              ]
            },
            {
              "elementType": "labels.text.stroke",
              "stylers": [
                {
                  "color": "#1a3646"
                }
              ]
            },
            {
              "featureType": "administrative",
              "elementType": "geometry",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "administrative.country",
              "elementType": "geometry.stroke",
              "stylers": [
                {
                  "color": "#4b6878"
                }
              ]
            },
            {
              "featureType": "administrative.land_parcel",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#64779e"
                }
              ]
            },
            {
              "featureType": "administrative.neighborhood",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "administrative.province",
              "elementType": "geometry.stroke",
              "stylers": [
                {
                  "color": "#4b6878"
                }
              ]
            },
            {
              "featureType": "landscape.man_made",
              "elementType": "geometry.stroke",
              "stylers": [
                {
                  "color": "#334e87"
                }
              ]
            },
            {
              "featureType": "landscape.natural",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#023e58"
                }
              ]
            },
            {
              "featureType": "poi",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#283d6a"
                }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#6f9ba5"
                }
              ]
            },
            {
              "featureType": "poi",
              "elementType": "labels.text.stroke",
              "stylers": [
                {
                  "color": "#1d2c4d"
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#023e58"
                }
              ]
            },
            {
              "featureType": "poi.park",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#3C7680"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#304a7d"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "labels",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "labels.icon",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#98a5be"
                }
              ]
            },
            {
              "featureType": "road",
              "elementType": "labels.text.stroke",
              "stylers": [
                {
                  "color": "#1d2c4d"
                }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#2c6675"
                }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "geometry.stroke",
              "stylers": [
                {
                  "color": "#255763"
                }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#b0d5ce"
                }
              ]
            },
            {
              "featureType": "road.highway",
              "elementType": "labels.text.stroke",
              "stylers": [
                {
                  "color": "#023e58"
                }
              ]
            },
            {
              "featureType": "transit",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "transit",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#98a5be"
                }
              ]
            },
            {
              "featureType": "transit",
              "elementType": "labels.text.stroke",
              "stylers": [
                {
                  "color": "#1d2c4d"
                }
              ]
            },
            {
              "featureType": "transit.line",
              "elementType": "geometry.fill",
              "stylers": [
                {
                  "color": "#283d6a"
                }
              ]
            },
            {
              "featureType": "transit.station",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#3a4762"
                }
              ]
            },
            {
              "featureType": "water",
              "elementType": "geometry",
              "stylers": [
                {
                  "color": "#0e1626"
                }
              ]
            },
            {
              "featureType": "water",
              "elementType": "labels.text",
              "stylers": [
                {
                  "visibility": "off"
                }
              ]
            },
            {
              "featureType": "water",
              "elementType": "labels.text.fill",
              "stylers": [
                {
                  "color": "#4e6d70"
                }
              ]
            }
          ]
    });
    addRestaurants(restaurants)
}


function addRestaurants(restaurants){
    for (i in restaurants) {
        let location = {
            "lat":restaurants[i]["location"]["latitude"],
            "lng":restaurants[i]["location"]["longitude"]
        }
        let name = restaurants[i]["name"]
        let unavailable = restaurants[i]["unavailable"]
        let icon = "mcdonalds.png"
        if  (unavailable.length > 0){
            icon = "mcdonalds-unavail.png"
        }
        if  (restaurants[i]["open"] === false ){
            icon = "mcdonalds-closed.png"
        }
        timeout = i*10
        window.setTimeout(() => {
            addMarker(map, location, name, icon, unavailable)
        }, timeout)
    }
}

function addMarker(map, location, name, icon, unavailable) {
    console.log(name)
    console.log(unavailable)
    marker = new google.maps.Marker({
      position: location,
      map: map,
      icon: icon,
    });
    const contentString =
    '<div id="content">' +
    '<h1 id="firstHeading" class="firstHeading">'+ name +'</h1>' +
    '<div id="bodyContent">' +
    '<p>'+ unavailable[0] + '</p>' +
    '</div>' +
    '</div>';
    const infowindow = new google.maps.InfoWindow({
        content: contentString,
    });
    marker.addListener("click", () => {
        infowindow.open(map, marker);
    });
    marker.setAnimation(google.maps.Animation.DROP);
  }
