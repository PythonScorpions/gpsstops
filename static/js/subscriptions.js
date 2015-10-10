/**
 *
 */

$(document).ready(function() {
  // $(".page .subscription-page .registration-step-4").show();
  // $(".page .subscription-page .registration-step-3").hide();
  // $(".page .subscription-page .registration-step-2").hide();
  // $(".page .subscription-page .registration-step-1").hide();

  $(".page .subscription-page .registration-step-1 button")
  .click(function(event) {
    if ($("input[name=plan]:checked").length <= 0) {
      bootbox.alert("Please Select a Subscription Plan.");
    } else if ($("input[name=confirmation]:checked").length <= 0) {
      bootbox.alert("Please agree to the terms.");
    } else {
      $(".page .subscription-page .registration-steps .step-1")
      .addClass("done")
      .removeClass("active")
      ;
      $(".page .subscription-page .registration-steps .step-2")
      .addClass("active")
      ;

      $(".page .subscription-page .registration-step-2").show();
      $(".page .subscription-page .registration-step-1").hide();

      $("body").scrollTop(0);
    }
  });

  $(".page .subscription-page .registration-step-2 button")
  .click(function(event) {
    if ($("input[name=confirmation]:checked").length <= 0) {
      bootbox.alert("Please agree to the terms.");
    } else {
      $(".page .subscription-page .registration-steps .step-2")
      .addClass("done")
      .removeClass("active")
      ;
      $(".page .subscription-page .registration-steps .step-3")
      .addClass("active")
      ;

      $(".page .subscription-page .registration-step-3").show();
      $(".page .subscription-page .registration-step-2").hide();

      $("body").scrollTop(0);
    }
  });

  $(".page .subscription-page .registration-step-3 button")
  .click(function(event) {
    if (false) {
      // bootbox.alert("Please agree to the terms.");
    } else {
      $(".page .subscription-page .registration-steps .step-3")
      .addClass("done")
      .removeClass("active")
      ;
      $(".page .subscription-page .registration-steps .step-4")
      .addClass("active")
      ;

      $(".page .subscription-page .registration-step-4").show();
      $(".page .subscription-page .registration-step-3").hide();

      $("body").scrollTop(0);
    }
  });
});