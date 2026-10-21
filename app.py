import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Fishy Dive", page_icon="🐠", layout="centered")
st.title("Fishy Dive")
st.caption("Chơi, kiếm điểm, mở khóa skin cá mới")

html = '''
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #061f39;
  }
  #game-shell {
    width: 430px;
    height: 620px;
    margin: 16px auto;
    position: relative;
    border: 4px solid #123d5d;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 12px 25px rgba(0,0,0,0.25);
    background: linear-gradient(#061f39, #0d4f7f 50%, #0aa4c8);
  }
  #scoreText {
    position: absolute;
    top: 10px;
    left: 0;
    width: 100%;
    text-align: center;
    color: white;
    font-size: 34px;
    font-weight: bold;
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
    backdrop-filter: blur(3px);
    z-index: 10;
  }
  .panel.hidden { display: none; }
  .panel-box {
    width: 82%;
    background: rgba(18, 38, 60, 0.9);
    border: 2px solid rgba(255,255,255,0.2);
    border-radius: 16px;
    padding: 24px 20px;
    color: white;
    text-align: center;
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
  .score-badge {
    margin-bottom: 18px;
    font-size: 16px;
    font-weight: bold;
    color: #dff7ff;
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
    transition: all 0.2s ease;
  }
  button:hover {
    transform: translateY(-1px);
    filter: brightness(1.05);
  }
  .primary {
    background: linear-gradient(#5ad0ff, #2aa6df);
    color: #03283d;
  }
  .secondary {
    background: linear-gradient(#ffcd67, #f7a33a);
    color: #4d2a00;
  }
  .shop-list {
    display: grid;
    gap: 12px;
    max-height: 340px;
    overflow-y: auto;
    margin-top: 12px;
  }
  .fish-card {
    display: grid;
    grid-template-columns: 60px 1fr auto;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 8px 10px;
    text-align: left;
  }
  .fish-mini {
    width: 52px;
    height: 28px;
    border-radius: 50%;
    position: relative;
    background: var(--fish-color);
  }
  .fish-mini::before {
    content: "";
    position: absolute;
    right: -12px;
    top: 50%;
    transform: translateY(-50%);
    width: 14px;
    height: 14px;
    background: var(--fish-color);
    clip-path: polygon(0 50%, 100% 0, 100% 100%);
  }
  .fish-mini::after {
    content: "";
    position: absolute;
    left: 10px;
    top: 8px;
    width: 5px;
    height: 5px;
    background: #111;
    border-radius: 50%;
  }
  .fish-name { font-weight: bold; }
  .fish-meta { font-size: 12px; opacity: 0.8; }
  .shop-action {
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: bold;
    cursor: pointer;
  }
  .shop-action.buy {
    background: linear-gradient(#ffe785, #ffbf47);
    color: #4a2b00;
  }
  .shop-action.use {
    background: linear-gradient(#94f7c9, #46d89e);
    color: #0d3d2e;
  }
  .small-text { font-size: 12px; opacity: 0.8; }
  .row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }
</style>

<div id="game-shell">
  <div id="scoreText">0</div>
  <canvas id="gameCanvas" width="430" height="620"></canvas>
  <audio id="bgm" loop>
    <source src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_6c2d4d1f8f.mp3?filename=gentle-ambient-ambient-114355.mp3" type="audio/mpeg">
  </audio>

  <div id="startScreen" class="panel">
    <div class="panel-box">
      <div class="title">Fishy Dive</div>
      <div class="subtitle">Chơi để kiếm điểm, mua cá mới và đổi skin</div>
      <div class="score-badge">Điểm của bạn: <span id="homePoints">0</span></div>
      <div class="button-row">
        <button id="startBtn" class="primary">Chơi</button>
        <button id="shopBtn" class="secondary">Cửa hàng</button>
      </div>
    </div>
  </div>

  <div id="shopScreen" class="panel hidden">
    <div class="panel-box">
      <div class="title" style="font-size:28px;">Cửa hàng cá</div>
      <div class="row">
        <div class="small-text">Điểm hiện có</div>
        <div class="small-text" id="shopPoints">0</div>
      </div>
      <div id="shopList" class="shop-list"></div>
      <div class="button-row" style="margin-top:16px;">
        <button id="backToMenuBtn" class="secondary">Quay lại</button>
      </div>
    </div>
  </div>

  <div id="gameOverScreen" class="panel hidden">
    <div class="panel-box">
      <div class="title" style="font-size:28px;">Game Over</div>
      <div class="subtitle" id="gameOverMessage">Bạn đã kiếm được 0 điểm</div>
      <div class="button-row">
        <button id="playAgainBtn" class="primary">Chơi lại</button>
        <button id="shopFromGameBtn" class="secondary">Cửa hàng</button>
      </div>
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreText = document.getElementById("scoreText");
const startScreen = document.getElementById("startScreen");
const shopScreen = document.getElementById("shopScreen");
const gameOverScreen = document.getElementById("gameOverScreen");
const homePoints = document.getElementById("homePoints");
const shopPoints = document.getElementById("shopPoints");
const shopList = document.getElementById("shopList");
const gameOverMessage = document.getElementById("gameOverMessage");
const bgm = document.getElementById("bgm");

function playMusic() {
  if (bgm) {
    bgm.volume = 0.25;
    bgm.play().catch(() => {});
  }
}

const fishCatalog = [
  { id: "classic", name: "Cá xanh", price: 0, kind: "classic", body: "#4ec0d8", fin: "#f7b152", accent: "#f4805d", shadow: "#1a2d3a" },
  { id: "coral", name: "Cá san hô", price: 12, kind: "classic", body: "#ff8e5d", fin: "#ffd166", accent: "#ff6b6b", shadow: "#7a3a2c" },
  { id: "moon", name: "Cá trăng", price: 20, kind: "classic", body: "#c4c7ff", fin: "#a7d8ff", accent: "#f7d6e0", shadow: "#3d4a8d" },
  { id: "forest", name: "Cá rừng", price: 28, kind: "classic", body: "#59d38a", fin: "#a4efb7", accent: "#fbdc7a", shadow: "#215a42" },
  { id: "royal", name: "Cá hoàng gia", price: 40, kind: "classic", body: "#d7b3ff", fin: "#ffd86b", accent: "#f39bff", shadow: "#563c79" },
  { id: "neon", name: "Cá neon", price: 35, kind: "classic", body: "#45f0d5", fin: "#ffeb66", accent: "#ff7eea", shadow: "#1f5e6a" },
  { id: "whale", name: "Cá voi", price: 500, kind: "whale", body: "#92c7d2", fin: "#dfeaf7", accent: "#6aa7b5", shadow: "#2d4d59" },
  { id: "shark", name: "Cá mập", price: 420, kind: "shark", body: "#8c9aa3", fin: "#d8dee5", accent: "#4f6570", shadow: "#2d3942" },
  { id: "dolphin", name: "Cá heo", price: 200, kind: "dolphin", body: "#5db8d7", fin: "#f4d35e", accent: "#e9f7ff", shadow: "#234c63" },
  { id: "moonfish", name: "Cá mặt trăng", price: 150, kind: "moonfish", body: "#f6e6ff", fin: "#ffe59a", accent: "#d8c0ff", shadow: "#6f5d90" }
];

const storage = {
  keyPoints: "fishy_points",
  keyUnlocked: "fishy_unlocked",
  keySelected: "fishy_selected"
};

const state = {
  points: Number(localStorage.getItem(storage.keyPoints) || 0),
  unlocked: JSON.parse(localStorage.getItem(storage.keyUnlocked) || '["classic"]'),
  selectedFish: localStorage.getItem(storage.keySelected) || "classic",
  screen: "start"
};

function saveProgress() {
  localStorage.setItem(storage.keyPoints, String(state.points));
  localStorage.setItem(storage.keyUnlocked, JSON.stringify(state.unlocked));
  localStorage.setItem(storage.keySelected, state.selectedFish);
}

function getSelectedFish() {
  return fishCatalog.find(f => f.id === state.selectedFish) || fishCatalog[0];
}

function updatePointDisplays() {
  homePoints.textContent = state.points;
  shopPoints.textContent = state.points;
}

function showScreen(name) {
  state.screen = name;
  startScreen.classList.toggle("hidden", name !== "start");
  shopScreen.classList.toggle("hidden", name !== "shop");
  gameOverScreen.classList.toggle("hidden", name !== "gameover");
  updatePointDisplays();
}

function renderShop() {
  shopList.innerHTML = "";
  for (const fish of fishCatalog) {
    const unlocked = state.unlocked.includes(fish.id);
    const selected = state.selectedFish === fish.id;

    const card = document.createElement("div");
    card.className = "fish-card";
    card.style.setProperty("--fish-color", fish.body);

    const fishView = document.createElement("div");
    fishView.className = "fish-mini";
    fishView.style.setProperty("--fish-color", fish.body);

    const textBlock = document.createElement("div");
    textBlock.innerHTML = `
      <div class="fish-name">${fish.name}</div>
      <div class="fish-meta">${unlocked ? (selected ? "Đang sử dụng" : "Đã mua") : `${fish.price} điểm`}</div>
    `;

    const actionBtn = document.createElement("button");
    actionBtn.className = "shop-action " + (unlocked ? "use" : "buy");
    actionBtn.textContent = unlocked ? (selected ? "Đang dùng" : "Dùng") : "Mua";

    actionBtn.addEventListener("click", () => {
      if (!unlocked) {
        if (state.points >= fish.price) {
          state.points -= fish.price;
          state.unlocked.push(fish.id);
          saveProgress();
          renderShop();
          updatePointDisplays();
        }
        return;
      }

      state.selectedFish = fish.id;
      saveProgress();
      renderShop();
    });

    card.appendChild(fishView);
    card.appendChild(textBlock);
    card.appendChild(actionBtn);
    shopList.appendChild(card);
  }
}

document.getElementById("startBtn").addEventListener("click", () => {
  showScreen("game");
  startGame();
});

document.getElementById("shopBtn").addEventListener("click", () => {
  renderShop();
  showScreen("shop");
});

document.getElementById("backToMenuBtn").addEventListener("click", () => {
  showScreen("start");
});

document.getElementById("shopFromGameBtn").addEventListener("click", () => {
  renderShop();
  showScreen("shop");
});

document.getElementById("playAgainBtn").addEventListener("click", () => {
  showScreen("game");
  startGame();
});

const game = {
  running: false,
  over: false,
  score: 0,
  best: 0,
  lastTime: 0,
  spawnTimer: 0,
  fish: { x: 110, y: 310, r: 18, vy: 0, rot: 0 },
  rocks: [],
  bubbles: [],
  seaweeds: [],
  tinyFish: []
};

function createBackgroundLife() {
  game.seaweeds = [];
  game.tinyFish = [];
  for (let i = 0; i < 18; i++) {
    game.seaweeds.push({
      x: Math.random() * canvas.width,
      y: canvas.height - 80 + Math.random() * 20,
      h: 30 + Math.random() * 80,
      speed: 0.5 + Math.random() * 1.2,
      sway: Math.random() * Math.PI * 2
    });
  }
  for (let i = 0; i < 7; i++) {
    game.tinyFish.push({
      x: Math.random() * canvas.width,
      y: 80 + Math.random() * (canvas.height - 180),
      size: 8 + Math.random() * 12,
      speed: 0.3 + Math.random() * 0.8,
      dir: Math.random() > 0.5 ? 1 : -1,
      phase: Math.random() * Math.PI * 2
    });
  }
}

function resetGame() {
  game.running = false;
  game.over = false;
  game.score = 0;
  game.spawnTimer = 0;
  game.rocks = [];
  game.bubbles = [];
  game.fish.x = 110;
  game.fish.y = 310;
  game.fish.vy = 0;
  game.fish.rot = 0;
  scoreText.textContent = "0";
}

function startGame() {
  resetGame();
  game.running = true;
  game.over = false;
  game.fish.vy = -8.5;
  playMusic();
}

function endGame() {
  game.running = false;`*

