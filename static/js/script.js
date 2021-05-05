$(document).ready(function () {
    $('.sidenav').sidenav({ edge: "right" });
    $('.collapsible').collapsible();
    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
  });
//   https://codepen.io/Paco_Cervantes/pen/ZLxKpj
  // start carrousel
   $('.carousel.carousel-slider').carousel({
      fullWidth: true,
      indicators: false
   });


   // move next carousel
   $('.moveNextCarousel').click(function(e){
      e.preventDefault();
      e.stopPropagation();
      $('.carousel').carousel('next');
   });

   // move prev carousel
   $('.movePrevCarousel').click(function(e){
      e.preventDefault();
      e.stopPropagation();
      $('.carousel').carousel('prev');
   });

});
// https://www.w3schools.com/js/tryit.asp?filename=tryjs_alert
   function commentLogin() {
        alert("Please login or register to post a comment");
}
// https://stackoverflow.com/questions/63033012/copy-the-text-to-the-clipboard-without-using-any-input
function shareQuote(quote_id) {
  var TempText = document.createElement("input");
  TempText.value = "http://ms3-quotes.herokuapp.com/share_quote/" + quote_id;
  document.body.appendChild(TempText);
  TempText.select();
  
  document.execCommand("copy");
  document.body.removeChild(TempText);
  
  alert("Copied sharable link to clipboard: " + TempText.value);
}

// $(.mood-button).change(function(e) {
//     if ($(this).is(':not(:checked)')) {
//             $(this).addClass( "input[type=checkbox] + label" );}

    // Moved to quotes.html
// $('input[name=test_quote_star]').change(function(e) {
//   if ($(this).is(':checked')) {
//         console.log("JS Post");
//         $.ajax({
//             url:"/add_fav_quote",
//             type: "POST",        // type or method?
//             // data: "Hi",
//             success: function(response) { 
//                 console.log("AJAX Post") 
//       }, 
//       error: function(request, status, error) { 
//                 console.log("Error: " + error) 
//       } 
//     }
//     );
// }
// e.preventDefault();
// });

