$( document ).ready(function() {
  
  $("#form").submit( function(e) {
    console.log("Called");
    console.log(e);
    e.preventDefault(); 
    get_restaurants($("#post_code").val());

  }); 



update_map = function (response)
{
  restaurants = response.Restaurants
  map.setCenter(restaurants[0].Latitude, restaurants[0].Longitude);
  map.setZoom(12);
  for(var i = 0; i < restaurants.length; i++)
  {
    if(restaurants[i].hasOwnProperty("Latitude"))
    {
      map.addMarker({
        lat: restaurants[i].Latitude,
        lng: restaurants[i].Longitude,
        title: restaurants[i].Name,
        infoWindow: {
          content: '<p>' + restaurants[i].Name + '</p>'
        }
      });
    }
  }
}

compare = function (a,b)
{
  if (a.value < b.value)
     return -1;
  if (a.value > b.value)
    return 1;
  return 0;
}

update_chart1 = function (response)
{
  chart = $("#chart1");
  restaurants = response.Restaurants;
  data = new Array();

  for(var i = 0; i < restaurants.length; i++)
  {
    for(var y = 0; y < restaurants[i].CuisineTypes.length; y++)
    {
      if (data.length != 0)
      {
        var found = false;
        for(var z = 0; z < data.length; z++)
        {
          if(data[z].category == restaurants[i].CuisineTypes[y].Name)
          {
            data[z].value = data[z].value + 1;
            found = true
          } 
        }
        if(!found)
        {
          entry = new Object();
          entry.category = restaurants[i].CuisineTypes[y].Name;
          entry.value = 1;
          data.push(entry);
        }
      }
      else
      {
        console.log("Adding first element");
        entry = new Object();
        entry.category = restaurants[i].CuisineTypes[y].Name;
        entry.value = 1;
        data.push(entry);
      }
    } 
  }

  data.sort(compare);

  chart.dxPieChart({
    dataSource: data,
    series: {
      argumentField: "category",
      valueField: "value",
      label: {
        visible: true,
      }
   },
   title: {
      text: "Cuisine Distribution"
    },
    tooltip: {
        enabled: true,
        percentPrecision: 2,
        customizeText: function (value) {
            return value.percentText;
        }
    }
  });
}

get_restaurants = function (post_code) 
{
  $.ajax({
    url: "http://api-interview.just-eat.com/restaurants?q=" + post_code,
    type: "GET",
    crossDomain: true,
    beforeSend: function(xhr) { 
      xhr.setRequestHeader("Accept-Tenant", "UK");
      xhr.setRequestHeader("Authorization", "Basic a2luZ3MtaGFjazpqNHlrN3ljb3Q1MHRmMng=");
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.setRequestHeader("Accept-Version", "2");
      $("#spinner").show();
    },
    success: function(response) 
    {
      console.log(response);
      update_map(response);
      update_chart1(response);
      $.smoothScroll(800);
      $("#spinner").hide();
    },
    error: function(response) 
    {
      $("#spinner").hide();
      console.log(response);
    }
  });
}
