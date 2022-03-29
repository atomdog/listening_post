
let node_list = [];
let edge_list = [];
let space = 0;

class cell
{
  constructor(x,y,s)
  {
    this.x = (x);
    this.x2 = (x)+10;
    this.y = y;
    this.y2 = y+60;
    this.s = s;
  }
  display()
  {
    stroke(153);
    rect(this.x, this.y, this.x2, this.y2);
  }
}

class block
{
  constructor(y)
  {
    this.cellblock = {};
    this.startx = (10);
    this.starty = y;
    this.endx = ((x2)*20)+10;
    this.endy = y+60;
  }
  display()
  {
    stroke(153);
    line(this.startx,this.starty,this.endx,this.endy);
  }
}

let font,fontsize = 8;
function preload() {
  font = loadFont('assets/SourceSansPro-Light.ttf');
  sents = loadJSON("assets/sentimentstash.json");
}

function setup()
{
  counter = 0;
  blocks = {};

  for(key in sents)
  {
    b = new block(counter*60);
    c2 = 0;
    for ykey in sents[key]['y']
    {
      ce = new cell(c2, counter*60, sents[key]['y'][0]);
      c2 = c2+1;
      blocks.cellblock.push(ce);
    }

    blocks.push(b);
  }

  createCanvas(2000, 2000);
  textFont(font);
  textSize(fontsize);
  textAlign(CENTER, CENTER);

}

function draw()
{
  background(220);
  for(let i = 0; i < blocks.length; i++)
  {
    blocks[i].display();
    for(let i2 = 0; i2 < blocks[i].length; i++)
    {
      blocks[i][i2].display();
    }
  }


}
