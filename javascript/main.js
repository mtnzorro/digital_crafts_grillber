$(document).ready(function() {

  $("a[href^='#']").on("click", function(e) {
        e.preventDefault();
        var hash = this.hash;
        $("html, body").animate({
            scrollTop: $(hash).offset().top
        }, 900, function() {
            window.location.hash = hash;
        });
    });

  $('.scroll').onePageNav({
      currentClass: 'current',
      changeHash: false,
      scrollSpeed: 750,
      scrollThreshold: 0.5,
      filter: '',
      easing: 'swing'
  });

});

var navWhite = document.getElementById("navbar");
window.onscroll = scroll;
function scroll() {
  if (window.pageYOffset >= 773) {
    navWhite.style.backgroundColor = "white";
  }
  else {
    navWhite.style.backgroundColor = "white";
  }
}


var bar = document.getElementById("fa-bars");
var navbars = document.getElementById("nav");
var navbarlinks = document.querySelectorAll(".navbar-link");
var body = document.querySelectorAll("body");
var clicked = false;

bar.addEventListener("click", function() {
  if (!clicked) {
    navbars.style.display = "block";
    clicked = true;
  } else {
      navbars.style.display = "";
      clicked = false;
  }
	// navbars.classList.toggle("hide");
});


if (window.innerWidth <  768) {
  for (var i = 0; i < navbarlinks.length; i++) {
    navbarlinks[i].addEventListener("click", function() {
      navbars.style.display = "none";
    });
  }
}
