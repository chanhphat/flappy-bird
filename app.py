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
    border-radius: 12*

