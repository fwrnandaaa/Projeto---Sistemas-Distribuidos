const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  app.use(
    ['/medicos', '/especialidades', '/agendas', '/agendamentos', '/convenio'],
    createProxyMiddleware({ target: 'http://localhost:8000', changeOrigin: true })
  );
};