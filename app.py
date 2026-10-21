import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Fishy Dive", page_icon="🐠", layout="centered")
st.title("Fishy Dive")
st.caption("Nhấn Space hoặc click chuột để bơi")

html = '''
<style>
  * { box-sizing: border-box; }
  body { margin: 0; }
  #game-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 12px;
  }
  #game {
    position: relative;
    width: 430px;
    height: 620px;
    border: 4px solid #123d5d;
    border-radius: 14px;
    overflow: hidden;
    background: linear-gradient(#061f39, #0d4f7f 50%, #0aa4c8);
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.25);
  }
  canvas {
    display: block;
    width: 100%;
    height: 100%;
  }
  #overlay {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0, 0, 0, 0.35);
    color: white;
    padding: 18px 22px;
    border-radius: 12px;
    text-align: center;
    font-size: 21px;
    line-height: 1.5;
    min-width: 220px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  }
  .hud {
    position: absolute;
    top: 10px;
    left: 0;
    width: 100%;
    text-align: center;
    color: white;
    font-weight: bold;
    font-size: 34px;
    text-shadow: 2px 2px 0 #000;
    pointer-events: none;
  }
</style>

<div id="game-wrap">
  <div id="game">
    <div class="hud" id="scoreText">0</div>
    <canvas id="gameCanvas" width="430" height="620"></canvas>
    <div id="overlay">Nhấn Space / Click để chơi</div>
  </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const overlay = document.getElementById("overlay");
const scoreText = document.getElementById("scoreText");

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

  for (let i = 0; i < 16; i++) {
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

function addBubble() {
  game.bubbles.push({
    x: Math.random() * canvas.width,
    y: canvas.height + 10,
    r: 4 + Math.random() * 8,
    speed: 0.8 + Math.random() * 1.4
  });
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
  overlay.style.display = "block";
  overlay.innerHTML = "Nhấn Space / Click để chơi";
}

function startGame() {
  if (game.over) resetGame();
  game.running = true;
  game.over = false;
  game.fish.vy = -8.5;
  overlay.style.display = "none";
}

function endGame() {
  game.running*
