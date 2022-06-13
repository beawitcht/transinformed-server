window.addEventListener('load', function() {
    document.getElementById('countries').addEventListener('change', checkRequired);
    document.getElementById('selfMedCheck').addEventListener('click', selfMedToggle);
    document.getElementById('likelyMedCheck').addEventListener('click', selfMedToggle);
});


function selfMedToggle() {
    var selfMed = document.getElementById("selfMedCheck");
    var selfMedLikely = document.getElementById("likelyMedCheck");
    var bridgingDesired = document.getElementById("bridgingDesired");
    if (selfMed.checked || selfMedLikely.checked) {
        bridgingDesired.disabled = false;
    } else {
        bridgingDesired.disabled = true;
        bridgingDesired.checked = false;
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