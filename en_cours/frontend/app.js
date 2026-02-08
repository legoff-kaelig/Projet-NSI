const output = document.getElementById("output");
const baseUrlInput = document.getElementById("baseUrl");
const nowButton = document.getElementById("nowButton");
const clearOutputButton = document.getElementById("clearOutput");

const createForm = document.getElementById("createForm");
const settingsForm = document.getElementById("settingsForm");
const weatherForm = document.getElementById("weatherForm");

function formatTimestamp(date) {
  const pad = (value) => String(value).padStart(2, "0");
  const month = pad(date.getMonth() + 1);
  const day = pad(date.getDate());
  const year = date.getFullYear();
  let hours = date.getHours();
  const minutes = pad(date.getMinutes());
  const seconds = pad(date.getSeconds());
  const ampm = hours >= 12 ? "PM" : "AM";
  hours = hours % 12;
  if (hours === 0) {
    hours = 12;
  }
  const hoursText = pad(hours);
  return `${month}/${day}/${year}, ${hoursText}:${minutes}:${seconds} ${ampm}`;
}

function setOutput(message, payload) {
  let text = message;
  if (payload !== undefined) {
    if (typeof payload === "string") {
      text += `\n\n${payload}`;
    } else {
      text += `\n\n${JSON.stringify(payload, null, 2)}`;
    }
  }
  output.textContent = text;
}

function getBaseUrl() {
  const value = baseUrlInput.value.trim();
  return value || "http://127.0.0.1:8000/auth";
}

async function sendRequest(payload) {
  const url = getBaseUrl();
  setOutput("Sending request...", payload);

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const bodyText = await response.text();
    let parsed = bodyText;
    try {
      parsed = JSON.parse(bodyText);
    } catch (error) {
      parsed = bodyText;
    }

    setOutput(`Status ${response.status} ${response.statusText}`, parsed);
  } catch (error) {
    setOutput("Request failed", error instanceof Error ? error.message : String(error));
  }
}

function readText(form, name) {
  const value = form.elements[name]?.value ?? "";
  return String(value).trim();
}

function readNumber(form, name) {
  const value = readText(form, name);
  if (!value) {
    return null;
  }
  const numberValue = Number(value);
  return Number.isNaN(numberValue) ? null : numberValue;
}

function readBooleanSelect(form, name) {
  const value = readText(form, name);
  if (value === "true") {
    return true;
  }
  if (value === "false") {
    return false;
  }
  return null;
}

createForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const payload = {
    action: "create_user",
    username: readText(createForm, "username"),
    email: readText(createForm, "email"),
    password_hash: readText(createForm, "password_hash"),
  };
  sendRequest(payload);
});

settingsForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const payload = {
    action: "update_settings",
    user_id: readNumber(settingsForm, "user_id"),
    password_hash: readText(settingsForm, "password_hash"),
  };

  const optionalFields = [
    ["username", readText(settingsForm, "username")],
    ["email", readText(settingsForm, "email")],
    ["location", readText(settingsForm, "location")],
    ["city", readText(settingsForm, "city")],
  ];

  for (const [key, value] of optionalFields) {
    if (value) {
      payload[key] = value;
    }
  }

  const refreshRate = readNumber(settingsForm, "refreshRate_minutes");
  if (refreshRate !== null) {
    payload.refreshRate_minutes = refreshRate;
  }

  const is24HourFormat = readBooleanSelect(settingsForm, "is24HourFormat");
  if (is24HourFormat !== null) {
    payload.is24HourFormat = is24HourFormat;
  }

  const isMetricSystem = readBooleanSelect(settingsForm, "isMetricSystem");
  if (isMetricSystem !== null) {
    payload.isMetricSystem = isMetricSystem;
  }

  const setupWizardDone = readBooleanSelect(settingsForm, "setupWizardDone");
  if (setupWizardDone !== null) {
    payload.setupWizardDone = setupWizardDone;
  }

  sendRequest(payload);
});

weatherForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const payload = {
    action: "update_weather",
    user_id: readNumber(weatherForm, "user_id"),
    password_hash: readText(weatherForm, "password_hash"),
    location: readText(weatherForm, "location"),
    timestamp: readText(weatherForm, "timestamp"),
  };
  sendRequest(payload);
});

nowButton.addEventListener("click", () => {
  weatherForm.elements.timestamp.value = formatTimestamp(new Date());
});

clearOutputButton.addEventListener("click", () => {
  output.textContent = "Waiting for a request.";
});

weatherForm.elements.timestamp.value = formatTimestamp(new Date());
