//This will be the client side JS script for contacting /calc
 function get(name){
 if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
    return decodeURIComponent(name[1]);
}

function dispErr(){
  $("#stile").html("Error 4200");
  $("#sinfo").html("<img src='css/tuna.png' class='img-responsive' align='left'> Sorry! It looks like we can't catch any tuna right now; you may have an invalid song address. Please try again later. ");
}

var tunac = 0;

function tunainc(){
	tunac++;
	$("#tunaCount").html(tunac);
}
function getSong(){
	var loading = setInterval(tunainc, 50); 

	song = get('id');
	if(song != undefined){
	  $.getJSON( "api/song?id=" + song, function( data ) {
	    var items = [];
	    if(data["id"] == "error")
	      dispErr();
	    else{
	     $("#stile").html(data["title"] + "<small> by " + data["artist"]);
	     $("#sinfo").html("Hej! We gave this song a tuna score of  <button type ='button' class='btn btn-info'>"+data["scale"]+"</button><br/> For more info on how we caught "+ data["scale"] + " tuna, read <a href='/about'>our about page.</a>");
	     //$("#sinfo").attr("align", "left")
	     $("#social").html('Views <span class="badge">' + data["popularity"] + "</span>");
	  }
	  }).always(function() {clearInterval(loading);});
	}
	else{
	  dispErr();
	}

}
window.onload = getSong();