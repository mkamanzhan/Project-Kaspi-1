ymaps.ready()
    .done(function (ym) {
        var myMap = new ym.Map('map', {
            center: [43.237259, 76.915419],
            zoom: 13,
            controls:[],
        });

     

        var zoomControl = new ymaps.control.ZoomControl({
            options: {
                size: "large",
                position: {
                    left: 'auto',
                    right: 10,
                    top: 10,
                }
            }
        });
        myMap.controls.add(zoomControl);


        var selected = -1;
        var geoObjects;

        $('#my-block').show();



        $("#my-search input").keyup(function(e){
            if($(this).val().length >= 3){   

                $('.my-hidden').show();

                if(e.which == 13 && geoObjects.getLength() != 0) {

                    $(".item").removeClass('selected');
                    $(".item:first-child").addClass('selected');

                    var id = 0;
                    selected = 0;
                    point = geoObjects.get(id);
                    myMap.geoObjects.get(id).options.set('preset', 'islands#redDotIconWithCaption');
                    $("#my-list-items").scrollTop(0);
                    $("#my-list-items").animate({scrollTop: $(".item:nth-child(" + (id+1) + ")").position().top - $("#my-list-items").offset().top}, 200);
                    myMap.setCenter(point.geometry._coordinates, 17,{duration: 1000});

                    $("#my-detail-item").html("<img class='icon' src='" + point.properties.get("icon_url") + "'>" + point.properties.get("name") + "<br>" + point.properties.get("category") + "<br>" + point.properties.get("address"));
                    var tip_list_html = "";
                    point.properties.get('tips').forEach(function(tip, i){

                        tip_list_html += "<div class='item' id='"+i+"'>" + tip +"</div>"
                    });
                    $("#my-list-tips").html(tip_list_html);
                    $("#my-tips-count").html(point.properties.get('tips').length);
                    $('#my-detail').show();

                } else {

                    $('#my-detail').hide();
                    $("#my-list-items").html("<img id='my-loading' src='/static/img/loading.gif'>"); 

                    jQuery.getJSON('/search/', {'text': $(this).val()}, function (json) {
                        myMap.geoObjects.removeAll();
                        selected = -1
                        geoObjects = ym.geoQuery(json.data);

                        if(geoObjects.getLength() != 0){
                            var venue_list_html = ''


                            geoObjects.each(function(item, i){

                                item.events.add('mouseenter', function (e) {
                                    if(i != selected){
                                        e.get('target').options.set('preset', 'islands#yellowDotIconWithCaption');
                                        $(".item:nth-child(" + (i+1) + ")").addClass('hover');
                                    }
                                    
                                    $("#my-list-items").scrollTop(0);
                                    $("#my-list-items").animate({scrollTop: $(".item:nth-child(" + (i+1) + ")").position().top - $("#my-list-items").offset().top}, 200);
                                    
                                }).add('mouseleave', function (e) {
                                    if(i != selected){   
                                        e.get('target').options.set('preset', 'islands#blueIcon');
                                        $(".item").removeClass('hover');
                                    }
                                });

                                item.properties.set('balloonContent', item.properties.get("name") + "<br>" + item.properties.get("category") + "<br>" + item.properties.get("address"));
                                item.properties.set('iconCaption', item.properties.get("name"));
                                venue_list_html += "<div class='item' id='"+i+"'><img class='icon' src='" + item.properties.get("icon_url") + "'>" + item.properties.get("name") + "<br>" + item.properties.get("category") + "<br>" + item.properties.get("address") + "</div>";
                            });


                            $("#my-list-items").html(venue_list_html);

                            geoObjects.addToMap(myMap);


                            $(".item").click(function(){
                                if(selected != -1){
                                    myMap.geoObjects.get(selected).options.set('preset', 'islands#blueIcon');
                                    $(".item").removeClass('selected');
                                }
                                $(this).addClass('selected');
                                var id = $(this).attr('id');
                                selected = id;
                                point = geoObjects.get(id);
                                myMap.geoObjects.get(id).options.set('preset', 'islands#redDotIconWithCaption');
                                myMap.setCenter(point.geometry._coordinates, 17,{duration: 1000});

                                $("#my-detail-item").html("<img class='icon' src='" + point.properties.get("icon_url") + "'>" + point.properties.get("name") + "<br>" + point.properties.get("category") + "<br>" + point.properties.get("address"));
                                var tip_list_html = "";
                                point.properties.get('tips').forEach(function(tip, i){
                                    tip_list_html += "<div class='item' id='"+i+"'>" + tip +"</div>"
                                });

                                $("#my-list-tips").html(tip_list_html);
                                $("#my-tips-count").html(point.properties.get('tips').length);
                                $('#my-detail').show();
                            });  

                            $(".item").hover(function(){
                                var id = $(this).attr('id');
                                if(id != selected){
                                    myMap.geoObjects.get(id).options.set('preset', 'islands#yellowDotIconWithCaption');
                                    myMap.geoObjects.get(id).options.set('zIndex', 700);
                                }
                            },function(){
                                var id = $(this).attr('id');
                                if(id != selected){
                                    myMap.geoObjects.get(id).options.set('preset', 'islands#blueIcon');     
                                    myMap.geoObjects.get(id).options.set('zIndex', 650);
                                }
                            });


                        } else {
                            $("#my-list-items").html("<h4>По вашему запросу ничего не найдено</h4>");
                        }

                        $("#my-count").html(geoObjects.getLength());
                    }).fail(function(){
                        $("#my-list-items").html("<h4>Проблемы с соединением</h4>"); 
                    });     
                }
            } else {
                myMap.geoObjects.removeAll();
                $('.my-hidden').hide();
                $('#my-detail').hide();
            }
        });

        $("#my-search-button").click(function(){
            if(geoObjects.getLength() != 0) {
                    if(selected != -1){
                        myMap.geoObjects.get(selected).options.set('preset', 'islands#blueIcon');
                        $(".item").removeClass('selected');
                    }
                    $(".item:first-child").addClass('selected');
                    var id = 0;
                    selected = 0;
                    point = geoObjects.get(id);
                    myMap.geoObjects.get(id).options.set('preset', 'islands#redDotIconWithCaption');
                    $("#my-list-items").scrollTop(0);
                    $("#my-list-items").animate({scrollTop: $(".item:nth-child(" + (id+1) + ")").position().top - $("#my-list-items").offset().top}, 200);
                    myMap.setCenter(point.geometry._coordinates, 17,{duration: 1000});

                    $("#my-detail-item").html("<img class='icon' src='" + point.properties.get("icon_url") + "'>" + point.properties.get("name") + "<br>" + point.properties.get("category") + "<br>" + point.properties.get("address"));
                    var tip_list_html = "";
                    point.properties.get('tips').forEach(function(tip, i){

                        tip_list_html += "<div class='item' id='"+i+"'>" + tip +"</div>"
                    });
                    $("#my-list-tips").html(tip_list_html);
                    $("#my-tips-count").html(point.properties.get('tips').length);
                    $('#my-detail').show();
            }
        });

        $("#my-clear").click(function(){
            $("#my-search input").val('');
            $("#my-search input").keyup();
        });

        $("#my-close").click(function(){
            $('#my-detail').hide();
        });
    });