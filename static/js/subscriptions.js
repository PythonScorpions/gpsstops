/**
 *
 */

var bindPlanEvents = function() {
  $(".page .subscription-page .registration-step .plans .plan")
  .click(function(event) {
    $(this).find("input[type=radio]").attr("checked", "checked");
  });
};

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

    return false;
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

    return false;
  });

  $(".page .subscription-page .registration-step-3 button")
  .click(function(event) {
    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/signup",
      data: $("form").serialize(),
      success: function(data, textStatus, jqXHR) {
        console.log(data, typeof(data));
        if (typeof(data) == 'object' && data.state == "success") {
          $("#paypal").attr("href", data.url);

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
        } else if (typeof(data) == 'string') {
          $("div#form").html(data);
        }
      }
    });

    return false;
  });

  bindPlanEvents();
});