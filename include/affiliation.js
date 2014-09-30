<script>
function addAffiliation(){
	var address = document.querySelectorAll(".address li");
	var idLookup = new Array();
	for(var i=0; i < address.length; i++){
		idLookup[address[i].getAttribute("data-id")] = i+1;
	}
	var author = document.querySelectorAll(".author_name")
	for(var i=0; i < author.length; i++){
		var superscript = document.createElement("sup");
		var affil = author[i].getAttribute("data-affiliation").split(", ");
		var affilText = "";
		for(var j=0; j < affil.length; j++){
			superscript.textContent += idLookup[affil[j]];
			if(j < affil.length -1){
				superscript.textContent += ", ";
			}
		}
		author[i].appendChild(superscript)
	}
}
if(window.addEventListener){
    window.addEventListener('load',addAffiliation,false); //W3C
}
else{
    window.attachEvent('onload',addAffiliation); //IE
}
</script>