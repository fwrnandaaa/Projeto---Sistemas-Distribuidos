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

        // Não exibe mensagens técnicas de conexão na interface.
        if (dados.tipo === 'conexao') {
          return;
        }

        setMensagens(listaAtual =>
          [
            ...listaAtual,
            {
              id: Date.now(),
              tipo: dados.tipo || 'notificacao',
              conteudo: dados.dados || dados.conteudo || dados,
              enviado_em: dados.enviado_em || '',
            },
          ].slice(-5)
        );
      } catch {
        setMensagens(listaAtual =>
          [
            ...listaAtual,
            {
              id: Date.now(),
              tipo: 'mensagem',
              conteudo: { mensagem: event.data },
              enviado_em: '',
            },
          ].slice(-5)
        );
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
    const conteudo = notificacao.conteudo;

    if (typeof conteudo === 'string') {
      return conteudo;
    }

    if (notificacao.tipo === 'novo_agendamento') {
      const dadosAgendamento = conteudo.dados || conteudo;

      return `Novo agendamento criado — Data: ${dadosAgendamento.data} | Horário: ${dadosAgendamento.horario}`;
    }

    return (
      conteudo.mensagem ||
      conteudo.texto ||
      JSON.stringify(conteudo)
    );
  };

  return (
    <section className="notificacoes-websocket">
      <div className="notificacoes-cabecalho">
        <span>🔔 Notificações em tempo real</span>

        <span className={`status-websocket status-${status}`}>
          {status}
        </span>
      </div>

      {mensagens.length === 0 ? (
        <p className="notificacoes-vazio">
          Nenhuma notificação recebida ainda.
        </p>
      ) : (
        <ul className="lista-notificacoes">
          {[...mensagens].reverse().map(notificacao => (
            <li key={notificacao.id} className="notificacao-item">
            {textoMensagem(notificacao)}
          </li>
          ))}
        </ul>
      )}
    </section>
  );
}