const form = document.getElementById('chat-form');
const input = document.getElementById('input-msg');
const messagesEl = document.getElementById('messages');

function appendMessage(text, role = 'assistant') {
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  div.appendChild(bubble);
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  appendMessage(text, 'user');
  input.value = '';

  const loadingMsg = document.createElement('div');
  loadingMsg.className = 'msg assistant';
  loadingMsg.innerHTML = '<div class="bubble">...</div>';
  messagesEl.appendChild(loadingMsg);
  messagesEl.scrollTop = messagesEl.scrollHeight;

  try {
    const resp = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, use_context: true, top_k: 3 })
    });

    if (!resp.ok) {
      const err = await resp.text();
      throw new Error(err || 'Erro na requisição');
    }

    const data = await resp.json();
    loadingMsg.remove();

    if (data.context && data.context.length) {
      appendMessage('Contexto utilizado:\n' + data.context.map((c, i) => `${i+1}. ${c.slice(0, 300).replace(/\n/g,' ')}...`).join('\n\n'), 'assistant');
    }

    appendMessage(data.reply, 'assistant');
  } catch (err) {
    loadingMsg.remove();
    appendMessage('Erro: ' + err.message, 'assistant');
  }
});
