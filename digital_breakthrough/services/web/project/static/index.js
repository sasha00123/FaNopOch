layer_buttons = document.getElementById("layer_buttons");
main_img = document.getElementById("main_img");

function onMouseDown(event) {
    // this - button
    let button = this.children[0];
    let img = document.getElementById("img-" + button.value);
    if (img.style.opacity === "0") {
        // Enable img
        img.style.opacity = "0.5";
        button.style.backgroundColor = "#CCCCCC";
    } else {
        // Disable img
        img.style.opacity = "0";
        button.style.backgroundColor = "#f8f9fa";
    }

}

let map;

lng.textContent = event_data[0][0];
lat.textContent = event_data[0][1];

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: event_data[0][0], lng: event_data[0][1] },
        zoom: 15,
        mapTypeId: "satellite"
    });

    marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(event_data[0][0], event_data[0][1])
    });
    infowindow = new google.maps.InfoWindow({
        content: "<div style='float:left'><img style='max-width: 200px' src='static/photos/" + event_id + ".jpg'></div>"
    });
    google.maps.event.addListener(map, 'click', function() {
        infowindow.open(map, marker);
    });
    infowindow.open(map, marker);


    google.maps.event.addListener(map, 'zoom_changed', function() {
        zoomLevel = map.getZoom();
        scale_map.textContent = zoomLevel;
    });
    var polygon = new google.maps.Polygon({
        map: map,
        path: event_data.map(e => {return {lat: e[0], lng: e[1]}}),
        name: "polygon",
        fillColor: "red"
    });
}
