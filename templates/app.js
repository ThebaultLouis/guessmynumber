// Vider le localStorage
localStorage.setItem("image", JSON.stringify([]));
// Initialisation Canvas
var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext('2d');

var painting = document.getElementById('paint');
var paint_style = getComputedStyle(painting);
canvas.width = parseInt(paint_style.getPropertyValue('width'));
canvas.height = parseInt(paint_style.getPropertyValue('height'));

var mouse = {
    x: 0,
    y: 0
};

// Mouvement
move = function (e) {
    mouse.x = e.pageX - this.offsetLeft;
    mouse.y = e.pageY - this.offsetTop;
}
canvas.addEventListener('mousemove', move, false);
canvas.addEventListener('touchmove', move, false);

ctx.lineWidth = 3;
ctx.lineJoin = 'round';
ctx.lineCap = 'round';
ctx.strokeStyle = '#000000';
// Debut du trait
canvas.addEventListener('mousedown', function (e) {
    ctx.beginPath();
    ctx.moveTo(mouse.x, mouse.y);

    canvas.addEventListener('mousemove', onPaint, false);
}, false);
canvas.addEventListener('touchstart', function (e) {
    ctx.beginPath();
    ctx.moveTo(mouse.x, mouse.y);

    canvas.addEventListener('touchmove', onPaint, false);
}, false);

// Fin du trait
canvas.addEventListener('mouseup', function () {
    canvas.removeEventListener('mousemove', onPaint, false);
}, false);
canvas.addEventListener('touchend', function () {
    canvas.removeEventListener('touchmove', onPaint, false);
}, false);

var onPaint = function () {
    ctx.lineTo(mouse.x, mouse.y);
    ctx.stroke();
};
// Réinitialiser
function clearArea() {
    // Use the identity matrix while clearing the canvas
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}
// Affichage des résultats
function displayImages() {

    var resultat = document.getElementById('display')
    var images = JSON.parse(localStorage.getItem("image"))

    // Creation de la div
    var div = document.createElement("div")
    div.setAttribute("width", "100%")
    div.setAttribute("height", ctx.canvas.height)
    div.classList.add("resultat")

    // Ajout du nombre deviné
    div.style.backgroundImage = images[0].image
    var h2 = document.createElement("h2")
    h2.appendChild(document.createTextNode(images[0].number))
    h2.classList.add("resultatTitre")
    h2.style.fontSize = "2em"
    h2.style.backgroundColor = "#7ec0ee"
    h2.style.marginBottom = "0"
    div.appendChild(h2)

    // Ajout du nombre deviné
    var img = document.createElement("img")
    img.setAttribute("width", "100%")
    img.setAttribute("height", ctx.canvas.height)
    img.setAttribute("src", images[0].image)
    // img.style.marginTop = "10px"
    // img.style.border = "solid black 2px"
    img.style.backgroundColor = "white"

    div.appendChild(img)
    resultat.insertBefore(div, resultat.firstChild)

    // resultat.insertBefore(img, resultat.firstChild)

}
// Envoyer au serveur
function submit(image) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "http://localhost:5000/100/100", false);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify({
        image: image
    }));
    return Number(JSON.parse(xhttp.responseText)['number'])
    // console.log(xhttp.responseText)
    // return 1
}
// Sauvegarder
var btn = document.getElementById('upload');

btn.addEventListener('click', e => {
    var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream"); // here is the most important part because if you dont replace you will get a DOM 18 exception.
    // console.log(image)
    // window.location.href=image;

    // Soumettre l'image à l'IA
    var number = submit(JSON.stringify(image))

    // Enregistrer dans l'historique des résultats
    var images = JSON.parse(localStorage.getItem("image"))
    images.unshift({
        image,
        number
    })
    localStorage.setItem("image", JSON.stringify(images))
    clearArea()
    displayImages()

})