const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  app.use(
    ['/medicos', '/especialidades'],
    createProxyMiddleware({ target: 'http://localhost:8001', changeOrigin: true })
  );
  app.use(
    ['/agendas', '/agendamentos'],
    createProxyMiddleware({ target: 'http://localhost:8002', changeOrigin: true })
  );
};
