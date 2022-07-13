const express = require("express");
const bodyParser = require("body-parser");
const { v4: uuidv4 } = require("uuid");

var http = require("http");
var path = require("path");
const INDEX = "./index.ejs";
const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public")));
app.set("views", "./views");
app.set("view engine", "ejs");
const server = http.createServer(app);
const io = require("socket.io")(server);
const { ExpressPeerServer } = require("peer");
const peerServer = ExpressPeerServer(server, {
  debug: true,
});

app.use("/peerjs", peerServer);
app.get("/", (req, res) => {
  res.redirect(`${uuidv4()}`);
});

const port = process.env.PORT || 3000;

const WebSocket = require("ws");
const wss = new WebSocket.Server({ server });

app.get("/", async function (req, res) {
  var lines = [];
  res.render(INDEX, { lines: lines });
});

app.get("/video", async function (req, res) {
  const range = req.headers.range;
  if (!range) {
    res.status(400).send("Requires Range Header");
  }
});

wss.on("connection", function connection(ws) {
  console.log("Client connected");
  console.log(wss.clients.size);
  ws.on("message", function (data) {
    wss.clients.forEach(function (client) {
      if (client != ws && client.readyState) {
        client.send(data);
      }
    });
  });
  ws.on("close", function () {
    console.log("lost one client");
    console.log(wss.clients.size);
  });
});

server.listen(port);
