import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Flappy Bird", page_icon="🐦", layout="centered")

st.title("Flappy Bird trên Streamlit")
st.caption("Nhấn Space hoặc click vào màn hình để bay")

GAME_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    body {
      margin: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f0f4f8;
      font-family: Arial, sans-serif;
    }
    canvas {
      border: 4px solid #1f2937;
      border-radius: 10px;
      background: linear-gradient(#87CEEB, #dff6ff);
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
      display: block;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <canvas id="gameCanvas" width="420" height="640"></canvas>

  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    const groundHeight = 90;
    const gravity = 0.55;
    const flapForce = -8.5;
    const pipeWidth = 70;
    const pipeGap = 150;
    const pipeSpeed = 2.4;

    let bird = {
      x: 90,
      y: canvas.height / 2,
      radius: 16,
      velocity: 0
    };

    let pipes = [];
    let score = 0;
    let bestScore = Number(localStorage.getItem("flappyBest") || 0);
    let lastPipeTime = 0;
    let gameOver = false;
    let started = false;

    function resetGame() {
      bird.y = canvas.height / 2;
      bird.velocity = 0;
      pipes = [];
      score = 0;
      lastPipeTime = 0;
      gameOver = false;
      started = false;
    }

    function flap() {
      if (gameOver) {
        resetGame();
      }
      if (!started) {
        started = true;
      }
      bird.velocity = flapForce;
    }

    function createPipe() {
      const minHeight = 60;
      const maxHeight = canvas.height - groundHeight - pipeGap - 60;
      const topHeight = Math.random() * (maxHeight - minHeight) + minHeight;
      pipes.push({
        x: canvas.width + 20,
        topHeight,
        passed: false
      });
    }

    function update() {
      if (!started || gameOver) return;

      bird.velocity += gravity;
      bird.y += bird.velocity;

      const now = performance.now();
      if (now - lastPipeTime > 1500) {
        lastPipeTime = now;
        createPipe();
      }

      for (let i = pipes.length - 1; i >= 0; i--) {
        const pipe = pipes[i];
        pipe.x -= pipeSpeed;

        if (!pipe.passed && pipe.x + pipeWidth < bird.x) {
          pipe.passed = true;
          score += 1;
          if (score > bestScore) {
            bestScore = score;
            localStorage.setItem("flappyBest", bestScore);
          }
        }

        const hitPipeX = bird.x + bird.radius > pipe.x && bird.x - bird.radius < pipe.x + pipeWidth;
        const hitTop = bird.y - bird.radius < pipe.topHeight;
        const hitBottom = bird.y + bird.radius > pipe.topHeight + pipeGap;

        if (hitPipeX && (hitTop || hitBottom)) {
          gameOver = true;
        }

        if (pipe.x + pipeWidth < 0) {
          pipes.splice(i, 1);
        }
      }

      const groundTop = canvas.height - groundHeight;
      if (bird.y + bird.radius >= groundTop || bird.y - bird.radius <= 0) {
        gameOver = true;
      }
    }

    function drawBackground() {
      ctx.fillStyle = "#87CEEB";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#7EC8E3";
      for (let i = 0; i < 5; i++) {
        ctx.beginPath();
        ctx.arc(60 + i * 90, 80 + (i % 2) * 20, 24, 0, Math.PI * 2);
        ctx.arc(95 + i * 90, 80 + (i % 2) * 20, 30, 0, Math.PI * 2);
        ctx.arc(130 + i * 90, 80 + (i % 2) * 20, 22, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    function drawGround() {
      const groundY = canvas.height - groundHeight;
      ctx.fillStyle = "#7ac142";
      ctx.fillRect(0, groundY, canvas.width, ground*

