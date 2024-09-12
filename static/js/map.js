function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("La géolocalisation n'est pas supportée par ce navigateur.");
    }
}

function showPosition(position) {
    let lat = position.coords.latitude;
    let lng = position.coords.longitude;

    updateMap(lat, lng);
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("L'utilisateur a refusé la demande de géolocalisation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Les informations de position ne sont pas disponibles.");
            break;
        case error.TIMEOUT:
            alert("La demande a expiré.");
            break;
        case error.UNKNOWN_ERROR:
            alert("Une erreur inconnue s'est produite.");
            break;
    }
}

function updateMap(lat, lng) {
    var map = L.map('map').setView([lat, lng], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    L.marker([lat, lng]).addTo(map).bindPopup("Vous êtes ici").openPopup();

    // Requête AJAX pour obtenir les mécaniciens proches
    $.ajax({
        url: '/mecaniciens_proches/',
        data: { lat: lat, lon: lng },
        success: function(data) {
            data.forEach(function(mecanicien) {
                L.marker([mecanicien.lat, mecanicien.lng]).addTo(map)
                    .bindPopup(mecanicien.name + "<br>" + mecanicien.service);
            });
        }
    });
}

window.onload = getLocation;
