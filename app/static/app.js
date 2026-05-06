const dictionary = {
  en: {
    title: "Inbound Driver Safety Intake",
    subtitle: "Please submit required photos before unloading.",
    languageLabel: "Language",
    doorLabel: "Door Number",
    driverLabel: "Driver Name (optional)",
    trailerLabel: "Trailer Number (optional)",
    doorPhoto: "Photo 1: Door",
    trailerPhoto: "Photo 2: Disconnected Trailer",
    chockPhoto: "Photo 3: Chocked Wheels",
    submit: "Submit",
    sending: "Sending...",
    success: "Submitted successfully. Thank you!",
    failed: "Submission failed. Please try again.",
  },
  es: {
    title: "Registro de Seguridad para Conductores",
    subtitle: "Envíe las fotos requeridas antes de descargar.",
    languageLabel: "Idioma",
    doorLabel: "Número de puerta",
    driverLabel: "Nombre del conductor (opcional)",
    trailerLabel: "Número del remolque (opcional)",
    doorPhoto: "Foto 1: Puerta",
    trailerPhoto: "Foto 2: Remolque desconectado",
    chockPhoto: "Foto 3: Ruedas con cuñas",
    submit: "Enviar",
    sending: "Enviando...",
    success: "Enviado correctamente. ¡Gracias!",
    failed: "Error al enviar. Inténtalo de nuevo.",
  },
  fr: {
    title: "Formulaire Sécurité Conducteur",
    subtitle: "Veuillez soumettre les photos requises avant le déchargement.",
    languageLabel: "Langue",
    doorLabel: "Numéro de quai",
    driverLabel: "Nom du conducteur (optionnel)",
    trailerLabel: "Numéro de remorque (optionnel)",
    doorPhoto: "Photo 1 : Quai",
    trailerPhoto: "Photo 2 : Remorque déconnectée",
    chockPhoto: "Photo 3 : Roues calées",
    submit: "Soumettre",
    sending: "Envoi en cours...",
    success: "Soumis avec succès. Merci !",
    failed: "Échec de l’envoi. Réessayez.",
  },
  ht: {
    title: "Fòm Sekirite Chofè Antre",
    subtitle: "Soumèt foto obligatwa yo anvan dechajman.",
    languageLabel: "Lang",
    doorLabel: "Nimewo pòt",
    driverLabel: "Non chofè (opsyonèl)",
    trailerLabel: "Nimewo trelè (opsyonèl)",
    doorPhoto: "Foto 1: Pòt",
    trailerPhoto: "Foto 2: Trelè dekonekte",
    chockPhoto: "Foto 3: Wou bloke",
    submit: "Voye",
    sending: "Ap voye...",
    success: "Voye avèk siksè. Mèsi!",
    failed: "Voye echwe. Tanpri eseye ankò.",
  },
};

const byId = (id) => document.getElementById(id);

function applyLanguage(lang) {
  const t = dictionary[lang] || dictionary.en;
  byId("title").textContent = t.title;
  byId("subtitle").textContent = t.subtitle;
  byId("language_label").textContent = t.languageLabel;
  byId("door_label").textContent = t.doorLabel;
  byId("driver_label").textContent = t.driverLabel;
  byId("trailer_label").textContent = t.trailerLabel;
  byId("door_photo_label").textContent = t.doorPhoto;
  byId("trailer_photo_label").textContent = t.trailerPhoto;
  byId("chock_photo_label").textContent = t.chockPhoto;
  byId("submitBtn").textContent = t.submit;
}

byId("language").addEventListener("change", (event) => {
  applyLanguage(event.target.value);
});

byId("intakeForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const lang = byId("language").value;
  const t = dictionary[lang] || dictionary.en;
  const status = byId("status");
  const button = byId("submitBtn");

  status.textContent = t.sending;
  status.className = "text-sm text-[#995213]";
  button.disabled = true;

  try {
    const formData = new FormData(byId("intakeForm"));
    const response = await fetch("/submit", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      let detail = "Request failed";
      try {
        const payload = await response.json();
        detail = payload.detail || detail;
      } catch (_e) {
        // no-op
      }
      throw new Error(detail);
    }

    byId("intakeForm").reset();
    byId("language").value = lang;
    applyLanguage(lang);
    status.textContent = t.success;
    status.className = "text-sm text-[#2a8703]";
  } catch (error) {
    status.textContent = `${t.failed} ${error.message || ""}`.trim();
    status.className = "text-sm text-[#ea1100]";
  } finally {
    button.disabled = false;
  }
});

applyLanguage("en");
