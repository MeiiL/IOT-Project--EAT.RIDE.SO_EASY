function initMap(){
    
    // HTML5 new feature: GPS
    var geo = window.navigator.geolocation;
    geo.getCurrentPosition(function(pos){    
        // Create a map object and specify the DOM element for display.
        // 參數1: 告訴她掛載在哪個區域下
        // 參數2: 字典: 把地圖有關的參數帶進去
        map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: pos.coords.latitude, lng: pos.coords.longitude},
            zoom: 15
        });
        here = {lat: pos.coords.latitude, lng: pos.coords.longitude};
        console.log(here);
        // 參數1: 字典: marker有關的資訊(1. marker的位置 2. marker要被放在哪張地圖)
        var marker = new google.maps.Marker({
            position: here,
            map: map
        });
    });
    
}

function performSearch() {
  var search_keyword = document.getElementById('search-food').value;
  var request = {
    location: here,
    radius: '1500',
    types: ['food'],
    name: search_keyword
  };

  service = new google.maps.places.PlacesService(map);
  service.nearbySearch(request, callback);
}

function callback(results, status) {
    console.log(results);

    if (status == google.maps.places.PlacesServiceStatus.OK) {
      for (var i = 0; i < results.length; i++) {
           var place = results[i];
           // 把google原本就放在result的icon拿出來
           var image = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
            };
            // 設定marker是跟以前一模一樣的, 只多帶了icon和title
            var marker = new google.maps.Marker({
                map: map,
                icon:image,
                position: place.geometry.location,
                title: place.name,
            });
      }
    }
}
