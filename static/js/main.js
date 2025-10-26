import Alert from "./modules/classes/Alert.js"

// XSS (basic)
const XSS_RE = /<\s*script\b|on\w+\s*=|javascript:|eval\s*\(|document\.cookie/i;

// SQL: blocks any use of reserved words or common query patterns
const SQL_RE = /\b(select|insert|update|delete|drop|create|alter|truncate|replace|merge|exec|execute|union|show|describe|grant|revoke|call)\b|(--|;|' *or *'|'\s*=\s*')/i;

// Function that determines whether text is dangerous
function isSuspicious(text) {
  if (!text) return false;
  const v = String(text);
  return XSS_RE.test(v) || SQL_RE.test(v);
}

function handlePaste(e) {
  const clipboard = e.clipboardData || window.clipboardData;
  const txt = clipboard ? clipboard.getData('text') : '';
  if (isSuspicious(txt)) {
    e.preventDefault();
    Alert.error('Posible inyección detectada (XSS o SQL). Acción bloqueada.');
  }
}

function handleInput(e) {
  const t = e.target;
  const val = t?.value ?? t?.innerText ?? t?.innerHTML ?? '';
  if (isSuspicious(val)) {
    Alert.error('Entrada sospechosa detectada en este campo. No use consultas SQL ni código.');
    try { t.focus(); } catch (err) {}
    t.style.outline = '2px solid red';
  }
}

function handleSubmit(e) {
  const form = e.target;
  if (!form || !form.elements) return;
  for (let el of Array.from(form.elements)) {
    const v = el.value ?? el.innerText ?? el.innerHTML ?? '';
    if (isSuspicious(v)) {
      e.preventDefault();
      Alert.error('Formulario bloqueado: contiene posible consulta SQL o código peligroso.');
      try { el.focus(); } catch (err) {}
      el.style.outline = '2px solid red';
      break;
    }
  }
}

document.addEventListener('paste', handlePaste, true);
document.addEventListener('input', handleInput, true);
document.addEventListener('submit', handleSubmit, true);