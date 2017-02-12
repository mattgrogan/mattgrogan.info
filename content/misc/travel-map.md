+++
date = "2017-01-06"
title = "My travel map"
draft = false
tags = ["Travel", "google-maps"]
+++

<style>

  #map_container {
    position: relative;
    min-height: 400px;
  }

  #map {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
  }

</style>

<div id="map_container" class="panel-body">
  <div id="map"></div>
</div>


<script type="text/javascript">
  function initMap() {

    var mapOptions = {
      zoom: 1,
      center: {
        lat: 30,
        lng: 0
      },
      mapTypeId: google.maps.MapTypeId.TERRAIN,
      panControl: false,
      zoomControl: false,
      mapTypeControl: false,
      scaleControl: false,
      streetViewControl: false,
      overviewMapControl: false
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);

    $.getJSON("/cities.json", function(data) {
      $.each(data, function(key, val) {

        // create the infowindow
        var infowindow = new google.maps.InfoWindow({
          content: val['formatted_address']
        })

        // create the marker
        var marker = new google.maps.Marker({
          map: map,
          position: {
            lat: val['latitude'],
            lng: val['longitude']
          },
          clickable: true,
          title: val['formatted_address'],
          icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 3,
            fillColor: '#de2d26',
            fillOpacity: 0.85,
            strokeColor: '#252525',
            strokeWeight: 1
          }
        });

        // tie the infowindow to the marker
        marker.addListener('mouseover', function() {
          infowindow.open(map, marker);
        });
        marker.addListener('mouseout', function() {
          infowindow.close(map, marker);
        });
      })

    })

  }

</script>

<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD4U3kKYHOvB2DPU6X15vyY2_18hilH5tU&callback=initMap"></script>
