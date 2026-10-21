import streamlit as st

st.set_page_config(page_title="Fishy Dive", page_icon="🐠", layout="centered")
st.title("Fishy Dive")
st.caption("Nhấn Space hoặc click chuột để bơi qua các rạn đá")

html = """
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
        background: linear-gradient(#061f39, #0d4f7f 45%, #1197c1);
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

    const state = {
        playing: false,
        gameOver: false,
        score: 0,
        best: 0,
        lastTime: 0,
        spawnTimer: 0,
        fish: {
            x: 110,
            y: 310,
            r: 18,
            vy: 0,
            rotation: 0
        },
        pipes: [],
        bubbles: []
    };

    function addBubble() {
        state.bubbles.push({
            x: Math.random() * canvas.width,
            y: canvas.height + 10,
            r: 4 + Math.random() * 8,
            speed: 0.8 + Math.random() * 1.4
        });
    }

    function updateScore() {
        scoreText.textContent = state.score;
    }

    function resetGame() {
        state.playing = false;
        state.gameOver = false;
        state.score = 0;
        state.spawnTimer = 0;
        state.pipes = [];
        state.bubbles = [];
        state.fish.x = 110;
        state.fish.y = 310;
        state.fish.vy = 0;
        state.fish.rotation = 0;
        updateScore();
        overlay.style.display = "block";
        overlay.innerHTML = "Nhấn Space / Click để chơi";
    }

    function startGame() {
        if (state.gameOver) {
            resetGame();
        }
        state.playing = true;
        state.gameOver = false;
        state.fish.vy = -8.5;
        overlay.style.display = "none";
    }

    function gameOver() {
        state.playing = false;
        state.gameOver = true;
        state.best = Math.max(state.best, state.score);
        overlay.style.display = "block";
        overlay.innerHTML = "Game Over!<br>Điểm: " + state.score + "<br>Best: " + state.best + "<br><br>Nhấn Space / Click để chơi lại";
    }

    function flap() {
        if (!state.playing && !state.gameOver) {
            startGame();
        } else if (state.playing) {
            state.fish.vy = -8.5;
        } else {
            resetGame();
            startGame();
        }
    }

    function spawnPipe() {
        const gap = 170;
        const minTop = 70;
        const maxTop = canvas.height - 80 - gap - minTop;
        const topHeight = minTop + Math.random() * maxTop;

        state.pipes.push({
            x: canvas.width + 20,
            width: 72,
            gap: gap,
            topHeight: topHeight,
            passed: false
        });
    }

    function update(dt) {
        if (!state.playing) return;

        state.fish.vy += 0.42 * dt * 0.06;
        state.fish.y += state.fish.vy * dt * 0.06;
        state.fish.rotation = Math.max(-1.25, Math.min(1.5, state.fish.vy / 10));

        state.spawnTimer += dt;
        if (state.spawnTimer >= 1500) {
            spawnPipe();
            state.spawnTimer = 0;
        }

        if (Math.random() < 0.08) {
            addBubble();
        }

        for (let i = state.bubbles.length - 1; i >= 0; i--) {
            const b = state.bubbles[i];
            b.y -= b.speed * dt * 0.06;
            b.x += Math.sin(b.y * 0.04) * 0.35;
            if (b.y + b.r < 0) {
                state.bubbles.splice(i, 1);
            }
        }

        for (const pipe of state.pipes) {
            pipe.x -= 2.3 * dt * 0.06;

            if (!pipe.passed && pipe.x + pipe.width < state.fish.x) {
                pipe.passed = true;
                state.score += 1;
                updateScore();
            }

            const fishLeft = state.fish.x - state.fish.r;
            const fishRight = state.fish.x + state.fish.r;
            const fishTop = state.fish.y - state.fish.r;
            const fishBottom = state.fish.y + state.fish.r;

            const pipeLeft = pipe.x;
            const pipeRight = pipe.x + pipe.width;
            const topBottom = pipe.topHeight;
            const bottomTop = pipe.topHeight + pipe.gap;

            const hitX = fishRight > pipeLeft && fishLeft < pipeRight;
            const hitTop = fishTop < topBottom;
            const hitBottom = fishBottom > bottomTop;

            if (hitX && (hitTop || hitBottom)) {
                gameOver();
            }
        }

        state.pipes = state.pipes.filter(pipe => pipe.x + pipe.width > -20);

        if (state.fish.y - state.fish.r <= 0 || state.fish.y + state.fish.r >= canvas.height - 80) {
            gameOver();
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

        for (const b of state.bubbles) {
            ctx.beginPath();
            ctx.fillStyle = "rgba(255,255,255,0.3)";
            ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function drawFish() {
        const fish = state.fish;

        ctx.save();
        ctx.translate(fish.x, fish.y);
        ctx.rotate(fish.rotation);

        // Thân cá lóc kiểu mạnh mẽ, khỏe khoắn
        ctx.fillStyle = "#2db07b";
        ctx.beginPath();
        ctx.ellipse(0, 0, 24, 16, 0, 0, Math.PI * 2);
        ctx.fill();

        // Vảy cá
        for (let i = -12; i <= 12; i += 6) {
            ctx.fillStyle = i % 2 === 0 ? "#38c789" : "#27a86b";
            ctx.beginPath();
            ctx.ellipse(i, 0, 5, 8, 0, 0, Math.PI * 2);
            ctx.fill();
        }

        // Đuôi cá
        ctx.fillStyle = "#f36d5b";
        ctx.beginPath();
        ctx.moveTo(-24, 0);
        ctx.lineTo(-44, -16);
        ctx.lineTo(-44, 16);
        ctx.closePath();
        ctx.fill();

        // Vây lưng
        ctx.fillStyle = "#ffb24c";
        ctx.beginPath();
        ctx.moveTo(0, -10);
        ctx.lineTo(18, -28);
        ctx.lineTo(18, -8);
        ctx.closePath();
        ctx.fill();

        // Vây bụng
        ctx.fillStyle = "#ff8f5b";
        ctx.beginPath();
        ctx.moveTo(2, 10);
        ctx.lineTo(18, 28);
        ctx.lineTo(16, 8);
        ctx.closePath();
        ctx.fill();

        // Vây đuôi phụ
        ctx.fillStyle = "#ff9a6b";
        ctx.beginPath();
        ctx.moveTo(-30, 0);
        ctx.lineTo(-50, -8);
        ctx.lineTo(-50, 8);
        ctx.closePath();
        ctx.fill();

        // Mắt
        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(10, -5, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#111111";
        ctx.beginPath();
        ctx.arc(12, -5, 2.4, 0, Math.PI * 2);
        ctx.fill();

        // Miệng
        ctx.strokeStyle = "#1c1c1c";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(18, 0);
        ctx.lineTo(27, 4);
        ctx.stroke();

        // Nếp gân rất đẹp
        ctx.strokeStyle = "rgba(255,255,255,0.25)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(4, -5);
        ctx.lineTo(14, -8);
        ctx.moveTo(5, 6);
        ctx.lineTo(15, 10);
        ctx.stroke();

        ctx.restore();
    }

    function drawPipe(pipe) {
        const x = pipe.x;*
import streamlit as st

st.set_page_config(page_title="Fishy Dive", page_icon="🐠", layout="centered")
st.title("Fishy Dive")
st.caption("Nhấn Space hoặc click chuột để bơi qua các rạn đá")

html = """
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
        background: linear-gradient(#061f39, #0d4f7f 45%, #1197c1);
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

    const state = {
        playing: false,
        gameOver: false,
        score: 0,
        best: 0,
        lastTime: 0,
        spawnTimer: 0,
        fish: {
            x: 110,
            y: 310,
            r: 18,
            vy: 0,
            rotation: 0
        },
        pipes: [],
        bubbles: []
    };

    function addBubble() {
        state.bubbles.push({
            x: Math.random() * canvas.width,
            y: canvas.height + 10,
            r: 4 + Math.random() * 8,
            speed: 0.8 + Math.random() * 1.4
        });
    }

    function updateScore() {
        scoreText.textContent = state.score;
    }

    function resetGame() {
        state.playing = false;
        state.gameOver = false;
        state.score = 0;
        state.spawnTimer = 0;
        state.pipes = [];
        state.bubbles = [];
        state.fish.x = 110;
        state.fish.y = 310;
        state.fish.vy = 0;
        state.fish.rotation = 0;
        updateScore();
        overlay.style.display = "block";
        overlay.innerHTML = "Nhấn Space / Click để chơi";
    }

    function startGame() {
        if (state.gameOver) {
            resetGame();
        }
        state.playing = true;
        state.gameOver = false;
        state.fish.vy = -8.5;
        overlay.style.display = "none";
    }

    function gameOver() {
        state.playing = false;
        state.gameOver = true;
        state.best = Math.max(state.best, state.score);
        overlay.style.display = "block";
        overlay.innerHTML = "Game Over!<br>Điểm: " + state.score + "<br>Best: " + state.best + "<br><br>Nhấn Space / Click để chơi lại";
    }

    function flap() {
        if (!state.playing && !state.gameOver) {
            startGame();
        } else if (state.playing) {
            state.fish.vy = -8.5;
        } else {
            resetGame();
            startGame();
        }
    }

    function spawnPipe() {
        const gap = 170;
        const minTop = 70;
        const maxTop = canvas.height - 80 - gap - minTop;
        const topHeight = minTop + Math.random() * maxTop;

        state.pipes.push({
            x: canvas.width + 20,
            width: 72,
            gap: gap,
            topHeight: topHeight,
            passed: false
        });
    }

    function update(dt) {
        if (!state.playing) return;

        state.fish.vy += 0.42 * dt * 0.06;
        state.fish.y += state.fish.vy * dt * 0.06;
        state.fish.rotation = Math.max(-1.25, Math.min(1.5, state.fish.vy / 10));

        state.spawnTimer += dt;
        if (state.spawnTimer >= 1500) {
            spawnPipe();
            state.spawnTimer = 0;
        }

        if (Math.random() < 0.08) {
            addBubble();
        }

        for (let i = state.bubbles.length - 1; i >= 0; i--) {
            const b = state.bubbles[i];
            b.y -= b.speed * dt * 0.06;
            b.x += Math.sin(b.y * 0.04) * 0.35;
            if (b.y + b.r < 0) {
                state.bubbles.splice(i, 1);
            }
        }

        for (const pipe of state.pipes) {
            pipe.x -= 2.3 * dt * 0.06;

            if (!pipe.passed && pipe.x + pipe.width < state.fish.x) {
                pipe.passed = true;
                state.score += 1;
                updateScore();
            }

            const fishLeft = state.fish.x - state.fish.r;
            const fishRight = state.fish.x + state.fish.r;
            const fishTop = state.fish.y - state.fish.r;
            const fishBottom = state.fish.y + state.fish.r;

            const pipeLeft = pipe.x;
            const pipeRight = pipe.x + pipe.width;
            const topBottom = pipe.topHeight;
            const bottomTop = pipe.topHeight + pipe.gap;

            const hitX = fishRight > pipeLeft && fishLeft < pipeRight;
            const hitTop = fishTop < topBottom;
            const hitBottom = fishBottom > bottomTop;

            if (hitX && (hitTop || hitBottom)) {
                gameOver();
            }
        }

        state.pipes = state.pipes.filter(pipe => pipe.x + pipe.width > -20);

        if (state.fish.y - state.fish.r <= 0 || state.fish.y + state.fish.r >= canvas.height - 80) {
            gameOver();
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

        for (const b of state.bubbles) {
            ctx.beginPath();
            ctx.fillStyle = "rgba(255,255,255,0.3)";
            ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function drawFish() {
        const fish = state.fish;

        ctx.save();
        ctx.translate(fish.x, fish.y);
        ctx.rotate(fish.rotation);

        // Thân cá lóc kiểu mạnh mẽ, khỏe khoắn
        ctx.fillStyle = "#2db07b";
        ctx.beginPath();
        ctx.ellipse(0, 0, 24, 16, 0, 0, Math.PI * 2);
        ctx.fill();

        // Vảy cá
        for (let i = -12; i <= 12; i += 6) {
            ctx.fillStyle = i % 2 === 0 ? "#38c789" : "#27a86b";
            ctx.beginPath();
            ctx.ellipse(i, 0, 5, 8, 0, 0, Math.PI * 2);
            ctx.fill();
        }

        // Đuôi cá
        ctx.fillStyle = "#f36d5b";
        ctx.beginPath();
        ctx.moveTo(-24, 0);
        ctx.lineTo(-44, -16);
        ctx.lineTo(-44, 16);
        ctx.closePath();
        ctx.fill();

        // Vây lưng
        ctx.fillStyle = "#ffb24c";
        ctx.beginPath();
        ctx.moveTo(0, -10);
        ctx.lineTo(18, -28);
        ctx.lineTo(18, -8);
        ctx.closePath();
        ctx.fill();

        // Vây bụng
        ctx.fillStyle = "#ff8f5b";
        ctx.beginPath();
        ctx.moveTo(2, 10);
        ctx.lineTo(18, 28);
        ctx.lineTo(16, 8);
        ctx.closePath();
        ctx.fill();

        // Vây đuôi phụ
        ctx.fillStyle = "#ff9a6b";
        ctx.beginPath();
        ctx.moveTo(-30, 0);
        ctx.lineTo(-50, -8);
        ctx.lineTo(-50, 8);
        ctx.closePath();
        ctx.fill();

        // Mắt
        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(10, -5, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#111111";
        ctx.beginPath();
        ctx.arc(12, -5, 2.4, 0, Math.PI * 2);
        ctx.fill();

        // Miệng
        ctx.strokeStyle = "#1c1c1c";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(18, 0);
        ctx.lineTo(27, 4);
        ctx.stroke();

        // Nếp gân rất đẹp
        ctx.strokeStyle = "rgba(255,255,255,0.25)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(4, -5);
        ctx.lineTo(14, -8);
        ctx.moveTo(5, 6);
        ctx.lineTo(15, 10);
        ctx.stroke();

        ctx.restore();
    }

    function drawPipe(pipe) {
        const x = pipe.x;*

