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

const themes = [
  {
    name: "biển ban ngày",
    skyTop: "#071f39",
    skyMid: "#0d4f7f",
    skyBottom: "#0aa4c8",
    seaweed: "#1ed38b",
    ground: "#1d5e4d",
    ground2: "#347d66",
    rockFill: "#7a8d8d",
    rockDark: "#5d6d70",
    bubble: "rgba(255,255,255,0.3)",
    tinyFish: "rgba(120,220,255,0.7)"
  },
  {
    name: "biển đêm",
    skyTop: "#0b1220",
    skyMid: "#182b46",
    skyBottom: "#3c6c85",
    seaweed: "#55d7a5",
    ground: "#1c4d4f",
    ground2: "#3d7f73",
    rockFill: "#7d8599",
    rockDark: "#4d5867",
    bubble: "rgba(200,240,255,0.28)",
    tinyFish: "rgba(150,210,255,0.75)"
  },
  {
    name: "biển san hô",
    skyTop: "#041f2d",
    skyMid: "#134d5d",
    skyBottom: "#267a8a",
    seaweed: "#7fe3aa",
    ground: "#204f52",
    ground2: "#3b7a73",
    rockFill: "#d2906f",
    rockDark: "#9b5b46",
    bubble: "rgba(255,230,220,0.25)",
    tinyFish: "rgba(255,158,110,0.7)"
  },
  {
    name: "biển hoang dã",
    skyTop: "#2a1d0d",
    skyMid: "#4d4531",
    skyBottom: "#7c886e",
    seaweed: "#9be34a",
    ground: "#3f5d3a",
    ground2: "#5d7a47",
    rockFill: "#6d7e5e",
    rockDark: "#4f5d45",
    bubble: "rgba(255,255,255,0.22)",
    tinyFish: "rgba(176,255,160,0.7)"
  }
];

function hexToRgb(hex) {
  const clean = hex.replace("#", "");
  const bigint = parseInt(clean, 16);
  return {
    r: (bigint >> 16) & 255,
    g: (bigint >> 8) & 255,
    b: bigint & 255
  };
}

function mixColor(a, b, t) {
  const c1 = hexToRgb(a);
  const c2 = hexToRgb(b);
  const r = Math.round(c1.r + (c2.r - c1.r) * t);
  const g = Math.round(c1.g + (c2.g - c1.g) * t);
  const bVal = Math.round(c1.b + (c2.b - c1.b) * t);
  return "rgb(" + r + "," + g + "," + bVal + ")";
}

function getThemeFromIndex(i) {
  return themes[i % themes.length];
}

function getActiveTheme() {
  const base = getThemeFromIndex(game.themeIndex);
  const next = getThemeFromIndex(game.nextThemeIndex);
  if (game.transition <= 0) return base;
  const t = 1 - game.transition;
  return {
    name: base.name,
    skyTop: mixColor(base.skyTop, next.skyTop, t),
    skyMid: mixColor(base.skyMid, next.skyMid, t),
    skyBottom: mixColor(base.skyBottom, next.skyBottom, t),
    seaweed: mixColor(base.seaweed, next.seaweed, t),
    ground: mixColor(base.ground, next.ground, t),
    ground2: mixColor(base.ground2, next.ground2, t),
    rockFill: mixColor(base.rockFill, next.rockFill, t),
    rockDark: mixColor(base.rockDark, next.rockDark, t),
    bubble: base.bubble,
    tinyFish: base.tinyFish
  };
}

const game = {
  running: false,
  over: false,
  score: 0,
  best: 0,
  lastTime: 0,
  spawnTimer: 0,
  themeIndex: 0,
  nextThemeIndex: 1,
  transition: 0,
  fish: { x: 110, y: 310, r: 18, vy: 0, rot: 0 },
  rocks: [],
  bubbles: [],
  seaweeds: [],
  tinyFish: [],
  rockCount: 0
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

function nextTheme() {
  game.nextThemeIndex = (game.theme*

