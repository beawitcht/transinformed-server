window.onscroll = function() {scrollDetected()};

button = document.getElementById("hamburger");
navMenu = document.getElementById("mobile");
backToTop = document.getElementById("backToTop");

button.addEventListener("click", () => {
  const currentState = button.getAttribute("data-state");
  if (!currentState || currentState === "closed") {
    button.setAttribute("data-state", "opened");
    button.setAttribute("aria-expanded", "true");

    navMenu.setAttribute("aria-expanded", "true");
  } else {
    button.setAttribute("data-state", "closed");
    button.setAttribute("aria-expanded", "false");

    navMenu.setAttribute("aria-expanded", "false");
  }
});

backToTop.addEventListener("click", () => {
  document.documentElement.scrollTo({top: 0, behavior: 'smooth'});
});

function scrollDetected() {
  if (document.body.scrollTop > 120 || document.documentElement.scrollTop > 120) {
    document.getElementById("backToTop").style.display = "block";
  } else {
    document.getElementById("backToTop").style.display = "none";
  }
}