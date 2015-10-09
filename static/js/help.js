/**
 *
 */

$(document).ready(function() {
  $("body").on("click", ".help-section-handler", function(event) {
    var section = $(this).data("section");
    console.log(section);

    $("#helpModal .modal-body").html("Loading....");
    $.get('/help/?section=' + section, function(data) {
      if (data) {
        $("#helpModal .modal-body").html(data);
      } else {
        $("#helpModal .modal-body").html("Error loading help section.");
      }
      $("#helpModal").modal("show");
    });

    return false;
  });
});