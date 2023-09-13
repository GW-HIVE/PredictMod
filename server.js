//e.g server.js
const express = require("express");
const ViteExpress = require("vite-express");

const app = express();

app.get("/message", (_, res) => res.send("Hello from express!"));

ViteExpress.listen(app, 4242, () => console.log("Server is listening..."));
