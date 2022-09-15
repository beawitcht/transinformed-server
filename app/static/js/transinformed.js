window.addEventListener('load', function () {
    // Countries dropdown
    document.getElementById('countries').addEventListener('change', countryFilters);
    // Medication Status
    document.getElementById('selfMedCheck').addEventListener('click', checkboxStatus);
    document.getElementById('likelyMedCheck').addEventListener('click', checkboxStatus);
    document.getElementById('noMedCheck').addEventListener('click', checkboxStatus);
    // Documents Held
    document.getElementById('diagnosisCheck').addEventListener('click', checkboxStatus);
    document.getElementById('hrtCheck').addEventListener('click', checkboxStatus);
    document.getElementById('noDocCheck').addEventListener('click', checkboxStatus);
    // GIC selector
    document.getElementById('referralCheck').addEventListener('click', revealContent);
    $("#gics option[id='Northern Ireland']").hide();
    $("#gics option[id='Scotland']").hide();
    $("#gics option[id='Wales']").hide();
    $("#gics option[id='England']").hide();

    // Private provider selector
    document.getElementById('sharedCareCheck').addEventListener('click', revealContent);
    // Private provider dropdown
    document.getElementById('privateProviderList').addEventListener('change', privateProviderConditions);

    // Immigration options
    document.getElementById('immigrationCheck').addEventListener('click', revealContent);
    document.getElementById('immigrationCheck').addEventListener('click', checkboxStatus);
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
    var immCheck = document.getElementById("immigrationCheck");
    var immLetter = document.getElementById("immigrationLetterCheck");

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

    // conditions for immigration options
    if (!immCheck.checked){
        immLetter.checked = false;
    }


}

function countryFilters() {
    var countriesSelect = document.getElementById("countries");
    // Only allow submission when a country is selected
    if (countriesSelect.value !== "Choose...") {
        document.getElementById("docx").disabled = false;
        document.getElementById("pdf").disabled = false;
    }
    else {
        document.getElementById("docx").disabled = true;
        document.getElementById("pdf").disabled = true;
    }
    // filter valid GICs based on country
    $("#gics").val(0).change();
    if (countriesSelect.value === "England") {
        $("#gics option[id='countryNeeded']").hide();
        $("#gics").val(1).change();
        $("#gics option[id='Northern Ireland']").hide();
        $("#gics option[id='Scotland']").hide();
        $("#gics option[id='Wales']").hide();
        $("#gics option[id='England']").show();
    }
    else if (countriesSelect.value === "Northern Ireland") {
        $("#gics option[id='countryNeeded']").hide();
        $("#gics").val(1).change();
        $("#gics option[id='England']").hide();
        $("#gics option[id='Scotland']").hide();
        $("#gics option[id='Wales']").hide();
        $("#gics option[id='Northern Ireland']").show();
    }
    else if (countriesSelect.value === "Scotland") {
        $("#gics option[id='countryNeeded']").hide();
        $("#gics").val(1).change();
        $("#gics option[id='England']").hide();
        $("#gics option[id='Northern Ireland']").hide();
        $("#gics option[id='Wales']").hide();
        $("#gics option[id='Scotland']").show();
    }
    else if (countriesSelect.value === "Wales") {
        $("#gics option[id='countryNeeded']").hide();
        $("#gics").val(1).change();
        $("#gics option[id='England']").hide();
        $("#gics option[id='Northern Ireland']").hide();
        $("#gics option[id='Scotland']").hide();
        $("#gics option[id='Wales']").show();
    }
    else {
        $("#gics option[id='countryNeeded']").show();
        $("#gics option[id='Northern Ireland']").hide();
        $("#gics option[id='Scotland']").hide();
        $("#gics option[id='Wales']").hide();
        $("#gics option[id='England']").hide();
    }
    
    
}

function revealContent() {
    var referralCheck = document.getElementById("referralCheck");
    var sharedCareCheck = document.getElementById("sharedCareCheck");
    var gicSelector = document.getElementById("gicSelector");
    var privateSelector = document.getElementById("privateSelector");
    var immigrationCheck = document.getElementById("immigrationCheck");
    var immigrationOption = document.getElementById("immigrationOption");
    referralCheck.checked ? gicSelector.hidden = false : gicSelector.hidden = true;
    sharedCareCheck.checked ? privateSelector.hidden = false : privateSelector.hidden = true;
    immigrationCheck.checked ? immigrationOption.hidden = false : immigrationOption.hidden = true;
}

function privateProviderConditions(){
    var privateProviderList = document.getElementById("privateProviderList");
    var privateProviderWarningMessage = document.getElementById("notUK")
    var privateProviderPreferredMessage = document.getElementById("preferred")
    if (privateProviderList.value === "GenderGP") {
        privateProviderList.classList.remove("is-valid");
        privateProviderList.classList.add("is-invalid");
        privateProviderWarningMessage.innerText =  "This provider is not based in the UK, which deters a lot of GPs from agreeing to shared care."
    }
    else if (privateProviderList.value.includes("Other") || privateProviderList.value.includes("haven't chosen")) {
        privateProviderList.classList.remove("is-invalid");
        privateProviderList.classList.remove("is-valid");
        privateProviderPreferredMessage.innerText = ""
        privateProviderWarningMessage.innerText = ""

    }
    else {
        privateProviderList.classList.remove("is-invalid");
        privateProviderList.classList.add("is-valid");
        privateProviderPreferredMessage.innerText =  "This provider offers GMC registered and UK based specialists."
    }
}