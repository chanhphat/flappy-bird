import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Fishy Dive", page_icon="🐠", layout="centered")
st.title("Fishy Dive")
st.caption("Chơi, kiếm điểm, đổi skin cá")

html = '''
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: #061f39;
    font-family: Arial, sans-serif;
  }
  #game-shell {
    width: 430px;
    height: 620px;
    margin: 14px auto;
    position: relative;
    border: 4px solid #123d5d;
    border-radius: 14px;
    overflow: hidden;
    background: linear-gradient(#061f39, #0d4f7f 50%, #0aa4c8);
    box-shadow: 0 12px 25px rgba(0,0,0,0.25);
  }
  #scoreText {
    position: absolute;
    top: 12px;
    left: 0;
    width: 100%;
    text-align: center;
    color: white;
    font-weight: bold;
    font-size: 34px;
    text-shadow: 2px 2px 0 #000;
    z-index: 4;
    pointer-events: none;
  }
  canvas {
    display: block;
    width: 100%;
    height: 100%;
  }
  .panel {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(4, 16, 30, 0.6);
    z-index: 10;
  }
  .panel.hidden { display: none; }
  .panel-box {
    width: 82%;
    padding: 24px 20px;
    border-radius: 16px;
    text-align: center;
    color: white;
    background: rgba(18, 38, 60, 0.9);
    border: 2px solid rgba(255,255,255,0.2);
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
  }
  .title {
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 12px;
  }
  .subtitle {
    font-size: 15px;
    opacity: 0.9;
    margin-bottom: 18px;
  }
  .button-row {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 8px;
  }
  button {
    border: none;
    border-radius: 12px;
    padding: 12px 18px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
  }
  .primary {
    background: linear-gradient(#5ad0ff, #2aa6df);
    color: #03283d;
  }
  .secondary {
    background: linear-gradient(#ffcd67, #f7a33a);
    color: #4d2a00;
  }
</style>

<div id="game-shell">
  <div id="scoreText">0</div>
  <canvas id="gameCanvas" width="430" height="620"></canvas>

  <div id="startScreen" class="panel">
    <div class="panel-box">
      <div class="title">Fishy Dive</div>
      <div class="subtitle">Bấm để chơi</div>
      <div class="button-row">
        <button id="startBtn" class="primary">Chơi</button>
      </div>
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreText = document.getElementById("scoreText");
const startScreen = document.getElementById("startScreen");

const fishCatalog = [
  { id: "classic", name: "Cá xanh", kind: "classic", body: "#4ec0d8", fin: "#f7b152", accent: "#f4805d", shadow: "#1a2d3a" },
  { id: "shark", name: "Cá mập", kind: "shark", body: "#8c9aa3", fin: "#d8dee5", accent: "#4f6570", shadow: "#2d3942" },
  { id: "dolphin", name: "Cá heo", kind: "dolphin", body: "#5db8d7", fin: "#f4d35e", accent: "#e9f7ff", shadow: "#234c63" },
  { id: "moonfish", name: "Cá mặt trăng", kind: "moonfish", body: "#f6e6ff", fin: "#ffe59a", accent: "#d8c0ff", shadow: "#6f5d90" }
];

const state = {
  selectedFish: "classic",
  score: 0,
  playing: false
};

const game = {
  bird: { x: 110, y: 300, r: 18, vy: 0, rot: 0 },
  pipes: [],
  lastTime: 0,
  spawnTimer: 0,
  score: 0
};

function getSelectedFish() {
  return fishCatalog.find(f => f.id === state.selectedFish) || fishCatalog[0];
}

function resetGame() {
  game.bird.x = 110;
  game.bird.y = 300;
  game.bird.vy = 0;
  game.bird.rot = 0;
  game.pipes = [];
  game.spawnTimer = 0;
  game.score = 0;
  state.score = 0;
  scoreText.textContent = "0";
}

function startGame() {
  resetGame();
  state.playing = true;
  startScreen.classList.add("hidden");
  game.bird.vy = -7.5;
}

function flap() {
  if (!state.playing) {
    startGame();
    return;
  }
  game.bird.vy = -7.5;
}

function spawnPipe() {
  const gap = 170;
  const topHeight = 80 + Math.random() * (canvas.height - 80 - gap - 150);
  game.pipes.push({
    x: canvas.width + 30,
    width: 72,
    gap: gap,
    topHeight: topHeight,
    passed: false
  });
}

function endGame() {
  state.playing = false;
  startScreen.classList.remove("hidden");
  startScreen.querySelector(".subtitle").textContent = "Game Over - Bấm Chơi lại";
  startScreen.querySelector(".title").textContent = "Fishy Dive";
  document.getElementById("startBtn").textContent = "Chơi lại";
}

function update(dt) {
  if (!state.playing) return;

  game.bird.vy += 0.42 * dt * 0.06;
  game.bird.y += game.bird.vy * dt * 0.06;
  game.bird.rot = Math.max(-1.25, Math.min(1.5, game.bird.vy / 10));

  game.spawnTimer += dt;
  if (game.spawnTimer >= 1500) {
    spawnPipe();
    game.spawnTimer = 0;
  }

  for (const pipe of game.pipes) {
    pipe.x -= 2.2 * dt * 0.06;

    if (!pipe.passed && pipe.x + pipe.width < game.bird.x) {
      pipe.passed = true;
      game.score += 1;
      state.score = game.score;
      scoreText.textContent = String(game.score);
    }

    const birdLeft = game.bird.x - game.bird.r;
    const birdRight = game.bird.x + game.bird.r;
    const birdTop = game.bird.y - game.bird.r;
    const birdBottom = game.bird.y + game.bird.r;

    const pipeLeft = pipe.x;
    const pipeRight = pipe.x + pipe.width;
    const topBottom = pipe.topHeight + 25;
    const bottomTop = pipe.topHeight + pipe.gap - 25;

    const hitX = birdRight > pipeLeft && birdLeft < pipeRight;
    const hitTop = birdTop < topBottom;
    const hitBottom = birdBottom > bottomTop;

    if (hitX && (hitTop || hitBottom)) {
      endGame();
      return;
    }
  }

  game.pipes = game.pipes.filter(pipe => pipe.x + pipe.width > -20);

  if (game.bird.y - game.bird.r <= 0 || game.bird.y + game.bird.r >= canvas.height - 80) {
    endGame();
  }
}

function drawBackground() {
  const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
  grad.addColorStop(0, "#071f39");
  grad.addColorStop(0.45, "#0d4f7f");
  grad.addColorStop(1, "#0aa4c8");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#1d5e4d";
  ctx.fillRect(0, canvas.height - 80, canvas.width, 80);

  for (let x = 0; x < canvas.width; x += 40) {
    ctx.fillStyle = "#347d66";
    ctx.beginPath();
    ctx.moveTo(x, canvas.height);
    ctx.lineTo(x + 18, canvas.height - 80);
    ctx.lineTo(x + 36, canvas.height);
    ctx.closePath();
    ctx.fill();
  }

  for (let i = 0; i < 12; i++) {
    const y = 20 + i * 24;
    ctx.strokeStyle = "rgba(255,255,255,0.08)";
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.bezierCurveTo(canvas.width * 0.2, y - 10, canvas.width * 0.7, y + 10, canvas.width, y);
    ctx.stroke();
  }
}

function drawPipe(pipe) {
  ctx.fillStyle = "#3fa86f";
  ctx.fillRect(pipe.x, 0, pipe.width, pipe.topHeight);
  ctx.fillRect(pipe.x, pipe.topHeight + pipe.gap, pipe.width, canvas.height - (pipe.topHeight + pipe.gap) - 80);

  ctx.fillStyle = "#2b7a4b";
  ctx.fillRect(pipe.x - 8, 0, pipe.width + 16, 18);
  ctx.fillRect(pipe.x - 8, pipe.topHeight + pipe.gap - 18, pipe.width + 16, 18);
}

function drawFish() {
  const selected = getSelectedFish();
  const f = game.bird;

  ctx.save();
  ctx.translate(f.x, f.y);
  ctx.rotate(f.rot);

  if (selected.kind === "shark") {
    ctx.fillStyle = "rgba(0,0,0,0.18)";
    ctx.beginPath();
    ctx.ellipse(0, 18, 30, 12, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = selected.body;
    ctx.beginPath();
    ctx.moveTo(-30, 0);
    ctx.quadraticCurveTo(-8, -22, 26, 0);
    ctx.quadraticCurveTo(-8, 22, -30, 0);
    ctx.fill();

    ctx.fillStyle = selected.fin;
    ctx.beginPath();
    ctx.moveTo(-2, -8);
    ctx.lineTo(14, -30);
    ctx.lineTo(20, -8);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = selected.fin;
    ctx.beginPath();
    ctx.moveTo(-6, 0);
    ctx.lineTo(-22, -26);
    ctx.lineTo(-18, 0);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = selected.accent;
    ctx.beginPath();
    ctx.moveTo(22, 0);
    ctx.lineTo(52, -12);
    ctx.lineTo(52, 12);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = "#111";
    ctx.beginPath();
    ctx.arc(10, -2, 4, 0, Math.PI * 2);
    ctx.fill();
  } else if (selected.kind === "dolphin") {
    ctx.fillStyle = "rgba(0,0,0,0.18)";
    ctx.beginPath();
    ctx.ellipse(0, 18, 32, 12, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = selected.body;
    ctx.beginPath();
    ctx.moveTo(-26, 0);
    ctx.quadraticCurveTo(0, -20, 28, 0);
    ctx.quadraticCurveTo(0, 22, -26, 0);
    ctx.fill();

    ctx.fillStyle = selected.fin;
    ctx.beginPath();
    ctx.moveTo(-2, -6);
    ctx.lineTo(12, -26);
    ctx.lineTo(20, -6);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = selected.fin;
    ctx.beginPath();
    ctx.moveTo(-4, 0);
    ctx.lineTo(12, -24);
    ctx.lineTo(18, 0);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = selected.accent;
    ctx.beginPath();
    ctx.moveTo(20, 0);
    ctx.lineTo(42, -10);
    ctx.lineTo(42, 10);
    ctx.closePath();
    ctx.fill();
  } else if (selected.kind === "moonfish") {
    ctx.fillStyle = "rgba(0,0,0,0.18)";
    ctx.beginPath();
    ctx.ellipse(0, 18, 30, 12, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = selected.body;
    ctx.beginPath();
    ctx.ellipse(0, 0, 34, 18, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = selected.accent;
    ctx.beginPath();
    ctx.arc(0, 0, 18, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = selected.body;
    ctx.beginPath();
    ctx.arc(5, 0, 12, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = selected.fin;
    ctx.beginPath();
    ctx.moveTo(-18, 0);
    ctx.lineTo(-42, -8);
    ctx.lineTo(-42, 8);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = selected.fin;
    ctx.beginPath();
    ctx.moveTo(-18, 0);
    ctx.lineTo(-44, -18);
    ctx.lineTo(-44, 18);
    ctx.closePath();
    ctx.fill();
  } else {
    ctx.fillStyle = "rgba(0,0,0,0.18)";
    ctx.beginPath();
    ctx.ellipse(0, 18, 28, 11, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = selected.body;
    ctx.beginPath();
    ctx.ellipse(0, 0, 34, 16, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = selected.fin;
    ctx.beginPath();
    ctx.moveTo(-4, -12);
    ctx.lineTo(18, -34);
    ctx.lineTo(22, -14);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = selected.accent;
    ctx.beginPath();
    ctx.moveTo(2, 12);
    ctx.lineTo(20, 34);
    ctx.lineTo(22, 12);
    ctx.closePath();
    ctx.fill();
  }

  ctx.restore();
}

function render() {
  drawBackground();
  for (const pipe of game.pipes) drawPipe(pipe);
  drawFish();
}

function loop(ts) {
  const dt = ts - (game.lastTime || ts);
  game.lastTime = ts;
  update(dt);
  render();
  requestAnimationFrame(loop);
}

document.getElementById("startBtn").addEventListener("click", function() {
  startGame();
});

document.addEventListener("keydown", function(e) {
  if (e.code === "Space") {
    e.preventDefault();
    flap();
  }
});

canvas.addEventListener("pointerdown", function() {
  flap();
});

resetGame();
requestAnimationFrame(loop);
</script>
'''

components.html(html, height=700, width=500)
