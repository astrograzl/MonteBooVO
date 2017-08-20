function setup() {
  var canvas = createCanvas(960, 720);
  canvas.parent('canvas');
  frameRate(25);
  background(255);
  strokeWeight(2);
  stroke(255);
  init(a);
}

var a = 20;

function draw() {
  var x = random(width); x -= x % a;
  var y = random(height); y -= y % a;

  var r = random(255);
  var g = random(255);
  var b = random(255);

  fill(r, g, b);
  rect(x, y, a, a);
}

function init(a) {
  for (var x = 0; x < width; x += a) {
    for (var y = 0; y < height; y += a) {
      var r = random(255);
      var g = random(255);
      var b = random(255);
      fill(r, g, b);
      rect(x, y, a, a);
    }
  }
}
