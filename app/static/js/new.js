// new stuffs
infoButtons(document.getElementById("gicLabelBtn"), document.getElementById("gicInfoLabel"));
infoButtons(document.getElementById("sharedCareLabelBtn"), document.getElementById("sharedCareInfoLabel"));
infoButtons(document.getElementById("bridgingDesiredLabelBtn"), document.getElementById("bridgingDesiredInfoLabel"));
infoButtons(document.getElementById("under16LabelBtn"), document.getElementById("under16InfoLabel"));
infoButtons(document.getElementById("fixedAddressLabelBtn"), document.getElementById("fixedAddressInfoLabel"));
infoButtons(document.getElementById("noIdProofLabelBtn"), document.getElementById("noIdProofInfoLabel"));

// expand additional info on clicking ?
function infoButtons(btn, btnLabel){
    btn.addEventListener("click", () => {
        const currentState = btn.getAttribute("data-state");
        if (!currentState || currentState === "closed") {
            btn.setAttribute("data-state", "opened");
            btn.setAttribute("aria-expanded", "true");
    
            btnLabel.setAttribute("aria-expanded", "true");
        } else {
            btn.setAttribute("data-state", "closed");
            btn.setAttribute("aria-expanded", "false");
    
            btnLabel.setAttribute("aria-expanded", "false");
        }
    });
};