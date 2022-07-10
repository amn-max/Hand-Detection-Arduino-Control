const bodyParser = require("body-parser");

const port = process.env.PORT || 3000;

const WebSocket = require("ws");
const wss = new WebSocket.Server({ port: port });

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
