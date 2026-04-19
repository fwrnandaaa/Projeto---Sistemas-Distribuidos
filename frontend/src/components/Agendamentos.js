import { useEffect, useState } from 'react';
import { api } from '../api';

export default function Agendamentos() {
  const [agendamentos, setAgendamentos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState('');

  const carregar = () => {
    setLoading(true);
    api.getAgendamentos()
      .then(setAgendamentos)
      .catch(() => setErro('Erro ao carregar agendamentos.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { carregar(); }, []);

  const handleCancelar = async (id) => {
    if (!window.confirm('Cancelar este agendamento?')) return;
    await api.deleteAgendamento(id);
    carregar();
  };

  if (loading) return <p className="info">Carregando agendamentos...</p>;
  if (erro) return <p className="erro">{erro}</p>;

  return (
    <div className="card">
      <h2>Consultas Agendadas</h2>
      {agendamentos.length === 0 ? (
        <p className="info">Nenhum agendamento encontrado.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>CPF do Paciente</th>
              <th>Médico ID</th>
              <th>Data</th>
              <th>Horário</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {agendamentos.map(ag => (
              <tr key={ag.id}>
                <td>{ag.id}</td>
                <td>{ag.usuario_cpf}</td>
                <td>{ag.agenda_detalhe?.medico_id ?? '—'}</td>
                <td>{ag.agenda_detalhe?.data ?? '—'}</td>
                <td>{ag.agenda_detalhe?.horario ?? '—'}</td>
                <td>
                  <button className="btn-excluir" onClick={() => handleCancelar(ag.id)}>
                    Cancelar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
