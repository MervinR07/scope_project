// for (let i = 0; i < 60; i++) {
//     let snow = document.createElement("div");
//     snow.className = "snowflake";
//     snow.innerHTML = "❄";
//     snow.style.left = Math.random() * 100 + "vw";
//     snow.style.animationDuration = 5 + Math.random() * 6 + "s";
//     snow.style.opacity = Math.random();
//     snow.style.fontSize = (10 + Math.random() * 20) + "px";
  
//   document.body.appendChild(snow);
// }

// Subtle winter snow effect
for (let i = 0; i < 30; i++) {
    let snow = document.createElement("div");
    snow.className = "snowflake";
    snow.innerHTML = "❄";
    snow.style.left = Math.random() * 100 + "vw";
    snow.style.animationDuration = 8 + Math.random() * 8 + "s";
    snow.style.fontSize = (10 + Math.random() * 8) + "px";
    document.body.appendChild(snow);
}
