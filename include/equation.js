<script>
function css( element, property ) {
    return window.getComputedStyle( element, null ).getPropertyValue( property );
}

function shiftImg(){
	var images = document.querySelectorAll("div.equation_css img");

	//Iterates through each of the images
	for (var i = 0; i < images.length; i++) {
	    //Sets the images top margin to the half of the height of the image
		var offset = - images[i].height / 2;
		var offset2 = Number(css(images[i].parentNode, "font-size").replace(/[^\d\.\-]/g, ''));
		offset = offset - offset2 / 2;
	    images[i].style.marginTop = offset.toString().concat("px");
	    images[i].parentNode.style.marginBottom = (offset + offset2).toString().concat("px");; 
	    images[i].parentNode.style.marginTop = (-offset).toString().concat("px");
	}
}
if(window.addEventListener){
    window.addEventListener('load',shiftImg,false); //W3C
}
else{
    window.attachEvent('onload',shiftImg); //IE
}
</script>