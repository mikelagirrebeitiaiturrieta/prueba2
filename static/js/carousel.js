$(".flipper").click(function() {
    var target = $( event.target );
    if ( target.is("a") ) {
      //follow that link
      return true;
    } else {
      $(this).toggleClass("flip");
    }
    return false;
  });