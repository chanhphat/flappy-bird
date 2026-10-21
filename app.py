function drawFish() {
  const f = game.fish;

  ctx.save();
  ctx.translate(f.x, f.y);
  ctx.rotate(f.rot);

  // thân cá dài, dẹp ngang
  ctx.fillStyle = "#2f9ec9";
  ctx.beginPath();
  ctx.ellipse(0, 0, 34, 18, 0, 0, Math.PI * 2);
  ctx.fill();

  // vùng ánh sáng trên thân
  ctx.fillStyle = "rgba(255,255,255,0.25)";
  ctx.beginPath();
  ctx.ellipse(-4, -3, 18, 10, 0, 0, Math.PI * 2);
  ctx.fill();

  // sọc đen / xanh đậm trên thân (để giống cá trong ảnh)
  ctx.strokeStyle = "#1c2b3d";
  ctx.lineWidth = 2;
  for (let i = -18; i <= 18; i += 7) {
    ctx.beginPath();
    ctx.moveTo(i, -10);
    ctx.quadraticCurveTo(i + 8, 0, i + 3, 12);
    ctx.stroke();
  }

  // vệt đen dọc và đốm
  ctx.fillStyle = "#1f2d3f";
  ctx.beginPath();
  ctx.ellipse(-2, -2, 8, 12, 0.2, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#1f2d3f";
  ctx.beginPath();
  ctx.ellipse(12, 2, 6, 8, 0.1, 0, Math.PI * 2);
  ctx.fill();

  // đuôi
  ctx.fillStyle = "#f76b5d";
  ctx.beginPath();
  ctx.moveTo(-30, 0);
  ctx.lineTo(-52, -18);
  ctx.lineTo(-52, 18);
  ctx.closePath();
  ctx.fill();

  // đuôi phụ nhỏ
  ctx.fillStyle = "#ff8d6a";
  ctx.beginPath();
  ctx.moveTo(-28, 0);
  ctx.lineTo(-46, -9);
  ctx.lineTo(-46, 9);
  ctx.closePath();
  ctx.fill();

  // vây lưng
  ctx.fillStyle = "#f7b24d";
  ctx.beginPath();
  ctx.moveTo(-2, -12);
  ctx.lineTo(16, -28);
  ctx.lineTo(18, -8);
  ctx.closePath();
  ctx.fill();

  // vây bụng
  ctx.fillStyle = "#f86b4c";
  ctx.beginPath();
  ctx.moveTo(4, 10);
  ctx.lineTo(18, 28);
  ctx.lineTo(16, 8);
  ctx.closePath();
  ctx.fill();

  // vây ngực
  ctx.fillStyle = "#ff9e63";
  ctx.beginPath();
  ctx.moveTo(4, 4);
  ctx.lineTo(18, 14);
  ctx.lineTo(12, 0);
  ctx.closePath();
  ctx.fill();

  // mắt
  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.arc(12, -5, 6, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#111111";
  ctx.beginPath();
  ctx.arc(14, -5, 2.4, 0, Math.PI * 2);
  ctx.fill();

  // miệng
  ctx.strokeStyle = "#111111";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(20, 0);
  ctx.lineTo(28, 4);
  ctx.stroke();

  // chấm sáng mắt
  ctx.fillStyle = "rgba(255,255,255,0.6)";
  ctx.beginPath();
  ctx.arc(10, -7, 1.5, 0, Math.PI * 2);
  ctx.fill();

  ctx.restore();
}
