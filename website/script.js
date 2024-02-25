document.addEventListener("DOMContentLoaded", () => {
  const box = document.querySelector(".black-box");
  let currentRotation = 0;
  let colors = ["red", "blue", "green", "yellow"];
  let currentColorIndex = 0;
  setInterval(() => {
    box.style.transform = "rotate(" + currentRotation + "deg)";
    box.style.backgroundColor = colors[currentColorIndex];
    currentColorIndex = (currentColorIndex + 1) % colors.length;
    currentRotation = (currentRotation + 1) % 360;
  }, 2000);
});
box.style.transition = "transform 2s linear";
let currentRotation = 0;
setInterval(() => {
    box.style.transform = "rotate(" + currentRotation + "deg)";
    currentRotation = (currentRotation + 1) % 360;
}, 20);
let box = document.querySelector(".black-box");
let position = 0;
let moveRight = true;
