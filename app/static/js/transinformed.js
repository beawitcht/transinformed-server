window.addEventListener('load', function () {
    // Countries dropdown
    document.getElementById('countries').addEventListener('change', checkRequired);
    // Medication Status
    document.getElementById('selfMedCheck').addEventListener('click', checkboxStatus);
    document.getElementById('likelyMedCheck').addEventListener('click', checkboxStatus);
    document.getElementById('noMedCheck').addEventListener('click', checkboxStatus);
    // Documents Held
    document.getElementById('diagnosisCheck').addEventListener('click', checkboxStatus);
    document.getElementById('hrtCheck').addEventListener('click', checkboxStatus);
    document.getElementById('noDocCheck').addEventListener('click', checkboxStatus);

    document.getElementById('asyncLoad').setAttribute('media', 'all');
});


function checkboxStatus() {
    // set check boxes
    var selfMed = document.getElementById("selfMedCheck");
    var selfMedLikely = document.getElementById("likelyMedCheck");
    var bridgingDesired = document.getElementById("bridgingDesired");
    var noMed = document.getElementById("noMedCheck");
    var diagnosis = document.getElementById("diagnosisCheck");
    var hrt = document.getElementById("hrtCheck");
    var noDoc = document.getElementById("noDocCheck");

    // conditions for Documents held
    (diagnosis.checked || hrt.checked) ? (noDoc.disabled = true) : (noDoc.disabled = false);
    noDoc.checked ? (diagnosis.disabled = true, hrt.disabled = true) : (diagnosis.disabled = false, hrt.disabled = false);

    // conditions for bridging
    (selfMed.checked || selfMedLikely.checked) && !hrt.checked ? (bridgingDesired.disabled = false) : (bridgingDesired.disabled = true, bridgingDesired.checked = false);

    // conditions for medication status
    if (selfMed.checked) {
        selfMedLikely.disabled = true;
        noMed.disabled = true;
    }
    else if (selfMedLikely.checked) {
        selfMed.disabled = true;
        noMed.disabled = true;
    }
    else if (noMed.checked) {
        selfMed.disabled = true;
        selfMedLikely.disabled = true;
    }
    else {
        selfMed.disabled = false;
        selfMedLikely.disabled = false;
        noMed.disabled = false;
    }


}

function checkRequired() {
    var countriesSelect = document.getElementById("countries");
    if (countriesSelect.value !== "Choose...") {
        document.getElementById("docx").disabled = false;
        document.getElementById("pdf").disabled = false;
    }
    else {
        document.getElementById("docx").disabled = true;
        document.getElementById("pdf").disabled = true;
    }
}