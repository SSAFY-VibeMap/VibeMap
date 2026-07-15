const HISTORY_KEY = 'vibemap.chat-history';
const SESSION_KEY = 'vibemap.chat-session-active';
const MAX_MESSAGES = 12;
const MAX_MESSAGE_LENGTH = 800;
const MAX_CONTEXT_LENGTH = 4_000;
const MAX_AGE_MS = 1000 * 60 * 60 * 6;

function isBrowser() {
  return typeof window !== 'undefined';
}

function normalizeMessage(message) {
  if (!message || !['user', 'bot'].includes(message.role) || typeof message.text !== 'string') return null;

  const text = message.text.trim().slice(0, MAX_MESSAGE_LENGTH);
  return text ? { role: message.role, text, createdAt: message.createdAt || Date.now() } : null;
}

export function beginChatSession() {
  if (!isBrowser()) return;

  // sessionStorage ends with the browser session. A missing marker means this is a
  // newly opened session, so persisted history from an older one is discarded.
  if (!window.sessionStorage.getItem(SESSION_KEY)) {
    window.localStorage.removeItem(HISTORY_KEY);
    window.sessionStorage.setItem(SESSION_KEY, String(Date.now()));
  }
}

export function loadChatHistory() {
  if (!isBrowser()) return [];

  try {
    const saved = JSON.parse(window.localStorage.getItem(HISTORY_KEY) || '[]');
    if (!Array.isArray(saved)) return [];

    const now = Date.now();
    return saved.map(normalizeMessage).filter((message) => message && now - message.createdAt < MAX_AGE_MS).slice(-MAX_MESSAGES);
  } catch {
    window.localStorage.removeItem(HISTORY_KEY);
    return [];
  }
}

export function saveChatHistory(messages) {
  if (!isBrowser()) return;

  const history = messages.map(normalizeMessage).filter(Boolean).slice(-MAX_MESSAGES);
  try {
    window.localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
  } catch {
    // Storage can be unavailable or full. The chat remains usable without persistence.
  }
}

export function buildChatContext(messages) {
  return messages
    .map(normalizeMessage)
    .filter(Boolean)
    .slice(-MAX_MESSAGES)
    .map(({ role, text }) => `${role === 'user' ? '사용자' : '챗봇'}: ${text}`)
    .join('\n')
    .slice(-MAX_CONTEXT_LENGTH);
}
