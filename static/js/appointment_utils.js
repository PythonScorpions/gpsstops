/**
 *
 */

$(function() {
  $("form field-row").addClass("form-group");
  $("form input:not(:checkbox), form select, form textarea").addClass("form-control");
  $("form input[type=submit]").addClass("btn btn-primary");

  var stopChecking = false, elVal = '';
  var el = $('[name=is_editable]').parents('.field-row');

  if ($('select[name=user]').find('option:selected').text() == 'Self') {
    $(el).find('[name=is_editable]').prop('checked', 'checked');
    $(el).hide();
  } else {
    elVal = $('[name=is_editable]').prop('checked') ? 'checked': '';
  }

  $('select[name=user]').change(function(event) {
    if($(this).find('option:selected').text() == 'Self') {
      $(el).find('[name=is_editable]').prop('checked', 'checked');
      $(el).hide();
    } else {
      if (!stopChecking) {
        $(el).find('[name=is_editable]').prop('checked', elVal);
      } else {
        $(el).find('[name=is_editable]').prop('checked', '');
      }
      $(el).show();
    }
  });

  $('[name=is_editable]').click(function() {
    stopChecking = true;
  });
});