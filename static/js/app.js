
/**********************************
 * Notifications and online users
 **********************************/

$(document).ready(function() {

    // notifications.onlineCount(function (count) {
    //     setUserCount(count);
    // });


    // notifications.onlineCountChange(function (count) {
    //     setUserCount(count);
    // });


    // function setUserCount(count) {
    //     // document.getElementById("users-online").innerHTML = count;
    //     console.log(count);
    // }

    // notifications.onNotification(addNotification);
    // notifications.enableDesktopNotifications();


    // function addNotification(notification) {
    //     var li = document.createElement("li");
    //     li.innerHTML = notification.name + ' - ' + notification.timestamp;
    //     var notificationsList = document.getElementById("notifications");
    //     notificationsList.insertBefore(li, notificationsList.firstChild);

    //     notifications.desktopNotification('New foo', {body: notification.name, icon: notification.icon, tag: 'foo'});
    // }

    function getTodayAppointments () {
        var reqData = {
            user: $("[name=user_id][type=hidden]").val(),
            date: $.datepicker.formatDate('mm/dd/yy', new Date())
        }
        $.ajax({
            url: '/api/appointments/?' + $.param(reqData),
            success: function(data, textStatus, jqXHR) {
                console.log(data);
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
                console.log(data);
            }
        });
    }

    getTodayAppointments();
    getTodayTasks();
});