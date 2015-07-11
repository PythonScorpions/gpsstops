/**
 *
 */

$(document).ready(function() {

  // $("body").append('<div id="appointmentDialog" title="Appointment"></div>');
  // var dialog = $( "#appointmentDialog" ).dialog({
  //   autoOpen: false,
  //   modal: true
  // });

  $("#appointmentDialog").modal({show:false});

  $("#appointmentDialog .modal-footer .btn-primary").click(function() {
    $.ajax({
      url: "/appointments/create/",
      method: "POST",
      data: $("form[name=appointmentForm").serialize(),
      success: function(data, textStatus, jqXHR) {
        if (data.status) {
          $("#appointmentDialog").modal('hide');
        } else {
          $("#appointmentDialog .modal-body").html(data);
        }
      }
    });
  });

});