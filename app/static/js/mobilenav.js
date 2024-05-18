button = document.getElementById("hamburger")
navMenu = document.getElementById("mobile")

button.addEventListener("click", () =>{
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


