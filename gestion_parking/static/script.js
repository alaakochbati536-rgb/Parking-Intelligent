
const video = document.getElementById("video");
const message = document.getElementById("camera-message");

let vehicules = [];

function ouvrirCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            video.srcObject = stream;
            message.style.display = "none";
        })
        .catch(function() {
            message.textContent = "Impossible d'ouvrir la caméra";
        });
}

function afficherDate() {
    const maintenant = new Date();

    document.getElementById("date").value =
        maintenant.toISOString().slice(0, 10);

    document.getElementById("heure").value =
        maintenant.toTimeString().slice(0, 5);
}

function pointer(type) {
    const plaque = document.getElementById("plaque").value.trim();

    if (plaque === "") {
        alert("Veuillez saisir le numéro de plaque !");
        return;
    }

    const maintenant = new Date();

    if (type === "entree") {
        vehicules.push({
            plaque: plaque,
            entree: maintenant,
            sortie: null
        });

        alert("Entrée enregistrée !");
    } else {
        const voiture = vehicules.find(v =>
            v.plaque === plaque && v.sortie === null
        );

        if (!voiture) {
            alert("Véhicule introuvable !");
            return;
        }

        voiture.sortie = maintenant;

        const duree = Math.floor(
            (voiture.sortie - voiture.entree) / 60000
        );

        alert("Sortie enregistrée ! Durée : " + duree + " minutes");
    }

    afficherListe();
    afficherStatistiques();
    afficherDate();
}

function afficherListe() {
    const liste = document.getElementById("liste");
    liste.innerHTML = "";

    vehicules.forEach(v => {
        const ligne = document.createElement("tr");

        ligne.innerHTML = `
            <td>${v.plaque}</td>
            <td>${v.entree.toLocaleTimeString()}</td>
            <td>${v.sortie ? v.sortie.toLocaleTimeString() : "En parking"}</td>
        `;

        liste.appendChild(ligne);
    });
}

function afficherStatistiques() {
    document.getElementById("total-voitures").textContent =
        vehicules.length;

    document.getElementById("total-entrees").textContent =
        vehicules.length;

    document.getElementById("total-sorties").textContent =
        vehicules.filter(v => v.sortie !== null).length;
}

window.onload = function() {
    afficherDate();
    ouvrirCamera();
};
