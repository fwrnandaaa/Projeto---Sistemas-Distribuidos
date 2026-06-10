import { useEffect, useState } from 'react';

export default function NotificacoesWebSocket() {
  const [status, setStatus] = useState('desconectado');
  const [mensagens, setMensagens] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8004/ws/notificacoes');

    socket.onopen = () => {
      setStatus('conectado');
    };

    socket.onmessage = event => {
      try {
        const dados = JSON.parse(event.data);

        setMensagens(listaAtual => [
          ...listaAtual,
          {
            id: Date.now(),
            tipo: dados.tipo || 'notificacao',
            conteudo: dados.dados || dados,
            enviado_em: dados.enviado_em || '',
          },
        ]);
      } catch {
        setMensagens(listaAtual => [
          ...listaAtual,
          {
            id: Date.now(),
            tipo: 'mensagem',
            conteudo: { mensagem: event.data },
            enviado_em: '',
          },
        ]);
      }
    };

    socket.onerror = () => {
      setStatus('erro');
    };

    socket.onclose = () => {
      setStatus('desconectado');
    };

    return () => {
      socket.close();
    };
  }, []);

  const textoMensagem = notificacao => {
    if (typeof notificacao.conteudo === 'string') {
      return notificacao.conteudo;
    }

    return (
      notificacao.conteudo.mensagem ||
      notificacao.conteudo.texto ||
      JSON.stringify(notificacao.conteudo)
    );
  };

  return (
    <section className="notificacoes-websocket">
      <p className="status-websocket">WebSocket: {status}</p>

      {mensagens.length > 0 && (
        <ul>
          {mensagens.map(notificacao => (
            <li key={notificacao.id}>
              <strong>{notificacao.tipo}:</strong> {textoMensagem(notificacao)}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}