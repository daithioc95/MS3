$(document).ready(function () {
    $('.sidenav').sidenav({ edge: "right" });
    $('.collapsible').collapsible();
    });

$('input[name=test_quote_star]').change(function() {
  if ($(this).is(':checked')) {
        console.log("JS Post")
        $.ajax({
            url:"/add_fav_quote",
            method: "GET",
            data: "Hello"
    }
    );
}
});
