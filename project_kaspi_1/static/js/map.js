/*ymaps.ready(init);

var myMap, myPlacemark;

function init(){ 
    myMap = new ymaps.Map("map", {
        center: [43.237259, 76.915419],
        zoom: 13
    }); 

    jQuery.getJSON('/venues', function (json) {
           
            var geoObjects = ym.geoQuery(json)
                    .addToMap(myMap)
                    .applyBoundsToMap(myMap, {
                        checkZoomRange: true
                    });
        });
}
*/

ymaps.ready()
    .done(function (ym) {
        var myMap = new ym.Map('map', {
            center: [43.237259, 76.915419],
            zoom: 13,
            controls:['largeMapDefaultSet'],
        });

        myMap.controls.remove('geolocationControl');
        myMap.controls.remove('searchControl');
        myMap.controls.remove('routeEditor');
        myMap.controls.remove('trafficControl');
        myMap.controls.remove('typeSelector');
        myMap.controls.remove('zoomControl');

        var zoomControl = new ymaps.control.ZoomControl({
            options: {
                size: "large",
                position: {
                    left: 'auto',
                    right: 10,
                    top: 100
                }
            }
        });
        myMap.controls.add(zoomControl);
        


        jQuery.getJSON('/venues', function (json) {
            var geoObjects = ym.geoQuery(json.data)
                    .addToMap(myMap)
                    .applyBoundsToMap(myMap, {
                        checkZoomRange: true
                    });
        });
    });