// backend/telegramNotifier.js
// elimina: const fetch = require('node-fetch');
const TOKEN   = "7200520916:AAFB9qSZZd0-mGWpbU-lq2MU9bb_JKD3E2o";
const CHAT_ID = "7326632476";

async function sendTelegramMessage(message) {
  const url = `https://api.telegram.org/bot${TOKEN}/sendMessage`;
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: CHAT_ID, text: message }),
    });
    const data = await res.json();
    if (!data.ok) console.error("Telegram API error:", data);
  } catch (err) {
    console.error("Error sending Telegram message:", err);
  }
}

module.exports = { sendTelegramMessage };
