$(function() {
  $("#id_tag").autocomplete({
    source: "/api/get_tags/",
    minLength: 2,
  });
});


$(function() {  
  $(".button").click(function() {  
$.ajax({
     type:"POST",
     url:"/api/add_tag/",
     data: {
            'test-data': 'test',
           
     },
     success: function(data){
         alert(data);
         $("body").append(data);
     }
});

  });  
});  