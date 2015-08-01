/**
 *
 */

$(document).ready(function() {

  try {
    $("[name=start_datetime]").val(
      Date
      .parseString($("[name=start_datetime]").val(), 'yyyy-MM-dd HH:mm:ss')
      .format('NNN dd,yyyy HH:mm a')
    );
  } catch(ex) {}

  $("[name=start_datetime]").datetimepicker({
    format: 'M d,Y h:i A'
  });

  var searchBox = new google.maps.places.SearchBox($("[name=where]")[0]);
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    var places = searchBox.getPlaces();
    if (places.length == 0) {
      return;
    }

    for (var i=0, place; place = places[i]; i++) {
      console.log(place);
      console.log(place.geometry.location.lat());
      console.log(place.geometry.location.lng());
      console.log(place.geometry.location);

      $("[name=latitude]").val(place.geometry.location.lat());
      $("[name=longitude]").val(place.geometry.location.lng());
      $("[name=location]").val(place.formatted_address);
    }
  });
});