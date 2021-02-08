(function() {
// var str = $( "#description" ).first().text();
// str = str.replace(/(?:\r\n|\r|\n)/g, '<br>');
// $( "#description" ).first().html(str);
$(document).ready(function(){
  $("#search").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#packages a").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});
}).call(this);
