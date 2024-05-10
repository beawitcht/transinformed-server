window.addEventListener('load', function () {
    revealContentReferral();
    revealContentSharedCare();
    revealContentImmigration();
    privateProviderConditions();
    countryServiceFilters();
    serviceFilters();
    // Countries dropdown
    document.getElementById('countries').addEventListener('change', countryServiceFilters);
    // Services dropdown
    document.getElementById('services').addEventListener('change', serviceFilters);
    // Medication Status
    document.getElementById('selfMedCheck').addEventListener('click', checkMedStatus);
    document.getElementById('likelyMedCheck').addEventListener('click', checkMedStatus);
    document.getElementById('noMedCheck').addEventListener('click', checkMedStatus);
    // Documents Held
    document.getElementById('diagnosisCheck').addEventListener('click', checkDocStatus);
    document.getElementById('hrtCheck').addEventListener('click', checkDocStatus);
    document.getElementById('noDocCheck').addEventListener('click', checkDocStatus);
    // GIC selector
    document.getElementById('referralCheck').addEventListener('click', revealContentReferral);

    // Private provider selector
    document.getElementById('sharedCareCheck').addEventListener('click', revealContentSharedCare);
    // Private provider dropdown
    document.getElementById('privateProviderList').addEventListener('change', privateProviderConditions);

    // Immigration options
    document.getElementById('immigrationCheck').addEventListener('click', revealContentImmigration);

    //Age checkbox
    document.getElementById('under16Check').addEventListener('click', checkAgeStatus);

    document.getElementById("docx").addEventListener('click', submitActionsDocx);
    document.getElementById("pdf").addEventListener('click', submitActionsPdf);

});

function checkDocStatus() {
    // conditions for Documents held
    (diagnosisCheck.checked || hrtCheck.checked) ? (noDocCheck.disabled = true) : (noDocCheck.disabled = false);
    noDocCheck.checked ? (diagnosisCheck.disabled = true, hrtCheck.disabled = true) : (diagnosisCheck.disabled = false, hrtCheck.disabled = false);

    // update bridging status as relevant
    bridgingCheck();

}

function checkAgeStatus() {
    // conditions for age options
    if (under16Check.checked) {
        sharedCareCheck.parentNode.hidden = true;
        sharedCareCheck.checked = false;
        privateSelector.hidden = true;
        privateProviderList.value = "I haven't chosen a provider yet";
        bridgingDesired.parentNode.hidden = true;
        bridgingDesired.checked = false
        bloodTests.parentNode.hidden = true;
        bloodTests.checked = false;
        grcCheck.parentNode.hidden = true;
        grcCheck.checked = false;
        medStatusSection.hidden = true;
        // unchecks all medStatusSection checkboxes
        $('#medStatusSection').find('input:checked[type=checkbox]').prop('checked', false);
        services.value = "Youth (≤16)";
        $("#services option[value='Adult (17+)']").hide();
        serviceFilters();
    }
    else {
        sharedCareCheck.parentNode.hidden = false;
        bridgingDesired.parentNode.hidden = false;
        bloodTests.parentNode.hidden = false;
        grcCheck.parentNode.hidden = false;
        medStatusSection.hidden = false;

        $("#services option[value='Adult (17+)']").show();
        serviceFilters();
    }
}

function bridgingCheck() {
    if (noMedCheck.checked) {
        bridgingDesired.disabled = true;
    }

    // conditions for bridging
    (selfMedCheck.checked || likelyMedCheck.checked) && !hrtCheck.checked && !noMedCheck.checked ? (bridgingDesired.disabled = false, bridgingDesiredLabel.innerHTML = 'I need a bridging prescription') : (bridgingDesired.disabled = true, bridgingDesired.checked = false, bridgingDesiredLabel.innerHTML = 'I need a bridging prescription (invalid medication status for bridging)');

    if (hrtCheck.checked) {
        bridgingDesired.disabled = true;
        bridgingDesired.checked = false;
        bridgingDesiredLabel.innerHTML = 'I need a bridging prescription (invalid document status for bridging)';
    }

    if ($('.med-status-check:checked').length === 0 && !hrtCheck.checked) {
        bridgingDesired.disabled = true;
        bridgingDesired.checked = false;
        bridgingDesiredLabel.innerHTML = "I need a bridging prescription (select medication status)";
    }
}

function checkMedStatus() {
    // set check boxes
    if (noMedCheck.checked) {
        bridgingDesired.disabled = true;
    }
    // conditions for medication status
    if (selfMedCheck.checked) {
        likelyMedCheck.disabled = true;
        noMedCheck.disabled = true;
    }
    else if (likelyMedCheck.checked) {
        selfMedCheck.disabled = true;
        noMedCheck.disabled = true;
    }
    else if (noMedCheck.checked) {
        selfMedCheck.disabled = true;
        likelyMedCheck.disabled = true;
    }
    else {
        selfMedCheck.disabled = false;
        likelyMedCheck.disabled = false;
        noMedCheck.disabled = false;
    }
    // update bridging status as relevant
    bridgingCheck();
}

function serviceFilters() {
    // selected country dependent on youth services for valid options
    countryServiceFilters();

    //  change youth options to available services
    services.value == "Youth (≤16)" ? grcCheck.disabled = true : grcCheck.disabled = false;

}

function countryServiceFilters() {
    var selectedCountry = countries.value;
    var selectedService = services.value;

    // Only allow submission when a country is selected
    disableButtonsLogic();

    // Define a mapping between countries and their corresponding GIC options
    if (selectedService == "Youth (≤16)") {
        var countryGICMapping = {
            "Y-England": ["Y-England"],
            "Y-Northern Ireland": ["Y-Northern Ireland"],
            "Y-Scotland": ["Y-Scotland"],
            "Y-Wales": ["Y-Wales"]
        };
    } else {
        var countryGICMapping = {
            "England": ["England"],
            "Northern Ireland": ["Northern Ireland"],
            "Scotland": ["Scotland"],
            "Wales": ["Wales"]
        };
    }

    // Hide all country options initially

    $("#gics option[value='Y-England'], #gics option[value='Y-Northern Ireland'], #gics option[value='Y-Scotland'], #gics option[value='Y-Wales']").hide();

    $("#gics option[value='England'], #gics option[value='Northern Ireland'], #gics option[value='Scotland'], #gics option[value='Wales']").hide();



    // Show the options related to the selected country and service
    if (countryGICMapping[selectedCountry] && selectedService !== "Choose...") {
        countryGICMapping[selectedCountry].forEach(option => {
            $("#gics option[value='" + option + "']").show();
        });
        $("#gics").val(1).change();
        $("#gics option[value='0']").hide();
        $("#gics option[value='1']").show();

    } else if (countryGICMapping["Y-" + selectedCountry] && selectedService !== "Choose...") {
        countryGICMapping["Y-" + selectedCountry].forEach(option => {
            $("#gics option[value='" + option + "']").show();
        });
        $("#gics").val(1).change();
        $("#gics option[value='0']").hide();
        $("#gics option[value='1']").show();

    } else {
        $("#gics option[value='0']").show();
        $("#gics option[value='1']").hide();
    }

}

function revealContentReferral() {
    referralCheck.checked ? gicSelector.hidden = false : (gicSelector.hidden = true, countryServiceFilters());
}

function revealContentSharedCare() {
    if (sharedCareCheck.checked) {
        privateSelector.hidden = false;
    }
    else {
        privateSelector.hidden = true;
        privateProviderList.value = "I haven't chosen a provider yet";
        $("#privateProviderList").removeClass("is-valid");
        $("#privateProviderList").removeClass("is-invalid");
    }
}

function revealContentImmigration() {
    immigrationCheck.checked ? immigrationOption.hidden = false : (immigrationOption.hidden = true, immigrationLetterCheck.checked = false);
}

function privateProviderConditions() {
    var privateProviderWarningMessage = document.getElementById("notUK");
    var privateProviderPreferredMessage = document.getElementById("preferred");
    if (privateProviderList.value === "GenderGP") {
        privateProviderList.classList.remove("is-valid");
        privateProviderList.classList.add("is-invalid");
        privateProviderWarningMessage.innerText = "This provider is not based in the UK, which deters some GPs from agreeing to shared care."
    }
    else if (privateProviderList.value.includes("Other") || privateProviderList.value.includes("haven't chosen")) {
        privateProviderList.classList.remove("is-invalid");
        privateProviderList.classList.remove("is-valid");
        privateProviderPreferredMessage.innerText = "";
        privateProviderWarningMessage.innerText = "";
    }
    else {
        privateProviderList.classList.remove("is-invalid");
        privateProviderList.classList.add("is-valid");
        privateProviderPreferredMessage.innerText = "This provider offers GMC registered and UK based specialists.";
    }
}

function disableButtonsLogic() {
    let docx = document.getElementById("docx")
    let pdf = document.getElementById("pdf")
    // Only allow submission when a country and service is selected
    if (countries.value !== "Choose..." && services.value !== "Choose...") {
        docx.disabled = false;
        if (pdf.innerText !== "PDF Unavailable") {
            pdf.disabled = false;
        }

    }
    else {
        docx.disabled = true;
        pdf.disabled = true;
    }
}
// do these on submitting word
function submitActionsDocx() {
    $(this).append('<input type="hidden" name="docx" value="docx" /> ');
    $("#generationForm").removeProp("target");
    submitActions();
}

// do these on submitting pdf
function submitActionsPdf() {
    $(this).append('<input type="hidden" name="pdf" value="pdf" /> ');
    $("#generationForm").prop({ "target": "_blank" });
    submitActions();
}

function submitActions() {
    if (gics.value !== "0") {
        if (gics.value !== "1") {
            $("#gics :selected").val($("#gics :selected").text());
        };
    };
    document.getElementById("generationForm").submit();

    const alertPlaceholder = document.getElementById('alertPlaceholder')
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
        `<div class="alert alert-success alert-dismissible" role="alert">`,
        `   <div>Thank you for using our document generator, if you found this service useful please <a href="https://opencollective.com/beawitching/donate/" class="alert-link" target="_blank" >consider donating</a> so that we can maintain this service.</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('')
    alertPlaceholder.append(wrapper)
}
