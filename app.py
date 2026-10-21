import streamlit as st
st.set_page_config(page_title="Fishy Dive", page_icon="🐠", layout="centered")
st.title("Fishy Dive")
st.caption("Nhấn Space hoặc click chuột để bơi qua các cục đá")

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
        rocks: [],
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
        state.rocks = [];
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

    function spawnRock() {
        const gap = 170;
        const minTop = 70;
        const maxTop = canvas.height - 80 - gap - minTop;
        const topHeight = minTop + Math.random() * maxTop;

        state.rocks.push({
            x: canvas.width + 20,
            width: 70,
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
            spawnRock();
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

        for (const rock of state.rocks) {
            rock.x -= 2.3 * dt * 0.06;

            if (!rock.passed && rock.x + rock.width < state.fish.x) {
                rock.passed = true;
                state.score += 1;
                updateScore();
            }

            const fishLeft = state.fish.x - state.fish.r;
            const fishRight = state.fish.x + state.fish.r;
            const fishTop = state.fish.y - state.fish.r;
            const fishBottom = state.fish.y + state.fish.r;

            const rockLeft = rock.x;
            const rockRight = rock.x + rock.width;
            const topBottom = rock.topHeight;
            const bottomTop = rock.topHeight + rock.gap;

            const hitX = fishRight > rockLeft && fishLeft < rockRight;
            const hitTop = fishTop < topBottom;
            const hitBottom = fishBottom > bottomTop;

            if (hitX && (hitTop || hitBottom)) {
                gameOver();
            }
        }

        state.rocks = state.rocks.filter(rock => rock.x + rock.width > -20);

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
            ctx.bezierCurveTo(canvas.width * 0.2, y - 12, canvas.width * 0.7, y + 12,*

