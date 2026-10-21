import streamlit as st

st.set_page_config(page_title="Fishy Dive", page_icon="🐠", layout="centered")

st.title("Fishy Dive")
st.caption("Nhấn Space hoặc click chuột để bơi qua các rạn đá")

components_html = """
<style>
    * { box-sizing: border-box; }
    body { margin: 0; }
    #game-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
    }
    #game {
        position: relative;
        width: 430px;
        height: 620px;
        border: 4px solid #113a5e;
        background: linear-gradient(#0b2d4f, #0f4c81, #0c6d9c);
        overflow: hidden;
        user-select: none;
        border-radius: 14px;
        box-shadow: 0 12px 25px rgba(0,0,0,0.25);
    }
    canvas {
        display: block;
        width: 100%;
        height: 100%;
        background: linear-gradient(#0a2546, #0e4d7b, #0d88a9);
    }
    .hud {
        position: absolute;
        top: 10px;
        left: 0;
        width: 100%;
        text-align: center;
        color: #fff;
        font-weight: bold;
        text-shadow: 2px 2px 0 #000;
        pointer-events: none;
    }
    .score {
        font-size: 36px;
    }
    .message {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        background: rgba(8, 25, 36, 0.45);
        color: white;
        border-radius: 12px;
        padding: 18px 24px;
        text-align: center;
        font-size: 20px;
        line-height: 1.5;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.2);
    }
</style>

<div id="game-wrapper">
    <div id="game">
        <div class="hud">
            <div class="score" id="score">0</div>
        </div>
        <canvas id="canvas" width="430" height="620"></canvas>
        <div class="message" id="message">Nhấn Space / Click để bơi</div>
    </div>
</div>

<script>
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const scoreEl = document.getElementById("score");
    const messageEl = document.getElementById("message");

    const W = canvas.width;
    const H = canvas.height;

    let started = false;
    let gameOver = false;
    let score = 0;
    let highScore = 0;

    const fish = {
        x: 110,
        y: H / 2,
        radius: 18,
        velocity: 0,
        gravity: 0.42,
        lift: -8.5,
        rotation: 0
    };

    const bubbles = [];
    let pipes = [];
    let pipeTimer = 0;
    const pipeInterval = 1500;
    const pipeSpeed = 2.3;

    function addBubble() {
        bubbles.push({
            x: Math.random() * W,
            y: H + 20,
            r: 4 + Math.random() * 8,
            speed: 0.6 + Math.random() * 1.2
        });
    }

    function resetGame() {
        fish.y = H / 2;
        fish.velocity = 0;
        fish.rotation = 0;
        pipes = [];
        pipeTimer = 0;
        score = 0;
        scoreEl.textContent = "0";
        started = false;
        gameOver = false;
        messageEl.style.display = "block";
        messageEl.innerHTML = "Nhấn Space / Click để bơi";
    }

    function startGame() {
        if (gameOver) {
            resetGame();
        }
        started = true;
        messageEl.style.display = "none";
        fish.velocity = fish.lift;
    }

    function endGame() {
        gameOver = true;
        started = false;
        highScore = Math.max(highScore, score);
        messageEl.style.display = "block";
        messageEl.innerHTML = "Game Over!<br>Điểm: " + score + "<br>Best: " + highScore + "<br><br>Nhấn Space / Click để chơi lại";
    }

    function spawnPipe() {
        const gap = 170;
        const minTop = 70;
        const maxTop = H - 120 - gap - minTop;
        const topHeight = minTop + Math.random() * maxTop;

        pipes.push({
            x: W + 20,
            width: 72,
            gap: gap,
            topHeight: topHeight,
            passed: false
        });
    }

    function update(delta) {
        if (!started || gameOver) return;

        fish.velocity += fish.gravity * delta * 0.06;
        fish.y += fish.velocity * delta * 0.06;

        fish.rotation = Math.max(-1.3, Math.min(1.5, fish.velocity / 10));

        pipeTimer += delta;
        if (pipeTimer >= pipeInterval) {
            spawnPipe();
            pipeTimer = 0;
        }

        if (Math.random() < 0.08) add*

