layer_buttons = document.getElementById("layer_buttons");
main_img = document.getElementById("main_img");

function onMouseDown(event) {
    // this - button
    let button = this.children[0];
    let img = document.getElementById("img-" + button.value);
    if (img.style.opacity === "0") {
        // Enable img
        img.style.opacity = "0.5";
        button.style.backgroundColor = "#CCCCCC";
    } else {
        // Disable img
        img.style.opacity = "0";
        button.style.backgroundColor = "#f8f9fa";
    }

}

for (let elem of layer_buttons.children) {
    elem.addEventListener("click", onMouseDown);
}