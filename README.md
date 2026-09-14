<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BILLIE — Assistente Virtual</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="header">
    <a class="logo" href="#inicio">BILLIE</a>
    <button class="menu-btn" id="menuBtn" aria-label="Abrir menu">
      ☰
    </button>
    <nav id="nav">
      <a href="#inicio">Início</a>
      <a href="#recursos">Recursos</a>
      <a href="#sobre">Sobre</a>
    </nav>
  </header>
  <main>
    <section class="hero" id="inicio">
      <div class="hero-text">
        <p class="eyebrow">SEU ASSISTENTE VIRTUAL</p>
        <h1>
          Olá! Eu sou a <span>BILLIE</span>.
        </h1>
        <p>
          Uma assistente virtual simples, rápida e feita
          para ajudar você no dia a dia.
        </p>
        <a class="button" href="#assistente">
          Conversar com a BILLIE
        </a>
      </div>
    </section>
    <section class="assistant" id="assistente">
      <p class="status">
        ● BILLIE está pronta
      </p>
      <h2>
        O que você quer fazer?
      </h2>
      <div class="command-box">
        <input
          id="commandInput"
          type="text"
          placeholder="Digite um comando..."
          autocomplete="off"
        >
        <button id="sendBtn">
          Enviar
        </button>
      </div>
      <div class="quick-actions">
        <button data-command="Que horas são?">
          🕐 Horário
        </button>
        <button data-command="Me dê uma ideia">
          💡 Ideia
        </button>
        <button data-command="Olá BILLIE">
          👋 Olá
        </button>
      </div>
      <div class="response" id="response">
        Digite algo para começar.
      </div>
    </section>
    <section class="features" id="recursos">
      <h2>
        Recursos
      </h2>
      <div class="cards">
        <article>
          <h3>
            💬 Conversar
          </h3>
          <p>
            Interaja com a BILLIE por comandos simples.
          </p>
        </article>
        <article>
          <h3>
            📅 Organizar
          </h3>
          <p>
            Planeje ideias, compromissos e tarefas.
          </p>
        </article>
        <article>
          <h3>
            ⚡ Atalhos
          </h3>
          <p>
            Uma base preparada para futuras integrações.
          </p>
        </article>
      </div>
    </section>
    <section class="about" id="sobre">
      <h2>
        Sobre a BILLIE
      </h2>
      <p>
        Esta é a primeira versão do projeto BILLIE.
        A ideia é evoluir a assistente com voz,
        comandos e integração com recursos do iPhone.
      </p>
    </section>
  </main>
  <footer>
    © 2026 BILLIE
  </footer>
  <script src="script.js"></script>
</body>
</html>