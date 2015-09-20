/**
 * Extra scripting for theme
 */

$(document).ready(function() {
  $(".hamburger-inner .bar").removeClass("hidden");
  $("#login-block").hide();

  $("#login").click(function(event) {
    $("#login-block").toggle("fade slide");
    console.log("reached");
  });
});