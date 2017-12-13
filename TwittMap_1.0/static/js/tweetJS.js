var map = "";
var location_list = [];
var marker_list = [];
var min_zoom = 3;



//Initialize Google Map
function initMap(){
	var nyc_geo = {lat: 40.7128, lng:-74.0059};
	var body = {
				zoom: 4,
				center: nyc_geo
	};
	map = new google.maps.Map(document.getElementById('GoogleMap'), body);

	zoom_limit(); //limit the zoom level
}

// Set the minimum zoom level
function zoom_limit(){
	google.maps.event.addListener(map, 'change_zoom', function(){
		if(map.getZoom()<min_zoom){
			map.setZoom(min_zoom);
		}
	});
}

function place_marker(lat, lng, source){
	var lat_lng = {lat: lat, lng: lng};
	var location = {
					position: lat_lng,
					map: map
				};


	var contentString = '<div id="content">'+
		'<div id="siteNotice">'+
		'</div>'+
		'<h1 id="firstHeading" class="firstHeading">  </h1>'+
		'<div id="bodyContent">'+
		'<p>' + source.author + '</p>' +
		'<p>' + source.text + '</p>' +
		'</div>' +
		'</div>';

	var infowindow = new google.maps.InfoWindow();
	infowindow.setContent(contentString);

	var marker = new google.maps.Marker(location);

	marker.addListener('click', function(){
		infowindow.open(map, marker);
		$("#search_distance").click(function(marker){
			markerClear(marker_list);
			markerClear(location_list);
			//infowindow.open(map, marker);
			clickMarker(lat_lng.lat,lat_lng.lng);
		});
	});

	/*
	marker.addListener('click',function(marker){
			markerClear(marker_list);
			markerClear(location_list);
			//infowindow.open(map, marker);
			clickMarker(lat_lng.lat,lat_lng.lng);
		});
		*/
	console.log("maker" + lat_lng.lat + ", " + lat_lng.lng);
	marker_list.push(marker);
}

function markerClear(list){
	for(var i=0;i<list.length;i++){
		list[i].setMap(null);
	}
}

function loadTweet(list){
		var source_list = list.hits.hits;
		//console.log("load tweet: " + source_list); // for debugging in Chrome
		var location_lat;
		var location_lng;
		for(var i = 0;i<source_list.length;i++) {
			location_lat = source_list[i]._source.location[1]; //latitude
			location_lng = source_list[i]._source.location[0]; //longitude
			//place marker on map
			place_marker(location_lat,location_lng, source_list[i]._source);
			//console.log(location_lat);
		}

	}

function clickMarker(lat,lng){
	var color = '00FF80'; // the color of picked marker
	var image = new google.maps.MarkerImage(
		"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + color,
		new google.maps.Size(80,400),
		new google.maps.Point(0,0),
        new google.maps.Point(10, 34)
		);
	var marker = new google.maps.Marker({
		position: {lat: lat,lng: lng},
		map: map,
		icon: image
	});
	console.log("Place new marker!!!!!")
	var marker_lat = lat;
	var marker_lng = lng;
	location_list.push(marker);
	searchDistance(marker_lat,marker_lng);

}

function searchDistance(lat,lng){
	var keyword = $("#keyword_select").val();
	var distance = $("#distance_select").val();
	var location = [lat,lng];

	console.log("--------keyword: "+keyword+", Distance: "+distance);

	$.ajax({
		url: '/search/' + keyword + '/' + distance + '/' + lat + '/' + lng,
		type: 'POST',
		success: function(result){
			//markerClear(location_list);
			loadTweet(result);
			console.log("Click Marker and load tweets!!!!")
		},
		error: function(error) {
			console.log(JSON.stringify(error));
	}
	});

}

$(document).ready(function() {
	$("#search").click(function(){
		var key = $("#keyword_select").val();
		$.ajax({
			url: '/search/' + key,
			type: 'POST',
			success: function(result) {
				markerClear(marker_list);
				markerClear(location_list);
				loadTweet(result);
				//console.log(JSON.stringify(result));
			},
			error: function(error) {
				console.log(JSON.stringify(error));
		}
		});
	});


});
