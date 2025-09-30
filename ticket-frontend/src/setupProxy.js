const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function(app) {
  const target = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

  console.log(`[setupProxy] Proxying /api → ${target}`);

  app.use(
    "/api",
    createProxyMiddleware({
      target,
      changeOrigin: true,
    })
  );
};
