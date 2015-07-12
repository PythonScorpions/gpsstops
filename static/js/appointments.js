/**
 *
 */

$(document).ready(function() {



  // $("body").append('<div id="appointmentDialog" title="Appointment"></div>');
  // var dialog = $( "#appointmentDialog" ).dialog({
  //   autoOpen: false,
  //   modal: true
  // });

  // $("#appointmentDialog").modal({show:false});

  // $("#appointmentDialog .modal-footer .btn-primary").click(function() {
  //   $.ajax({
  //     url: "/appointments/create/",
  //     method: "POST",
  //     data: $("form[name=appointmentForm").serialize(),
  //     success: function(data, textStatus, jqXHR) {
  //       if (data.status) {
  //         $("#appointmentDialog").modal('hide');
  //       } else {
  //         $("#appointmentDialog .modal-body").html(data);
  //       }
  //     }
  //   });
  // });

  $("[name=start_datetime]").datetimepicker({
    formatTime:'g:i A',
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