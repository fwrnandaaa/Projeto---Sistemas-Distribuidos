const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  app.use(
    ['/medicos', '/especialidades', '/agendas', '/agendamentos', '/convenio', '/relatorios'],
    createProxyMiddleware({ target: 'http://localhost:8000', changeOrigin: true })
  );
};
