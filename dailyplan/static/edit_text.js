$("#{{ user['id'] }}").click(function(){
  $("p.{{ user['id'] }}").attr("contentEditable", "true");
});