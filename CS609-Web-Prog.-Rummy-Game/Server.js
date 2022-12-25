const http = require('http');
const server = http.createServer()

let N = 2
let playerNum=0
let turn = 0

let deck=[]
let stock=[]
const conv = '0A23456789TJQK'
let deal = [[], []]

function mkDeck() {
  for (let i of 'SHDC' ) {
    for (let j=1; j<=13; j++) {
      deck.push(conv[j]+i)
    }
  }
}

function shuffle() {
  for(let i=0; i<52; i++) {
     stock.push(deck[i])
  }
  for(let j=52; j>1; j--) {
    let k = parseInt(j*Math.random())
    //swap stock[j-1], stock[k]
    let t=stock[j-1]
    stock[j-1]=stock[k]
    stock[k]=t
  }
}

function mkDeal(N,deal) {
  for(let i=0; i<7; i++) {
  for(let j=0; j<N; j++) {
    deal[j].push(stock.pop())
  }} 
}

discardList = ['1D','1S']


server.on('request', (request, response)=>{
  const { headers, method, url } = request;
  console.log(url)
  let qm = url.indexOf('?')
  let equal = url.indexOf('=')
  let want = url.substring(qm+1,equal)
  let wpPlayerNum = url.slice(equal+1)
  //turn = (turn+1)%N
  console.log(`${want}`)
  console.log('PlayerNum='+`${wpPlayerNum}`)
  console.log('Turn='+`${turn}`)
  if (wpPlayerNum==turn) {
    console.log('equal')
  }
  else {
    console.log('NOT equal')
  }
  let body = [];
  if (want=='play') {
    if (playerNum<2) {
       //print a message 'too early; wait and try again'
      response.statusCode = 200;
      response.setHeader('Content-Type', 'application/json');
      const responseBody = { headers, method, url, body };
      console.log(`display2("Too early wait and try again")`);
      response.write(`display2("Too early wait and try again")`);
      response.end();
    }
    else {
      if (wpPlayerNum==turn) {
         //play
        response.statusCode = 200;
        response.setHeader('Content-Type', 'application/json');
        const responseBody = { headers, method, url, body };
        response.write(`display2("Please Play",'${discardList}')`);
        response.end();
      }
      else {
        response.statusCode = 200;
        response.setHeader('Content-Type', 'application/json');
        const responseBody = { headers, method, url, body };
        response.write(`display2("Wait your turn")`);
        response.end();
      }
    }
  }
  if (want=='login') {
    if (playerNum==0) {
      mkDeck()
      shuffle()
      mkDeal(N,deal)
      console.log(deal)
    }
    console.log(`${playerNum}`)
    response.statusCode = 200;
    response.setHeader('Content-Type', 'application/json');
    const responseBody = { headers, method, url, body };
    response.write(`display('${playerNum}','${deal[playerNum]}')`);
    console.log(`display('${playerNum}','${deal[playerNum]}')`);
    response.end();
    playerNum++
    console.log(`${playerNum}`)
  }
  request.on('error', (err) => {
    console.error(err);
  }).on('data', (chunk) => {
    body.push(chunk);
  }).on('end', () => {
    body = Buffer.concat(body).toString();
    // BEGINNING OF NEW STUFF

    response.on('error', (err) => {
      console.error(err);
    });

    // Note: the 2 lines above could be replaced with this next one:
    // response.writeHead(200, {'Content-Type': 'application/json'})


    // Note: the 2 lines above could be replaced with this next one:
    // response.end(JSON.stringify(responseBody))

    // END OF NEW STUFF
  });
}).listen(60302);
