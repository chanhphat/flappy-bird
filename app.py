cat > app.py <<'PY'
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

    const rockLeft = rock.x + 12;
    const rockRight = rock.x + rock.width - 12;
    const topBottom = rock.topHeight + 22;
    const bottomTop = rock.topHeight + rock.gap - 22;

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

  for (const s of game.seaweeds) {
    s.sway += 0.04 * s.speed;
  }

  for (const f of game.tinyFish) {
    f.x += f.speed * f.dir * 0.5;
    f.y += Math.sin(f.x * 0.04 + f.phase) * 0.25;

    if (f.x > canvas.width + 30) f.x = -30;
    if (f.x < -30) f.x = canvas.width + 30;
  }
}

function drawBackground() {
  const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
  grad.addColorStop(0, "#071f39");
  grad.addColorStop(0.45, "#0d4f7f");
  grad.addColorStop(1, "#0aa4c8");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "rgba(255,255,255,0.06)";
  ctx.lineWidth = 1;
  for (let y = 30; y < canvas.height; y += 30) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.bezierCurveTo(canvas.width * 0.2, y - 12, canvas.width * 0.7, y + 12, canvas.width, y);
    ctx.stroke();
  }

  for (const f of game.tinyFish) {
    ctx.save();
    ctx.translate(f.x, f.y);
    ctx.scale(f.dir, 1);

    ctx.fillStyle = "rgba(120, 220, 255, 0.7)";
    ctx.beginPath();
    ctx.ellipse(0, 0, f.size, f.size * 0.52, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "rgba(255,255,255,0.7)";
    ctx.beginPath();
    ctx.arc(f.size * 0.3, -1, f.size * 0.15, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#ff7a5c";
    ctx.beginPath();
    ctx.moveTo(-f.size, 0);
    ctx.lineTo(-f.size - 8, -f.size * 0.5);
    ctx.lineTo(-f.size - 8, f.size * 0.5);
    ctx.closePath();
    ctx.fill();

    ctx.restore();
  }

  for (const s of game.seaweeds) {
    ctx.save();
    ctx.translate(s.x, s.y);

    const sway = Math.sin(s.sway) * 10;
    ctx.strokeStyle = "#1ed38b";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(0, 0);

    let px = 0;
    let py = 0;
    for (let i = 1; i <= 6; i++) {
      px = (i % 2 === 0 ? -1 : 1) * (6 + i * 2) + sway * 0.2;
      py = -s.h * (i / 7);
      ctx.quadraticCurveTo(px, py, 0, -s.h * (i / 6));
    }

    ctx.stroke();
    ctx.restore();
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

  ctx.fillStyle = "rgba(0,0,0,0.18)";
  ctx.beginPath();
  ctx.ellipse(0, 18, 28, 11, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#4ec0d8";
  ctx.beginPath();
  ctx.ellipse(0, 0, 34, 16, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "rgba(255,255,255,0.25)";
  ctx.beginPath();
  ctx.ellipse(-6, -2, 18, 8, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#1a2d3a";
  ctx.beginPath();
  ctx.ellipse(-2, 0, 10, 12, 0.1, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = "#1b2d3a";
  ctx.lineWidth = 2;
  for (let i = -18; i <= 18; i += 7) {
    ctx.beginPath();
    ctx.moveTo(i - 2, -9);
    ctx.quadraticCurveTo(i + 8, 0, i + 3, 11);
    ctx.stroke();
  }

  ctx.fillStyle = "#1a2430";
  ctx.beginPath();
  ctx.ellipse(12, 2, 6, 8, 0.1, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#f7b152";
  ctx.beginPath();
  ctx.moveTo(-4, -12);
  ctx.lineTo(18, -34);
  ctx.lineTo(22, -14);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#f4805d";
  ctx.beginPath();
  ctx.moveTo(2, 12);
  ctx.lineTo(20, 34);
  ctx.lineTo(22, 12);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#f9c76d";
  ctx.beginPath();
  ctx.moveTo(-3, -10);
  ctx.lineTo(-18, -30);
  ctx.lineTo(8, -18);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#ff9b64";
  ctx.beginPath();
  ctx.moveTo(3, 10);
  ctx.lineTo(-18, 30);
  ctx.lineTo(10, 16);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#f56d4d";
  ctx.beginPath();
  ctx.moveTo(-30, 0);
  ctx.lineTo(-56, -18);
  ctx.lineTo(-56, 0);
  ctx.lineTo(-56, 18);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#ff8f67";
  ctx.beginPath();
  ctx.moveTo(-27, 0);
  ctx.lineTo(-46, -9);
  ctx.lineTo(-46, 9);
  ctx.closePath();
  ctx.fill();

  ctx.fillStyle = "#fff";
  ctx.beginPath();
  ctx.arc(15, -5, 6.5, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#111";
  ctx.beginPath();
  ctx.arc(17, -5, 2.5, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "rgba(255,255,255,0.8)";
  ctx.beginPath();
  ctx.arc(13, -7, 1.4, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = "#111";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(22, 0);
  ctx.lineTo(30, 4);
  ctx.stroke();

  ctx.restore();
}

function drawRock(rock) {
  const x = rock.x;
  const width = rock.width;
  const topHeight = rock.topHeight;
  const gap = rock.gap;

  ctx.fillStyle = "#7a8d8d";
  ctx.beginPath();
  ctx.moveTo(x, 0);
  ctx.lineTo(x + width, 0);
  ctx.lineTo(x + width + 8, topHeight - 18);
  ctx.lineTo(x + width * 0.6, topHeight + 10);
  ctx.lineTo(x + width * 0.3, topHeight - 6);
  ctx.lineTo(x - 4, topHeight - 10);
  ctx.closePath();
  ctx.fill();

  const bottomY = topHeight + gap;
  ctx.fillStyle = "#7a8d8d";
  ctx.beginPath();
  ctx.moveTo(x, canvas.height - 80);
  ctx.lineTo(x + width, canvas.height - 80);
  ctx.lineTo(x + width + 10, bottomY + 18);
  ctx.lineTo(x + width * 0.7, bottomY + 6);
  ctx.lineTo(x + width * 0.4, bottomY + 8);
  ctx.lineTo(x - 4, bottomY + 18);
  ctx.closePath();
  ctx.fill();
}

function render() {
  drawBackground();
  for (const rock of game.rocks) drawRock(rock);
  drawFish();
}

function loop(ts) {
  const dt = ts - (game.lastTime || ts);
  game.lastTime = ts;

  update(dt);
  render();

  requestAnimationFrame(loop);
}

document.addEventListener("keydown", (e) => {
  if (e.code === "Space") {
    e.preventDefault();
    flap();
  }
});

canvas.addEventListener("pointerdown", () => flap());

createBackgroundLife();
resetGame();
requestAnimationFrame(loop);
</script>
"""

components.html(html, height=700, width=500)
PY
