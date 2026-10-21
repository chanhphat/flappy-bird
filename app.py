import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Fishy Dive", page_icon="🐠", layout="centered")
st.title("Fishy Dive")
st.caption("Nhấn Space hoặc click chuột để bơi")

html = """
<div id="game-wrapper" style="display:flex; justify-content:center; align-items:center; margin-top:10px;">
  <div id="game" style="
      position:relative;
      width:430px;
      height:620px;
      border:4px solid #123d5d;
      border-radius:14px;
      overflow:hidden;
      background:linear-gradient(#061f39, #0d4f7f 50%, #0aa4c8);
      box-shadow:0 12px 25px rgba(0, 0, 0, 0.25);
  ">
    <div id="scoreText" style="
      position:absolute; top:10px; left:0; width:100%;
      text-align:center; color:white; font-weight:bold; font-size:34px;
      text-shadow:2px 2px 0 #000; pointer-events:none;
    ">0</div>

    <canvas id="gameCanvas" width="430" height="620"></canvas>

    <div id="overlay" style="
      position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
      background:rgba(0,0,0,0.35); color:white; padding:18px 22px;
      border-radius:12px; text-align:center; font-size:21px; line-height:1.5;
      min-width:220px; box-shadow:0 8px 20px rgba(0,0,0,0.15);
    ">Nhấn Space / Click để chơi</div>
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
  bubbles: []
};

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
  game.running = false;
  game.over = true;
  game.best = Math.max(game.best, game.score);
  overlay.style.display = "block";
  overlay.innerHTML = "Game Over!<br>Điểm: " + game.score + "<br>Best: " + game.best + "<br><br>Nhấn Space / Click để chơi lại";
}

function flap() {
  if (!game.running && !game.over) {
    startGame();
  } else if (game.running) {
    game.fish.vy = -8.5;
  } else {
    resetGame();
    startGame();
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

function spawnRock() {
  const gap = 170;
  const minTop = 70;
  const maxTop = canvas.height - 80 - gap - minTop;
  const topHeight = minTop + Math.random() * maxTop;

  game.rocks.push({
    x: canvas.width + 20,
    width: 72,
    gap: gap,
    topHeight: topHeight,
    passed: false
  });
}

function update(dt) {
  if (!game.running) return;

  game.fish.vy += 0.42 * dt * 0.06;
  game.fish.y += game.fish.vy * dt * 0.06;
  game.fish.rot = Math.max(-1.25, Math.min(1.5, game.fish.vy / 10));

  game.spawnTimer += dt;
  if (game.spawnTimer >= 1500) {
    spawnRock();
    game.spawnTimer = 0;
  }

  if (Math.random() < 0.08) addBubble();

  for (let i = game.bubbles.length - 1; i >= 0; i--) {
    const b = game.bubbles[i];
    b.y -= b.speed * dt * 0.06;
    b.x += Math.sin(b.y * 0.04) * 0.35;
    if (b.y + b.r < 0) game.bubbles.splice(i, 1);
  }

  for (const rock of game.rocks) {
    rock.x -= 2.3 * dt * 0.06;

    if (!rock.passed && rock.x + rock.width < game.fish.x) {
      rock.passed = true;
      game.score += 1;
      scoreText.textContent = game.score;
    }

    const fishLeft = game.fish.x - game.fish.r;
    const fishRight = game.fish.x + game.fish.r;
    const fishTop = game.fish.y - game.fish.r;
    const fishBottom = game.fish.y + game.fish.r;

    const rockLeft = rock.x;
    const rockRight = rock.x + rock.width;
    const topBottom = rock.topHeight;
    const bottomTop = rock.topHeight + rock.gap;

    const hitX = fishRight > rockLeft && fishLeft < rockRight;
    const hitTop = fishTop < topBottom;
    const hitBottom = fishBottom > bottomTop;

    if (hitX && (hitTop || hitBottom)) {
      endGame();
    }
  }

  game.rocks = game.rocks.filter(r => r.x + r.width > -20);

  if (game.fish.y - game.fish.r <= 0 || game.fish.y + game.fish.r >= canvas.height - 80) {
    endGame();
  }
}

function drawSeaweed(x, y, scale) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);

  ctx.strokeStyle = "#18d38a";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(0, 0);

  for (let i = 0; i < 5; i++) {
    const px = (i % 2 === 0 ? -8 : 8) * (1 + i * 0.25);
    const py = -20 - i * 12;
    ctx.quadraticCurveTo(px, py, 0, -30 - i * 14);
  }
  ctx.stroke();
  ctx.restore();
}

function drawBackground() {
  const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
  grad.addColorStop(0, "#071f39");
  grad.addColorStop(0.5, "#0d4f7f");
  grad.addColorStop(1, "#0aa4c8");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "rgba(255,255,255,0.09)";
  ctx.lineWidth = 1;
  for (let y = 30; y < canvas.height; y += 30) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.bezierCurveTo(canvas.width * 0.2, y - 12, canvas.width * 0.7, y + 12, canvas.width, y);
    ctx.stroke();
  }

  for (let x = 0; x < canvas.width; x += 26) {
    drawSeaweed(x, canvas.height - 80, 1 + (x % 3) * 0.32);
  }

  ctx.fillStyle = "#1d5e4d";
  ctx.fillRect(0, canvas.height - 80, canvas.width, 80);

  ctx.fillStyle = "#347d66";
  for (let x = 0; x < canvas.width; x += 38) {
    ctx.beginPath();
    ctx.moveTo(x, canvas.height);
    ctx.lineTo(x + 18, canvas.height - 80);
    ctx.lineTo(x + 36, canvas.height);
    ctx.closePath();
    ctx.fill();
  }

  for (const b of game.bubbles) {
    ctx.beginPath();
    ctx.fillStyle = "rgba(255,255,255,0.3)";
    ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawFish() {
  const f = game.fish;

  ctx.save();
  ctx.translate(f.x, f.y);
  ctx.rotate(f.rot);

  // bóng dưới cá
  ctx.fillStyle = "rgba(0,0,0,0.18)";
  ctx.beginPath();
  ctx.ellipse(0, 18, 28, 11, 0, 0, Math.PI * 2);
  ctx.fill();

  // thân cá dẹp
  ctx.fillStyle = "#4ec0d8";
  ctx.beginPath();
  ctx.ellipse(0, 0, 34, 16, 0, 0, Math.PI * 2);
  ctx.fill();

  // sáng trên thân*

