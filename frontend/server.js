var express = require("express");
var http = require('http');
var proxyMiddleware = require("http-proxy-middleware");

var isDev = process.env.NODE_ENV == "development";
var apiUrl = "http://infoauto-backend:8000";

var app = express();

app.use(
  proxyMiddleware("/api/**/*.json", {
    target: "http://localhost:3000",
    secure: false,
    pathRewrite: {
      "^/api": "/",
    },
    changeOrigin: true,
  })
);

app.use(
  proxyMiddleware(["/api/**", "!**/*.json"], {
    target: apiUrl,
    secure: false,
    changeOrigin: false,
  })
);

app.use('/scripts', express.static(__dirname + '/dist/scripts'));
app.use('/styles', express.static(__dirname + '/dist/styles'));
app.use('/app', express.static(__dirname + '/dist/app'));
app.use('/maps', express.static(__dirname + '/dist/maps'));
app.use('/assets', express.static(__dirname + '/dist/assets'));

app.use('/*', function (req,res) {
  res.sendFile('/dist/index.html', { root: __dirname })
})

app.listen(3000, () => {
    console.log('serving...');
})
