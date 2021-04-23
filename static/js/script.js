$(document).ready(function () {
    $('.sidenav').sidenav({ edge: "right" });
    $('.collapsible').collapsible();
    
});

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

