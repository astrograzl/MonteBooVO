function setup() {
  noStroke();
  frameRate(25);
  var canvas = createCanvas(960, 720);
  canvas.parent('canvas');
}

var t = 666;
var hit = 25;

function draw() {
  translate(width/2, height/2);
  if (hit == 25) {
    background(255);
    terc(t/10);
    hit = 0;
  }
  if (frameCount % 25 == 0 && strela(32)) hit++;
}

function terc(r) {
  for (var i = 10; i > 0; i -= 1) {
    if (i % 2 == 0) {
      fill(255);
    } else {
      fill(0);
    }
    ellipse(0, 0, i*r, i*r);
  }
}

function strela(r) {
  var x = random(-width/2, width/2);
  var y = random(-height/2, height/2);
  if (sqrt(sq(x)+sq(y)) < t/2) {
    fill(255, 0, 0);
    ellipse(x, y, r, r);
    return true;
  } else {
    fill(128);
    ellipse(x, y, r, r);
    return false;
  }
}
