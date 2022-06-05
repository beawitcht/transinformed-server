function selfMedToggle() {
    var selfMed = document.getElementById("selfMedCheck");
    var selfMedLikely = document.getElementById("likelyMedCheck");
    if (selfMed.checked || selfMedLikely.checked) {
        document.getElementById("bridgingDesired").disabled = false;
    } else {
        document.getElementById("bridgingDesired").disabled = true;
    }

    if (selfMed.checked) {
        selfMedLikely.disabled = true;
    }
    else if (selfMedLikely.checked) {
        selfMed.disabled = true;
    }
    else {
        selfMed.disabled = false;
        selfMedLikely.disabled = false;
    }
}

function checkRequired(){
    var countriesSelect = document.getElementById("countries");
    if (countriesSelect.value !== "Choose..."){
        document.getElementById("docx").disabled = false;
        document.getElementById("pdf").disabled = false;
    }
    else {
        document.getElementById("docx").disabled = true;
        document.getElementById("pdf").disabled = true;
    }
}

