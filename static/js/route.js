/**
 *
 */

var start_lat;
var start_long;
var input_first;
var input_last;
var searchBox_first;
var searchBox_last;
var map;
var markers = [];
var hotel_markers = [];
var food_markers = [];
var gas_markers = [];
var autocomplete = [];
var autocompleteOptions = {};
var waypoints = [];
var last_waypoint_no = 0;
var hotel_status = false;
var food_status = false;
var gas_status = false;
var traffic_status = false;

$(function() {

    $("#myList").sortable({
        axis : 'y',
        items : '.title',
        start: function () {
            // To keep Add more waypoint button fixed
            $(this).find("li:not(.title)").each(function () {
                $(this).data("fixedIndex", $(this).index());
            });
        },
        change: function () {
            // To keep Add more waypoint button fixed
            $(this).find("li:not(.title)").each(function () {
                $(this).detach().insertAfter($("#myList li:eq(" + ($(this).data("fixedIndex")-1) + ")"));
            });

            setTimeout(function() {
                changeIds();
            }, 1000);
            setTimeout(function() {
               calcRoute();
            }, 1000);
        }
    });
});

function check_validation() {
    var flag = false;
    if($('#trip_title').val() == ''){
        flag = true;
        $(".error_title").show();
    }
    else{
        $(".error_title").hide();
    }
    if($('#datepicker').val() == ''){
        flag = true;
        $(".error_datetime").show();
    }
    else{
        $(".error_datetime").hide();
    }
    $('.loc').each(function(i, obj) {
        var near_address_common = $(this).find(".near_address_common");
        if(i==0){
            title_error = '#error_title1';
        }
        else{
            if(last_waypoint_no == 0){
                title_error = '#error_title2';
            }
            else{
                if(last_waypoint_no+1 == i){
                    title_error = '#error_title2';
                }

                else{
                    title_error = '#error_title'+(i+2);
                }
            }
        }
        if(near_address_common.val() == ''){
            flag = true;
            $(title_error).show();
        }
        else{
            $(title_error).hide();
        }
    });
    if(flag==false){
        $( ".manual_view" ).submit();
    }
}

function way_point_weathers(w){

    if(w == last_waypoint_no){
        return;
    }
    var cmn_var = w+3;
    var lat_var = w+1;
    var lng_var = w+1;
    console.log(cmn_var);
    if($("#cmn"+cmn_var+"").val() != ""){

        console.log(lat_var);
        console.log(lng_var);
        var lat = $("#latitude"+lat_var+"").val();
        var lng = $("#longitude"+lng_var+"").val();
        selected_date = new Date(Date.parse($("#datepicker").val()));
        selected_day = selected_date.getDate();
        selected_month = selected_date.getMonth();
        selected_year = selected_date.getFullYear();
        weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+lat+"&lon="+lng+"&cnt=16&units=imperial";
        console.log(weather_url);

        $.get(weather_url, function(data, status){
            flag = false;
            for(var f=0;f<data.list.length;++f){
                var date = new Date(data.list[f].dt * 1000);
                var day = date.getDate();
                var month = date.getMonth();
                var year = date.getFullYear();
                if(selected_day==day && selected_month==month && selected_year==year){
                    var description = data.list[f].weather[0].description;
                    var clouds = (data.list[f].temp.min+data.list[f].temp.min)/2 +' F';
                    var wind_speed = data.list[f].speed + ' ml/h';
                    var humidity = data.list[f].humidity + '%';
                    console.log(description);
                    $(".desc_"+lat_var+"").text(description);
                    $(".fer_"+lat_var+"").text(clouds);
                    $(".wind_"+lat_var+"").text(wind_speed);
                    $(".hum_"+lat_var+"").text(humidity);
                    flag = true;
                    break
                }
            }
            if(flag == false){
                $(".desc_"+lat_var+"").text('Weather Forecast Not available at this day');
                $(".fer_"+lat_var+"").text('');
                $(".wind_"+lat_var+"").text('');
                $(".hum_"+lat_var+"").text('');
            }
        });

    }
    else{
        $(".desc_"+lat_var+"").text('');
        $(".fer_"+lat_var+"").text('');
        $(".wind_"+lat_var+"").text('');
        $(".hum_"+lat_var+"").text('');
    }

    setTimeout(function()
    {
        way_point_weathers(w + 1);

    }, 2000);

}

function changeIds() {

    $('.loc').each(function(i, obj) {
        var near_address_common = $(this).find(".near_address_common");
        var address_common = $(this).find(".address_common");
        var note_common = $(this).find(".note_common");
        var lat_common = $(this).find(".lat_common");
        var lng_common = $(this).find(".lng_common");
        var delete_a = $(this).find(".delete_waypoint");
        var errors = $(this).find(".errors");
        var infos = $(this).find(".info");
        var stop_hs = $(this).find(".stop_calc");
        var descs = $(this).find(".descs");
        var fers = $(this).find(".fers");
        var winds = $(this).find(".winds");
        var hums = $(this).find(".hums");

        var prefix = "way_loc";
        var classes = obj.className.split(" ").filter(function(c) {
            return c.lastIndexOf(prefix, 0) !== 0;
        });
        obj.className = $.trim(classes.join(" "));

        descs.removeAttr('class');
        fers.removeAttr('class');
        winds.removeAttr('class');
        hums.removeAttr('class');

        if(i==0){
            address_common.attr('placeholder', 'Start Location');
            address_common.attr('name', 'start_search_address');
            near_address_common.attr('name', 'start_near_address');
            note_common.attr('name', 'start_note_location');
            lat_common.attr('name', 'latitude_first');
            lat_common.attr('id', 'latitude_first');
            lng_common.attr('name', 'longitude_first');
            lng_common.attr('id', 'longitude_first');
            near_address_common.attr('id', 'address1');
            address_common.attr('id', 'cmn1');
            errors.attr('id', 'error_title1');
            address_common.css('background-color', '#AFBFCD');
            $(delete_a).remove();
            $(stop_hs).remove();
            descs.addClass( "descs" );
            descs.addClass( "desc_first" );
            fers.addClass( "fers" );
            fers.addClass( "fer_first" );
            winds.addClass( "winds" );
            winds.addClass( "wind_first" );
            hums.addClass( "hums" );
            hums.addClass( "hum_first" );

        }
        else{
            if(last_waypoint_no == 0){
                address_common.attr('placeholder', 'End Location');
                address_common.attr('name', 'end_search_address');
                near_address_common.attr('name', 'end_near_address');
                note_common.attr('name', 'end_note_location');
                lat_common.attr('name', 'latitude_last');
                lat_common.attr('id', 'latitude_last');
                lng_common.attr('name', 'longitude_last');
                lng_common.attr('id', 'longitude_last');
                near_address_common.attr('id', 'address2');
                address_common.attr('id', 'cmn2');
                errors.attr('id', 'error_title2');
                address_common.css('background-color', '#AFBFCD');
                $(delete_a).remove();
                $(stop_hs).remove();
                infos.after("<div class='stop_calc'><input type='text' readonly='true' name='stop_distance' class='map-input stop_distance' " +
                "placeholder='Stop Distance' style='font-weight: bold; color: blue;'/><input type='text' readonly='true' " +
                "name='stop_hours' class='map-input stop_hours' placeholder='Stop Hours' style='font-weight: bold; color: blue;'/> " +
                "</div>");
                descs.addClass( "descs" );
                descs.addClass( "desc_last" );
                fers.addClass( "fers" );
                fers.addClass( "fer_last" );
                winds.addClass( "winds" );
                winds.addClass( "wind_last" );
                hums.addClass( "hums" );
                hums.addClass( "hum_last" );
            }
            else{
                if(last_waypoint_no+1 == i){
                    address_common.attr('placeholder', 'End Location');
                    address_common.attr('name', 'end_search_address');
                    near_address_common.attr('name', 'end_near_address');
                    note_common.attr('name', 'end_note_location');
                    lat_common.attr('name', 'latitude_last');
                    lat_common.attr('id', 'latitude_last');
                    lng_common.attr('name', 'longitude_last');
                    lng_common.attr('id', 'longitude_last');
                    near_address_common.attr('id', 'address2');
                    address_common.attr('id', 'cmn2');
                    errors.attr('id', 'error_title2');
                    address_common.css('background-color', '#AFBFCD');
                    $(delete_a).remove();
                    $(stop_hs).remove();
                    infos.after("<div class='stop_calc'><input type='text' readonly='true' name='stop_distance' class='map-input stop_distance' " +
                "placeholder='Stop Distance' style='font-weight: bold; color: blue;'/><input type='text' readonly='true' " +
                "name='stop_hours' class='map-input stop_hours' placeholder='Stop Hours' style='font-weight: bold; color: blue;'/> " +
                "</div>");
                    descs.addClass( "descs" );
                    descs.addClass( "desc_last" );
                    fers.addClass( "fers" );
                    fers.addClass( "fer_last" );
                    winds.addClass( "winds" );
                    winds.addClass( "wind_last" );
                    hums.addClass( "hums" );
                    hums.addClass( "hum_last" );
                }
                else{
                    var way_li_class = 'way_loc_'+i;
                    $(obj).addClass(way_li_class);
                    address_common.attr('placeholder', 'Stop '+ i );
                    address_common.attr('name', 'search_address'+i);
                    near_address_common.attr('name', 'near_address'+i);
                    note_common.attr('name', 'note_waypoint'+i);
                    lat_common.attr('name', 'latitude'+i);
                    lat_common.attr('id', 'latitude'+i);
                    lng_common.attr('name', 'longitude'+i);
                    lng_common.attr('id', 'longitude'+i);
                    near_address_common.attr('id', 'address'+(i+2));
                    address_common.attr('id', 'cmn'+(i+2));
                    errors.attr('id', 'error_title'+(i+2));
                    $(delete_a).remove();
                    address_common.after("<a id='"+i+"' class='delete_waypoint'><i class='glyphicon glyphicon-remove' style='color: #CD3C58;'></i></a>");
                    address_common.css('background-color', '');
                    $(stop_hs).remove();
                    infos.after("<div class='stop_calc'><input type='text' readonly='true' name='stop_distance' class='map-input stop_distance' " +
                "placeholder='Stop Distance' style='font-weight: bold; color: blue;'/><input type='text' readonly='true' " +
                "name='stop_hours' class='map-input stop_hours' placeholder='Stop Hours' style='font-weight: bold; color: blue;'/> " +
                "</div>");
                    descs.addClass( "descs" );
                    descs.addClass( "desc_"+i );
                    fers.addClass( "fers" );
                    fers.addClass( "fer_"+i );
                    winds.addClass( "winds" );
                    winds.addClass( "wind_"+i );
                    hums.addClass( "hums" );
                    hums.addClass( "hum_"+i );
                }
            }
        }
    });

    var current_classes = $('.pac-input').length;
    for(var r=0;r<autocomplete.length;++r){
        google.maps.event.clearListeners(autocomplete[r], 'place_changed');
    }
    autocomplete = [];
    for(var k=0; k<current_classes;k++) {
        if (k != 0 && k != current_classes - 1) {
            alreadyInput = [];
            alreadyInput.push($('.pac-input')[k]);
            setupAutocomplete(autocomplete, alreadyInput, 0, k);
        }
    }
    console.log(searchBox_first);
    google.maps.event.clearListeners(searchBox_first, 'place_changed');
    google.maps.event.clearListeners(searchBox_last, 'place_changed');
    input_first = $('.pac-input')[0];
    input_last = $('.pac-input')[current_classes-1];
    console.log(input_first);
    console.log(input_last);
    // map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    searchBox_first = new google.maps.places.SearchBox((input_first));
// {#    console.log(searchBox_first);#}
    searchBox_last = new google.maps.places.SearchBox((input_last));

    google.maps.event.addListener(searchBox_first, 'places_changed', function() {
        console.log("searchbox first");
        var places = searchBox_first.getPlaces();
        if (places.length == 0) {
            return;
        }
        for (var i = 0, marker; marker = markers[i]; i++) {
            marker.setMap(null);
        }
        // For each place, get the icon, place name, and location.
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0, place; place = places[i]; i++) {
              // Create a marker for each place.
            marker = new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location,
            });
            $("#latitude_first").val(place.geometry.location.lat());
            $("#longitude_first").val(place.geometry.location.lng());
            updateMarkerPosition(marker.getPosition());
            geocodePosition(marker.getPosition(),'1');

            if($("#datepicker").val() != ""){
                selected_date = new Date(Date.parse($("#datepicker").val()));
                selected_day = selected_date.getDate();
                selected_month = selected_date.getMonth();
                selected_year = selected_date.getFullYear();
                weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+place.geometry.location.lat()+"&lon="+place.geometry.location.lng()+"&cnt=16&units=imperial";


                $.get(weather_url, function(data, status){
                    flag = false;
                    console.log(data);
                    for(f=0;f<data.list.length;++f){
                        var date = new Date(data.list[f].dt * 1000);
                        var day = date.getDate();
                        var month = date.getMonth();
                        var year = date.getFullYear();
                        if(selected_day==day && selected_month==month && selected_year==year){
                            description = data.list[f].weather[0].description;
                            clouds = (data.list[f].temp.min+data.list[f].temp.min)/2 +' F';
                            wind_speed = data.list[f].speed + ' ml/h';
                            humidity = data.list[f].humidity + '%';
                            $(".desc_first").text(description);
                            $(".fer_first").text(clouds);
                            $(".wind_first").text(wind_speed);
                            $(".hum_first").text(humidity);
                            flag = true;
                            break
                        }
                    }
                    if(flag == false){
                        $(".desc_first").text('Weather Forecast Not available at this day');
                        $(".fer_first").text('');
                            $(".wind_first").text('');
                            $(".hum_first").text('');
                    }
                });
            }
            else{
                $(".desc_first").text('');
                $(".fer_first").text('');
                $(".wind_first").text('');
                $(".hum_first").text('');
            }

            google.maps.event.addListener(marker, 'dragend', function() {
                geocodePosition(marker.getPosition(),'1');
                $("#latitude_first").val(marker.getPosition().lat());
                $("#longitude_first").val(marker.getPosition().lat());
            });
            markers.push(marker);
            bounds.extend(place.geometry.location);
        }

        if($('#address2').val().length > 0 && $('#address2').val() != 'undefined')
        {
            console.log("searchbox last make route");
            setTimeout(function() {
                calcRoute();
            }, 1000);
        }
        else{
            map.fitBounds(bounds);
            map.setZoom(9);
        }
    });

    // End Place Search Box
    google.maps.event.addListener(searchBox_last, 'places_changed', function() {
        console.log("searchbox last");
        var places1 = searchBox_last.getPlaces();
        if (places1.length == 0) {
            return;
        }
        for (var i = 0, marker; marker = markers[i]; i++) {
            marker.setMap(null);
        }
        // For each place, get the icon, place name, and location.
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0, place; place = places1[i]; i++) {
        // Create a marker for each place.
            marker = new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location
            });
            $("#latitude_last").val(place.geometry.location.lat());
            $("#longitude_last").val(place.geometry.location.lng());
            updateMarkerPosition(marker.getPosition());
            geocodePosition(marker.getPosition(),'2');

            if($("#datepicker").val() != ""){
                selected_date = new Date(Date.parse($("#datepicker").val()));
                selected_day = selected_date.getDate();
                selected_month = selected_date.getMonth();
                selected_year = selected_date.getFullYear();
                weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+place.geometry.location.lat()+"&lon="+place.geometry.location.lng()+"&cnt=16&units=imperial";

                flag = false;
                $.get(weather_url, function(data, status){
                    console.log(data);
                    for(f=0;f<data.list.length;++f){
                        var date = new Date(data.list[f].dt * 1000);
                        var day = date.getDate();
                        var month = date.getMonth();
                        var year = date.getFullYear();
                        if(selected_day==day && selected_month==month && selected_year==year){
                            description = data.list[f].weather[0].description;
                            clouds = (data.list[f].temp.min+data.list[f].temp.min)/2 +' F';
                            wind_speed = data.list[f].speed + ' ml/h';
                            humidity = data.list[f].humidity + '%';
                            $(".desc_last").text(description);
                            $(".fer_last").text(clouds);
                            $(".wind_last").text(wind_speed);
                            $(".hum_last").text(humidity);
                            flag = true
                            break
                        }
                    }
                    if(flag == false){
                        $(".desc_last").text('Weather Forecast Not available at this day');
                        $(".fer_last").text('');
                            $(".wind_last").text('');
                            $(".hum_last").text('');
                    }
                });
            }
            else{
                $(".desc_last").text('');
                $(".fer_last").text('');
                $(".wind_last").text('');
                $(".hum_last").text('');
            }

            google.maps.event.addListener(marker, 'dragend', function() {
                geocodePosition(marker.getPosition(),'2');
                $("#latitude_last").val(marker.getPosition().lat());
                $("#longitude_last").val(marker.getPosition().lat());
            });
            markers.push(marker);
            bounds.extend(place.geometry.location);
        }

        if($('#address1').val().length > 0 && $('#address1').val() != 'undefined')
        {
            console.log("searchbox last make route");
            setTimeout(function() {
                calcRoute();
            }, 500);
        }
        else{
            map.fitBounds(bounds);
            map.setZoom(9);
        }
    });

    if($("#datepicker").val() != ""){
            if($("#cmn1").val() != ""){
                lat = $("#latitude_first").val();
                lng = $("#longitude_first").val();
                selected_date = new Date(Date.parse($("#datepicker").val()));
                selected_day = selected_date.getDate();
                selected_month = selected_date.getMonth();
                selected_year = selected_date.getFullYear();
                weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+lat+"&lon="+lng+"&cnt=16&units=imperial";

                $.get(weather_url, function(data, status){
                    flag = false;
                    for(f=0;f<data.list.length;++f){
                        var date = new Date(data.list[f].dt * 1000);
                        var day = date.getDate();
                        var month = date.getMonth();
                        var year = date.getFullYear();
                        if(selected_day==day && selected_month==month && selected_year==year){
                            console.log(data.list[f]);
                            description = data.list[f].weather[0].description;
                            clouds = (data.list[f].temp.min+data.list[f].temp.min)/2 +' F';
                            wind_speed = data.list[f].speed + ' ml/h';
                            humidity = data.list[f].humidity + '%';
                            $(".desc_first").text(description);
                            $(".fer_first").text(clouds);
                            $(".wind_first").text(wind_speed);
                            $(".hum_first").text(humidity);
                            flag = true
                            break
                        }
                    }
                    if(flag == false){
                        $(".desc_first").text('Weather Forecast Not available at this day');
                        $(".fer_first").text('');
                            $(".wind_first").text('');
                            $(".hum_first").text('');
                    }
                });
            }
            else{
                $(".desc_first").text('');
                $(".fer_first").text('');
                $(".wind_first").text('');
                $(".hum_first").text('');
            }
            if($("#cmn2").val() != ""){
                lat = $("#latitude_last").val();
                lng = $("#longitude_last").val();
                selected_date = new Date(Date.parse($("#datepicker").val()));
                selected_day = selected_date.getDate();
                selected_month = selected_date.getMonth();
                selected_year = selected_date.getFullYear();
                weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+lat+"&lon="+lng+"&cnt=16&units=imperial";

                $.get(weather_url, function(data, status){
                    flag = false;
                    for(f=0;f<data.list.length;++f){
                        var date = new Date(data.list[f].dt * 1000);
                        var day = date.getDate();
                        var month = date.getMonth();
                        var year = date.getFullYear();
                        if(selected_day==day && selected_month==month && selected_year==year){
                            console.log(data.list[f]);
                            description = data.list[f].weather[0].description;
                            clouds = (data.list[f].temp.min+data.list[f].temp.min)/2 +' F';
                            wind_speed = data.list[f].speed + ' ml/h';
                            humidity = data.list[f].humidity + '%';
                            $(".desc_last").text(description);
                            $(".fer_last").text(clouds);
                            $(".wind_last").text(wind_speed);
                            $(".hum_last").text(humidity);
                            flag = true
                            break
                        }
                    }
                    if(flag == false){
                        $(".desc_last").text('Weather Forecast Not available at this day');
                        $(".fer_last").text('');
                            $(".wind_last").text('');
                            $(".hum_last").text('');
                    }
                });
            }
            else{
                $(".desc_last").text('');
                $(".fer_last").text('');
                $(".wind_last").text('');
                $(".hum_last").text('');
            }

            way_point_weathers(0);
        }

}

$(document).on("click",".delete_waypoint", function() {
    $('.way_loc_'+$(this).attr('id')).remove();
    last_waypoint_no -= 1;
    $('.total_waypoint').val(last_waypoint_no);

    setTimeout(function() {
        changeIds();
    }, 1000);
    if($('#address1').val().length > 0 && $('#address2').val().length >0) {
        setTimeout(function () {
            calcRoute();
        }, 1000);
    }
});

$(document).on("input",".address_common", function() {
    if(this.value != ''){
        var id = this.id.slice('-1');
        var near_id = '#address' + id;
        $(near_id).val('');
    }
});

function setAllMap(map, item_markers) {
  for (var i = 0; i < item_markers.length; i++) {
    item_markers[i].setMap(map);
  }
}

$(document).ready(function(){

    $('.manual_view').areYouSure( {'message':'Your Route Details are not saved yet!'} );

    $(window).keydown(function(event){
        if(event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    });

    $('.show_hotels').on('click', function(){
        hotel_status ^= true;
        if(hotel_status == true){
            $('.show_hotels').text('Hide Hotels');
            var path = route.overview_path;
            var boxes = rboxer.box(path, 0.1);

            for (var u = 0; u < boxes.length; u++) {
                var bounds = boxes[u];
                var request = {
                    bounds: bounds,
                    types: ['lodging']
                };
                service.nearbySearch(request, callback);
            }

            function callback(results, status) {
                if (status == google.maps.places.PlacesServiceStatus.OK) {
                    for (var i = 0; i < results.length; i++) {
                        var place = results[i];
                        var marker = new google.maps.Marker({
                            map: map,
                            position: place.geometry.location,
                            icon: 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png'
                        });
                        hotel_markers.push(marker);
                        google.maps.event.addListener(marker, 'click', function() {
                            infowindow.setContent(place.name);
                            infowindow.open(map, this);
                        });
                    }
                }
            }
        }
        else{
            $('.show_hotels').text('Find Hotels');
            setAllMap(null, hotel_markers);
        }

    });

    $('.show_food').on('click', function(){
        food_status ^= true;
        if(food_status == true){
            $('.show_food').text('Hide Food');
            var path = route.overview_path;
            var boxes = rboxer.box(path, 0.1);

            for (var u = 0; u < boxes.length; u++) {
                var bounds = boxes[u];
                var request = {
                    bounds: bounds,
                    types: ['food']
                };
                service.nearbySearch(request, callback);
            }

            function callback(results, status) {
                if (status == google.maps.places.PlacesServiceStatus.OK) {
                    for (var i = 0; i < results.length; i++) {
                        var place = results[i];
                        var marker = new google.maps.Marker({
                            map: map,
                            position: place.geometry.location,
                            icon: 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'
                        });
                        food_markers.push(marker);
                        google.maps.event.addListener(marker, 'click', function() {
                            infowindow.setContent(place.name);
                            infowindow.open(map, this);
                        });
                    }
                }
            }
        }
        else{
            $('.show_food').text('Find Food');
            setAllMap(null, food_markers);
        }

    });

    $('.show_gas').on('click', function(){
        gas_status ^= true;
        if(gas_status == true){
            $('.show_gas').text('Hide GasStations');
            var path = route.overview_path;
            var boxes = rboxer.box(path, 0.6);

            for (var u = 0; u < boxes.length; u++) {
                var bounds = boxes[u];
                var request = {
                    bounds: bounds,
                    types: ['gas_station']
                };
                service.nearbySearch(request, callback);
            }

            function callback(results, status) {
                if (status == google.maps.places.PlacesServiceStatus.OK) {
                    for (var i = 0; i < results.length; i++) {
                        var place = results[i];
                        var marker = new google.maps.Marker({
                            map: map,
                            position: place.geometry.location,
                            icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
                        });
                        gas_markers.push(marker);
                        google.maps.event.addListener(marker, 'click', function() {
                            infowindow.setContent(place.name);
                            infowindow.open(map, this);
                        });
                    }
                }
            }
        }
        else{
            $('.show_gas').text('Find GasStations');
            setAllMap(null, gas_markers);
        }

    });

    $('.show_traffic').on('click', function() {
        traffic_status ^= true;
        if (traffic_status == true) {
            trafficLayer.setMap(map);
            $('.show_traffic').text('Hide Traffic');
        }
        else {
            trafficLayer.setMap(null);
            $('.show_traffic').text('Find Traffic');
        }
    });

    $('#datepicker').on('change', function(){
        console.log("datepicker chnaged");
        if($("#datepicker").val() != ""){
            if($("#cmn1").val() != ""){
                lat = $("#latitude_first").val();
                lng = $("#longitude_first").val();
                selected_date = new Date(Date.parse($("#datepicker").val()));
                selected_day = selected_date.getDate();
                selected_month = selected_date.getMonth();
                selected_year = selected_date.getFullYear();
                weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+lat+"&lon="+lng+"&cnt=16&units=imperial";

                $.get(weather_url, function(data, status){
                    flag = false;
                    for(f=0;f<data.list.length;++f){
                        var date = new Date(data.list[f].dt * 1000);
                        var day = date.getDate();
                        var month = date.getMonth();
                        var year = date.getFullYear();
                        if(selected_day==day && selected_month==month && selected_year==year){
                            console.log(data.list[f]);
                            description = data.list[f].weather[0].description;
                            clouds = (data.list[f].temp.min+data.list[f].temp.min)/2 +' F';
                            wind_speed = data.list[f].speed + ' ml/h';
                            humidity = data.list[f].humidity + '%';
                            $(".desc_first").text(description);
                            $(".fer_first").text(clouds);
                            $(".wind_first").text(wind_speed);
                            $(".hum_first").text(humidity);
                            flag = true;
                            break
                        }
                    }
                    if(flag == false){
                        $(".desc_first").text('Weather Forecast Not available at this day');
                        $(".fer_first").text('');
                            $(".wind_first").text('');
                            $(".hum_first").text('');
                    }
                });
            }
            else{
                $(".desc_first").text('');
                $(".fer_first").text('');
                $(".wind_first").text('');
                $(".hum_first").text('');
            }
            if($("#cmn2").val() != ""){
                lat = $("#latitude_last").val();
                lng = $("#longitude_last").val();
                selected_date = new Date(Date.parse($("#datepicker").val()));
                selected_day = selected_date.getDate();
                selected_month = selected_date.getMonth();
                selected_year = selected_date.getFullYear();
                weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+lat+"&lon="+lng+"&cnt=16&units=imperial";

                $.get(weather_url, function(data, status){
                    flag = false;
                    for(f=0;f<data.list.length;++f){
                        var date = new Date(data.list[f].dt * 1000);
                        var day = date.getDate();
                        var month = date.getMonth();
                        var year = date.getFullYear();
                        if(selected_day==day && selected_month==month && selected_year==year){
                            console.log(data.list[f]);
                            description = data.list[f].weather[0].description;
                            clouds = (data.list[f].temp.min+data.list[f].temp.min)/2 +' F';
                            wind_speed = data.list[f].speed + ' ml/h';
                            humidity = data.list[f].humidity + '%';
                            $(".desc_last").text(description);
                            $(".fer_last").text(clouds);
                            $(".wind_last").text(wind_speed);
                            $(".hum_last").text(humidity);
                            flag = true;
                            break
                        }
                    }
                    if(flag == false){
                        $(".desc_last").text('Weather Forecast Not available at this day');
                        $(".fer_last").text('');
                            $(".wind_last").text('');
                            $(".hum_last").text('');
                    }
                });
            }
            else{
                $(".desc_last").text('');
                $(".fer_last").text('');
                $(".wind_last").text('');
                $(".hum_last").text('');
            }

            way_point_weathers(0);
        }
    });

    // Multiple Location add Script
    $('.add_more_waypoint').on('click', function(){
        // Getting last waypoint no
        last_waypoint_no = parseInt($('.total_waypoint').val()) + 1;
        var waypoint_id = last_waypoint_no + 2;
        console.log("Adding waypoint value-->"+last_waypoint_no);
        var myhtml= "<li class='title loc way_loc_"+last_waypoint_no+"'><input class='controls form-control pac-input address_common' type='text' " +
                "placeholder='Stop "+ last_waypoint_no+"' id='cmn"+waypoint_id+"' name='search_address"+ last_waypoint_no+"' required='true'" +
                 "style='display: initial; width: 267px;'> <a id='"+last_waypoint_no+"' class='delete_waypoint'><i class='glyphicon glyphicon-remove' style='color: #CD3C58;'></i></a> " +
                "<span class='errors' id='error_title"+waypoint_id+"' style='display:none; color: red; font-size: 13px;'>This Location is invalid</span>" +
                "<input TYPE='hidden' id='address"+waypoint_id+"' class='controls form-control near_address_common address"+last_waypoint_no+"' type='text' " +
                "placeholder='Waypoint "+last_waypoint_no+" Nearest address' name='near_address"+ last_waypoint_no+"'>" +
                "<input class='form-control note_common location_note_"+last_waypoint_no+"' " +
                "placeholder='Note (optional)' name='note_waypoint"+ last_waypoint_no+"'/ >" +
                "<p class='weather_"+last_waypoint_no+"'><b style='color: blue; font-size: 15px'>Weather:</b>" +
                "<b class='descs desc_"+last_waypoint_no+"' style='font-size: 15px;'></b>" +
                "<p class='fers fer_"+last_waypoint_no+"' style='margin-left: 63px; font-weight: 700; font-size: 15px'></p>" +
                "<br><p style='font-size: 12px'>Wind: <b class='winds wind_"+last_waypoint_no+"'></b> Humidity: " +
                "<b class='hums hum_"+last_waypoint_no+"'></b></p></p>" +
                "<input TYPE='hidden' name='latitude"+last_waypoint_no+"' id='latitude"+last_waypoint_no+"' class='lat_common latitude"+last_waypoint_no+" form-control' value />" +
                "<input TYPE='hidden' name='longitude"+last_waypoint_no+"' id='longitude"+last_waypoint_no+"' class='lng_common longitude"+last_waypoint_no+" form-control' value />" +
                "<input type='hidden' name='marker_status"+last_waypoint_no+"' class='form-control info' id='info'/>" +
                "<input type='hidden' name='my_waypoint_no' class='my_waypoint_no' value='"+last_waypoint_no+"'></input>" +
                "<div class='stop_calc'><input type='text' readonly='true' name='stop_distance' class='map-input stop_distance' " +
                "placeholder='Stop Distance' style='font-weight: bold; color: blue;'/><input type='text' readonly='true' " +
                "name='stop_hours' class='map-input stop_hours' placeholder='Stop Hours' style='font-weight: bold; color: blue;'/> " +
                "</div></li>";
        // appending new waypoint html
        if(last_waypoint_no == 1){
            $('.add_waypoint_container').after(myhtml);
        }
        else{
            var current_way_loc = '.way_loc_'+parseInt(last_waypoint_no-1);
            $(current_way_loc).after(myhtml);
        }

        var newInput = [];
        var newEl = $('.pac-input')[last_waypoint_no];
        newInput.push(newEl);
        setupAutocomplete(autocomplete, newInput, 0, last_waypoint_no);
        $('.total_waypoint').val(last_waypoint_no);
    });

});

function update_way_addressfun(latlng_data, way_no){
    $('#latitude'+way_no).val(latlng_data.lat());
    $('#longitude'+way_no).val(latlng_data.lng());

    if($("#datepicker").val() != ""){
        selected_date = new Date(Date.parse($("#datepicker").val()));
        selected_day = selected_date.getDate();
        selected_month = selected_date.getMonth();
        selected_year = selected_date.getFullYear();
        weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+latlng_data.lat()+"&lon="+latlng_data.lng()+"&cnt=16&units=imperial";

        $.get(weather_url, function(data, status){
            flag = false;
            console.log(data);
            for(f=0;f<data.list.length;++f){
                var date = new Date(data.list[f].dt * 1000);
                var day = date.getDate();
                var month = date.getMonth();
                var year = date.getFullYear();
                if(selected_day==day && selected_month==month && selected_year==year){
                    description = data.list[f].weather[0].description;
                    clouds = (data.list[f].temp.min+data.list[f].temp.min)/2 +' F';
                    wind_speed = data.list[f].speed + ' ml/h';
                    humidity = data.list[f].humidity + '%';
                    $(".desc_"+way_no+"").text(description);
                    $(".fer_"+way_no+"").text(clouds);
                    $(".wind_"+way_no+"").text(wind_speed);
                    $(".hum_"+way_no+"").text(humidity);
                    flag = true;
                    break
                }
            }
            if(flag == false){
                $(".desc_"+way_no+"").text('Weather Forecast Not available at this day');
                $(".fer_"+way_no+"").text('');
                    $(".wind_"+way_no+"").text('');
                    $(".hum_"+way_no+"").text('');
            }
        });
    }
    else{
        $(".desc_"+way_no+"").text('');
        $(".fer_"+way_no+"").text('');
        $(".wind_"+way_no+"").text('');
        $(".hum_"+way_no+"").text('');
    }

    geocoder.geocode({
        latLng: latlng_data
    }, function(responses) {
        if (responses && responses.length > 0) {
            current_location = responses[0].formatted_address;
            // waypoints.push(current_location);
            update_way_address(current_location, way_no)
        }
    });
}

function update_way_address(str, way_no) {
    console.log(str+"<>"+way_no);
    $('#address'+(way_no+2)).val(str);
}

function setupAutocomplete(autocomplete, inputs, i, last_waypoint_no) {
    console.log(autocomplete);
    autocomplete.push(new google.maps.places.Autocomplete(inputs[i], autocompleteOptions));
    var idx = autocomplete.length - 1;
    //autocomplete[i].bindTo('bounds', map);
    autocomplete[idx].bindTo('bounds', map);
    google.maps.event.addListener(autocomplete[idx], 'place_changed', function() {
        console.log(last_waypoint_no, "<--- Waypoint ");

        console.log(idx);
        var place_n = autocomplete[idx].getPlace();
        console.log(place_n);
        // This will return the nearest address and add as waypoint
        update_way_addressfun(place_n.geometry.location, last_waypoint_no);
        if($('#address1').val().length > 0 && $('#address2').val().length >0)
        {
            console.log("searchbox waypoint "+last_waypoint_no+"  make route");
            setTimeout(function() {
                calcRoute();
            }, 1000);
        }
    });
}

// drag make possible

var geocoder = new google.maps.Geocoder();

function geocodePosition(pos,box_no) {
    geocoder.geocode({
        latLng: pos
    }, function(responses) {
        if (responses && responses.length > 0) {
            if(box_no == '1'){
                updateMarkerAddress1(responses[0].formatted_address);
            }
            else{
                updateMarkerAddress2(responses[0].formatted_address);
            }

        } else {
            if(box_no == '1'){
                updateMarkerAddress1('Cannot determine address at this location.');
            }
            else{
                updateMarkerAddress2('Cannot determine address at this location.');
            }
        }
    });
}

function updateMarkerPosition(latLng) {
    var str =  latLng.lat() +" "+ latLng.lng();
    $('#info').val(str);
}

function updateMarkerAddress1(str) {
    $('#address1').val(str);
}

function updateMarkerAddress2(str) {
    $('#address2').val(str);
}

var directionsDisplay;
var startPos;
var current_location;
var directionsService = new google.maps.DirectionsService();
var rboxer = new RouteBoxer();
var distance = 20; // km
var trafficLayer = new google.maps.TrafficLayer();
var rendererOptions = {
// {#    polylineOptions: // {#}
// {#      strokeColor: "blue",#}
// {#      strokeOpacity: 0.5,#}
// {#      strokeWeight: 10#}
// {#    }#}
};

function initialize() {
    directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);

    var chicago = new google.maps.LatLng(41.850033, -87.6500523);
// {##}
// {#    map = new google.maps.Map(document.getElementById('map-canvas'), // {#}
// {#        mapTypeId: google.maps.MapTypeId.ROADMAP,#}
// {#        zoom: 6,#}
// {#        center: chicago#}
// {#    });#}
// {##}
// {#    directionsDisplay.setMap(map);#}

    var geoSuccess = function(position) {
        startPos = position;
        start_lat = startPos.coords.latitude;
        start_long = startPos.coords.longitude;
        current_location = new google.maps.LatLng(start_lat, start_long);
        map = new google.maps.Map(document.getElementById('map-canvas'), {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoom: 6,
            center: current_location
        });
        var marker = new google.maps.Marker({
            position: current_location,
            map: map
        });
        markers.push(marker);

        directionsDisplay.setMap(map);
// {#        trafficLayer.setMap(map);#}
        service = new google.maps.places.PlacesService(map);
        infowindow = new google.maps.InfoWindow();
    };
    var geoError = function(position){
        current_location = new google.maps.LatLng(41.850033, -87.6500523);
        map = new google.maps.Map(document.getElementById('map-canvas'), {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoom: 6,
            center: current_location
        });
        var marker = new google.maps.Marker({
            position: current_location,
            map: map
        });
        markers.push(marker);
        directionsDisplay.setMap(map);
// {#        trafficLayer.setMap(map);#}
    };

    navigator.geolocation.getCurrentPosition(geoSuccess, geoError);

    // search box defined here
    input_first = $('.pac-input')[0];
    input_last = $('.pac-input')[1];
    // map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    searchBox_first = new google.maps.places.SearchBox((input_first));
    searchBox_last = new google.maps.places.SearchBox((input_last));

    // search function start here
    google.maps.event.addListener(searchBox_first, 'places_changed', function() {
        console.log("searchbox first");
        var places = searchBox_first.getPlaces();
        if (places.length == 0) {
            return;
        }
        for (var i = 0, marker; marker = markers[i]; i++) {
            marker.setMap(null);
        }
        // For each place, get the icon, place name, and location.
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0, place; place = places[i]; i++) {
              // Create a marker for each place.
            marker = new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location
            });
            $("#latitude_first").val(place.geometry.location.lat());
            $("#longitude_first").val(place.geometry.location.lng());
            updateMarkerPosition(marker.getPosition());
            geocodePosition(marker.getPosition(),'1');

            if($("#datepicker").val() != ""){
                selected_date = new Date(Date.parse($("#datepicker").val()));
                selected_day = selected_date.getDate();
                selected_month = selected_date.getMonth();
                selected_year = selected_date.getFullYear();
                weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+place.geometry.location.lat()+"&lon="+place.geometry.location.lng()+"&cnt=16&units=imperial";


                $.get(weather_url, function(data, status){
                    flag = false;
                    for(f=0;f<data.list.length;++f){
                        var date = new Date(data.list[f].dt * 1000);
                        var day = date.getDate();
                        var month = date.getMonth();
                        var year = date.getFullYear();
                        if(selected_day==day && selected_month==month && selected_year==year){
                            description = data.list[f].weather[0].description;
                            clouds = (data.list[f].temp.min+data.list[f].temp.min)/2 +' F';
                            wind_speed = data.list[f].speed + ' ml/h';
                            humidity = data.list[f].humidity + '%';
                            $(".desc_first").text(description);
                            $(".fer_first").text(clouds);
                            $(".wind_first").text(wind_speed);
                            $(".hum_first").text(humidity);
                            flag = true;
                            break
                        }
                    }
                    if(flag == false){
                        $(".desc_first").text('Weather Forecast Not available at this day');
                        $(".fer_first").text('');
                        $(".wind_first").text('');
                        $(".hum_first").text('');
                    }
                });
            }
            else{
                $(".desc_first").text('');
                $(".fer_first").text('');
                $(".wind_first").text('');
                $(".hum_first").text('');
            }

            google.maps.event.addListener(marker, 'dragend', function() {
                geocodePosition(marker.getPosition(),'1');
                $("#latitude_first").val(marker.getPosition().lat());
                $("#longitude_first").val(marker.getPosition().lat());
            });
            markers.push(marker);
            bounds.extend(place.geometry.location);
        }

        if($('#address2').val().length > 0 && $('#address2').val() != 'undefined')
        {
            console.log("searchbox last make route");
            setTimeout(function() {
                calcRoute();
            }, 1000);
        }
        else{
            map.fitBounds(bounds);
            map.setZoom(9);
        }
    });

    // End Place Search Box
    google.maps.event.addListener(searchBox_last, 'places_changed', function() {
        console.log("searchbox last");
        var places1 = searchBox_last.getPlaces();
        if (places1.length == 0) {
            return;
        }
        for (var i = 0, marker; marker = markers[i]; i++) {
            marker.setMap(null);
        }
        // For each place, get the icon, place name, and location.
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0, place; place = places1[i]; i++) {
        // Create a marker for each place.
            marker = new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location,
            });
            $("#latitude_last").val(place.geometry.location.lat());
            $("#longitude_last").val(place.geometry.location.lng());
            updateMarkerPosition(marker.getPosition());
            geocodePosition(marker.getPosition(),'2');

            if($("#datepicker").val() != ""){
                selected_date = new Date(Date.parse($("#datepicker").val()));
                selected_day = selected_date.getDate();
                selected_month = selected_date.getMonth();
                selected_year = selected_date.getFullYear();
                weather_url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+place.geometry.location.lat()+"&lon="+place.geometry.location.lng()+"&cnt=16&units=imperial";

                $.get(weather_url, function(data, status){
                    flag = false;
                    for(f=0;f<data.list.length;++f){
                        var date = new Date(data.list[f].dt * 1000);
                        var day = date.getDate();
                        var month = date.getMonth();
                        var year = date.getFullYear();
                        if(selected_day==day && selected_month==month && selected_year==year){
                            description = data.list[f].weather[0].description;
                            clouds = (data.list[f].temp.min+data.list[f].temp.min)/2 +' F';
                            wind_speed = data.list[f].speed + ' ml/h';
                            humidity = data.list[f].humidity + '%';
                            $(".desc_last").text(description);
                            $(".fer_last").text(clouds);
                            $(".wind_last").text(wind_speed);
                            $(".hum_last").text(humidity);
                            flag = true;
                            break
                        }
                    }
                    if(flag == false){
                        $(".desc_last").text('Weather Forecast Not available at this day');
                        $(".fer_last").text('');
                            $(".wind_last").text('');
                            $(".hum_last").text('');
                    }
                });
            }
            else{
                $(".desc_last").text('');
                $(".fer_last").text('');
                $(".wind_last").text('');
                $(".hum_last").text('');
            }

            google.maps.event.addListener(marker, 'dragend', function() {
                geocodePosition(marker.getPosition(),'2');
                $("#latitude_last").val(marker.getPosition().lat());
                $("#longitude_last").val(marker.getPosition().lat());
            });
            markers.push(marker);
            bounds.extend(place.geometry.location);
        }

        if($('#address1').val().length > 0 && $('#address1').val() != 'undefined')
        {
            console.log("searchbox last make route");
            setTimeout(function() {
                calcRoute();
            }, 500);
        }
        else{
            map.fitBounds(bounds);
            map.setZoom(9);
        }
    });

}

var route;

//initial function close here

// calculate route function
function calcRoute() {
    $('.optimized_view').empty();
    for (var i = 0, marker; marker = markers[i]; i++) {
        marker.setMap(null);
    }
    console.log("yes it is entering on calcroute");
    var start = $('#address1').val();
    var end = $('#address2').val();

    console.log(start);
    console.log(end);

    var way_points_arr = [];
    total_waypoints_temp = parseInt($('.total_waypoint').val()) +2;
    for(var p=3; p<=total_waypoints_temp;p++){
        if($('#address'+p).val() != ''){
            way_points_arr.push({
            location:$('#address'+p).val(),
            stopover:true});
        }
    }
    console.log(way_points_arr);

    var request = {
        origin: start,
        destination: end,
        waypoints: way_points_arr,
        travelMode: google.maps.TravelMode.DRIVING,
        unitSystem: google.maps.UnitSystem.IMPERIAL
    };

    var request2 = {
        origin: start,
        destination: end,
        waypoints: way_points_arr,
        optimizeWaypoints: true,
        travelMode: google.maps.TravelMode.DRIVING,
        unitSystem: google.maps.UnitSystem.IMPERIAL
    };

    String.prototype.toHHMMSS = function () {
        var sec_num = parseInt(this, 10);
        var hours   = Math.floor(sec_num / 3600);
        var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
        var seconds = sec_num - (hours * 3600) - (minutes * 60);

        if (hours   < 10) {hours   = "0"+hours;}
        if (minutes < 10) {minutes = "0"+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}
        return hours+' hrs '+minutes+' mins';
    };

    directionsService.route(request2, function(response2, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            console.log(response2);
            var optimized_routes = response2.routes[0].legs;
            var optimized_waypoints_order = response2.routes[0].waypoint_order;
            console.log(optimized_routes);
            var total_distance_opt = 0;
            var total_duration_opt = 0;
            for (var o = 0; o < optimized_routes.length; o++) {
                total_distance_opt += parseInt(optimized_routes[o].distance.text.substr(0,optimized_routes[o].distance.text.length-3).replace(',',''));
                total_duration_opt += optimized_routes[o].duration.value;
            }
// {#            total_distance_opt = (total_distance_opt / 1000.0).toFixed();#}
            var total_distance_opt_int = total_distance_opt.toString() + ' miles';
            var total_duration_opt_format = total_duration_opt.toString().toHHMMSS();
            for(var e=0;e<optimized_waypoints_order.length;++e){
                console.log(optimized_waypoints_order[e]);
                $('.optimized_view').append("<input TYPE='hidden' name='order"+e+"' value='"+optimized_waypoints_order[e]+"'>");

            }
            $('.optimized_view').append("<input type='text' name='opt_distance' value='"+total_distance_opt_int+"'/>" +
            "<input type='text' name='opt_hours' value='"+total_duration_opt_format+"'/>");
        }
    });

    directionsService.route(request, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {

            setAllMap(null, hotel_markers);
            setAllMap(null, food_markers);
            setAllMap(null, gas_markers);

            $('.show_gas').text('Find GasStations');
            $('.show_food').text('Find Food');
            $('.show_hotels').text('Find Hotels');

            hotel_status = false;
            gas_status = false;
            food_status = false;

            directionsDisplay.setDirections(response);
            route = response.routes[0];
            console.log(route);

            $('.route_extra').show();

            var total_distance_int = 0;
            var total_duration = 0;
            for (var i = 0; i < route.legs.length; i++) {

                total_distance_int += parseInt(route.legs[i].distance.text.substr(0,route.legs[i].distance.text.length-3).replace(',',''));
                total_duration+= route.legs[i].duration.value;
            }

            $('.stop_distance').each(function(i, obj) {
                $(this).val(route.legs[i].distance.text.substr(0,route.legs[i].distance.text.length-3).toString() + ' miles');
            });
            $('.stop_hours').each(function(i, obj) {
                $(this).val(route.legs[i].duration.value.toString().toHHMMSS());
            });
// {#            total_distance_int = (total_distance_int / 1000.0).toFixed();#}

            var total_distance = total_distance_int.toString() + ' miles';
            var total_duration_in_format = total_duration.toString().toHHMMSS();
            $('.total_distance').val(total_distance);
            $('.total_hours').val(total_duration_in_format);
        }
    });
}

google.maps.event.addDomListener(window, 'load', initialize);


