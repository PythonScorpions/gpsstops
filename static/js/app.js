
/**********************************
 * Notifications and online users
 **********************************/

$(document).ready(function() {

    function getTodayAppointments () {
        var reqData = {
            user: $("[name=user_id][type=hidden]").val(),
            date: $.datepicker.formatDate('mm/dd/yy', new Date())
        }
        $.ajax({
            url: '/api/appointments/?' + $.param(reqData),
            success: function(data, textStatus, jqXHR) {
                if ( data.code == 1 ) {
                    for(var i=0, appointment; appointment = data.data[i]; i++) {
                        console.log("Appointment: ", appointment.notification_required);
                        if (appointment.notification_required) {
                            var cur_dt_in_secs = Math.floor((new Date()).getTime() / 1000);
                            var given_dt_in_secs = Math.floor((new Date(appointment.start_datetime)).getTime() / 1000);

                            var diff = (given_dt_in_secs - cur_dt_in_secs);
                            var required_diff = (appointment.notification_time * 60);

                            if ( diff >= 0 && diff <= required_diff ) {
                                $.notify("You have an appointment " + appointment.title + " on " + appointment.start_datetime, 'info');
                            }
                        } else {
                            console.log("Notification not required");
                        }
                    }
                }
            }
        });
    }

    function getTodayTasks () {
        var reqData = {
            user: $("[name=user_id][type=hidden]").val(),
            date: $.datepicker.formatDate('mm/dd/yy', new Date())
        }
        $.ajax({
            url: '/api/task/?' + $.param(reqData),
            success: function(data, textStatus, jqXHR) {
                if ( data.code == 1 ) {
                    for(var i=0, task; task = data.data[i]; i++) {
                        console.log("Task: ", task.notification_required);
                        if (task.notification_required) {
                            var cur_dt_in_secs = Math.floor((new Date()).getTime() / 1000);
                            var given_dt_in_secs = Math.floor((new Date(task.due_date)).getTime() / 1000);

                            var diff = (given_dt_in_secs - cur_dt_in_secs);
                            var required_diff = (task.notification_time * 60);

                            if ( diff >= 0 && diff <= required_diff ) {
                                $.notify("You have an task " + task.title + " on " + task.due_date, 'info');
                            }
                        } else {
                            console.log("Notification not required");
                        }
                    }
                }
            }
        });
    }

    getTodayAppointments();
    getTodayTasks();
    // $.notify("Do not press this button", "info");
});