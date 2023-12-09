// Display photo previews on home page
let i = 0;
let images = [];
let time = 2000;

images[0] = "./static/images/13goingon30.jpeg";
images[1] = "./static/images/Barbie.jpeg";
images[2] = "./static/images/Endgame.jpeg";
images[3] = "./static/images/Erastour.jpeg";
images[4] = "./static/images/Everything.jpeg";
images[5] = "./static/images/Hungergames.jpeg";
images[6] = "./static/images/Interstellar.jpeg";
images[7] = "./static/images/Legallyblonde.jpeg";
images[8] = "./static/images/Oppenheimer.jpeg";
images[9] = "./static/images/Spiritedaway.jpeg";

function change() {
    document.previews.src = images[i];
    if (i < images.length - 1) {
        i++;
    } else {
        i = 0;
    }

    setTimeout("change()", time);
}

window.onload = change;
