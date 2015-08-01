/**
 *
 */

$(document).ready(function() {

  try {
    $("[name=due_date]").val(
      Date
      .parseString($("[name=due_date]").val(), 'yyyy-MM-dd HH:mm:ss')
      .format('NNN dd,yyyy HH:mm a')
    );
  } catch(ex) {}

  $("[name=due_date]").datetimepicker({
    format: 'M d,Y h:i A'
  });

});