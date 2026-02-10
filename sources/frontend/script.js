const API_URL = "http://127.0.0.1:8000/auth";
const USER_ID = 1;
const PASSWORD_HASH = "demo_hash";

let weatherRequestInProgress = false;
const WEATHER_ICON_MAP = {
  clear: ["1000"],
  partly_cloudy: ["1100", "1101", "1103"],
  cloudy: ["1001", "1102"],
  fog: ["2000", "2100"],
  rain: ["4000", "4001", "4200", "4201"],
  snow: ["5000", "5001", "5100", "5101"],
  freezing_rain: ["6000", "6001", "6200", "6201"],
  ice_pellets: ["7000", "7101", "7102"],
  thunderstorm: ["8000"]
};

// Animation de clic sur les éléments de navigation
document.querySelectorAll(".nav-item").forEach(item => {
  item.addEventListener("click", () => {
    item.style.transform = "scale(0.9)";
    setTimeout(() => item.style.transform = "", 150);
  });
});

// Récupère la position de l'utilisateur afin de l'utiliser pour la requête météo
function getUserLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject("Geolocation non supportée");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        resolve({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude
        });
      },
      (err) => {
        reject(err.message);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 600000
      }
    );
  });
}

// Extrait le nombre de secondes à attendre pour la prochaie requête (en cas de rate limit)
function extractWaitSeconds(details) {
  const match = details?.match(/wait (\d+)s/);
  return match ? parseInt(match[1], 10) : null;
}

// Arrondit une température à 1 chiffre après la virgule et en supprimant le .0 si c'est un entier
function formatTemperature(temp) {
  if (temp === null || temp === undefined) return "--";

  const rounded = Math.round(temp * 10) / 10;

  if (Number.isInteger(rounded)) {
    return `${rounded}`;
  }

  return `${rounded.toFixed(1)}`;
}

// Déplace le curseur de l'indicateur AQI en fonction de la valeur (1-200)
function moveAQICursor(aqiValue) {
  const cursor = document.getElementById("movable");
  if (aqiValue === null) return;

  const MIN = 1;
  const MAX = 200;
  const clamped = Math.max(MIN, Math.min(MAX, aqiValue));
  const percent = ((clamped - MIN) / (MAX - MIN)) * 100;
  cursor.style.left = `${percent}%`;
}

// Convertit un code météo en une description textuelle
function getWeatherLabel(weatherCode) {
  const code = String(weatherCode);

  if (code === "1000") return "Ensoleillé";
  if (code === "1100" || code === "1101" || code === "1103") return "Partiellement nuageux";
  if (code === "1001" || code === "1102") return "Nuageux";
  if (code.startsWith("2")) return "Brouillard";
  if (code.startsWith("4")) return "Pluie";
  if (code.startsWith("5")) return "Neige";
  if (code.startsWith("6")) return "Pluie verglaçante";
  if (code.startsWith("7")) return "Grêle";
  if (code.startsWith("8")) return "Orage";
  return "Météo inconnue";
}

// Convertit un code météo en une icone
function getWeatherIcon(weatherCode) {
  if (!weatherCode) return;
  const code = String(weatherCode);

  for (const [icon, codes] of Object.entries(WEATHER_ICON_MAP)) {
    if (
      codes.some(base => code === base || code.startsWith(base))
    ) {
      return icon;
    }
  }

  const family = code.charAt(0);

  switch (family) {
    case "1": return "cloudy";
    case "2": return "fog";
    case "4": return "rain";
    case "5": return "snow";
    case "6": return "freezing_rain";
    case "7": return "ice_pellets";
    case "8": return "thunderstorm";
    default: return "partly_cloudy";
  }
}

// Effectue la requête de mise à jour météo et gère les différentes réponses (succès, rate limit, erreurs)
async function updateWeather(elements) {
  weatherRequestInProgress = true;
  let latitude = 48.8566; // Par défaut : Paris
  let longitude = 2.3522;

  try {
    const loc = await getUserLocation();
    latitude = loc.latitude;
    longitude = loc.longitude;
  } catch (e) {
    console.log(e);
  }

  const payload = {
    action: "update_weather",
    user_id: USER_ID,
    password_hash: PASSWORD_HASH,
    latitude,
    longitude,
  };

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const raw = await res.text();
    let data;
    try {
      data = JSON.parse(raw);
    } catch (e) {
      console.log(e);
    }

    if (res.status === 200 && data.status === "ok") {
      localStorage.setItem("weather_cache", JSON.stringify(data.weather_update));
      displayWeather(elements, data.weather_update);
      return;
    }

    if (res.status === 429) {
      console.warn("Rate limit détecté");

      const waitSeconds = extractWaitSeconds(data.details);
      console.log("waitSeconds =", waitSeconds);

      const cached = localStorage.getItem("weather_cache");
      if (cached) {
        displayWeather(elements, JSON.parse(cached));
        return;
      }
      console.warn("Aucun cache météo disponible");
      return;
    }

    console.error("Erreur backend :", data);

  } catch (e) {
    console.log(e);
  } finally {
    weatherRequestInProgress = false;
  }
}

// Affiche les données météo dans l'interface
function displayWeather(elements, w) {
  console.log("displayWeather", w);

  elements.city.textContent = w.city;
  elements.date.textContent = new Date(w.timestamp).toLocaleDateString("fr-FR");
  elements.statut.textContent = getWeatherLabel(w.weather_code);
  elements.temp.textContent = `${formatTemperature(w.temperature)}°C`;
  elements.ressenti.textContent = w.feels_like !== undefined ? `${w.feels_like}°C` : "—";
  elements.precip.textContent = w.precipitation !== undefined ? `${w.precipitation}%` : "—";
  elements.wind.textContent = w.wind_speed !== undefined ? `${w.wind_speed} km/h` : "—";
  elements.humidity.textContent = w.humidity !== undefined ? `${w.humidity}%` : "—";
  const aqi = w.european_aqi;
  moveAQICursor(aqi);
  const icon = getWeatherIcon(w.weather_code);
  elements.img.src = `assets/img/${icon}.svg`;
}

// Initialise l'interface et lance la première requête météo au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
  const elements = {
    date: document.getElementById("date"),
    statut: document.getElementById("statut"),
    city: document.getElementById("city"),
    temp: document.getElementById("temp"),
    img: document.getElementById("modifiable-img"),
    ressenti: document.querySelector("#temperature span"),
    precip: document.querySelector("#precipitations span"),
    wind: document.querySelector("#wind span"),
    humidity: document.querySelector("#humidity span"),
  };
  updateWeather(elements);
});