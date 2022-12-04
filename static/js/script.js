$(document).ready(function () {
	// Mobile Navbar
	// Source: https://materializecss.com/navbar.html
	$(".sidenav").sidenav({ edge: "right" });
	$(".collapsible").collapsible();
	//  Mood Board carousel
	//  Acknowledge: https://materializecss.com/carousel.html#two!
	//  Acknowledge: https://codepen.io/Paco_Cervantes/pen/ZLxKpj
	$(".carousel.carousel-slider").carousel({
		fullWidth: true,
		indicators: true,
	});
	// start carrousel
	$(".carousel.carousel-slider").carousel({
		fullWidth: true,
		indicators: false,
	});
	// move next carousel
	$(".moveNextCarousel").click(function (e) {
		e.preventDefault();
		e.stopPropagation();
		$(".carousel").carousel("next");
	});
	// move prev carousel
	$(".movePrevCarousel").click(function (e) {
		e.preventDefault();
		e.stopPropagation();
		$(".carousel").carousel("prev");
	});
});
// Comment login prompt
// Acknowledge: https://www.w3schools.com/js/tryit.asp?filename=tryjs_alert
function commentLogin() {
	alert("Please login or register to post a comment");
}
// Prompt on enter key in textbox
$("#comment").keyup(function (event) {
	if (event.keyCode === 13) {
		$("#post-button").click();
	}
});
// Funciton to copy quote info to clipboard
// Acknowledge: https://stackoverflow.com/questions/63033012/copy-the-text-to-the-clipboard-without-using-any-input
// Acknowledge: https://www.w3schools.com/howto/howto_js_copy_clipboard.asp
function shareQuote(link_id) {
	var TempText = document.createElement("input");
	// Extract quote id
	quote_id = link_id.split("-")[1];
	// formulate link
	TempText.value =
		"https://web-production-aaee.up.railway.app/share_quote/" + quote_id;
	document.body.appendChild(TempText);
	TempText.select();
	// copy
	document.execCommand("copy");
	document.body.removeChild(TempText);
	// Prompt user
	alert("Copied sharable link to clipboard: " + TempText.value);
}
