window.addEventListener("load", function(){
	console.log("onload");
	document.querySelector('#ifrm').addEventListener("load", function() {

		console.log("test");
		var x = document.getElementById("price_table").rows[0].cells.length;
		console.log( x);
	}, true);
});


function myFunc() {
	var iframe = document.getElementById('ifrm');
var innerDoc = (iframe.contentDocument)
               ? iframe.contentDocument
               : iframe.contentWindow.document;

var ulObj = innerDoc.getElementById("ID_TO_SEARCH");
	var x = document.getElementById('ifrm').contentWindow.document.getElementById('price_table');//.rows[0].cells.length;
		console.log( x);
		console.log( ulObj);

}

let myVar = setInterval(myFunc, 1500);