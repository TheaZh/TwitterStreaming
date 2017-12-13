var map = "";
var location_list = [];
var marker_list = [];
var min_zoom = 2;

//Initialize Google Map
var nyc_geo = {lat: 40.7128, lng:-74.0059};
var body = {
				zoom: 4,
				center: nyc_geo};
map = new google.maps.Map(document.getElementById('GoogleMap'), body);
zoom_limit(); //limit the zoom level


// Set the minimum zoom level
function zoom_limit(){
	google.maps.event.addListener(map, 'change_zoom', function(){
		if(map.getZoom()<min_zoom){
			map.setZoom(min_zoom);
		}
	});
}

//map
