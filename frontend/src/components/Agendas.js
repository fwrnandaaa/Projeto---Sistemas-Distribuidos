import { useEffect, useState } from 'react';
import { api } from '../api';

const initForm = { medico_id: '', data: '', horario: '', disponivel: true };

export default function Agendas() {
  const [agendas, setAgendas] = useState([]);
  const [medicos, setMedicos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState('');
  const [form, setForm] = useState(initForm);
  const [salvando, setSalvando] = useState(false);
  const [mensagem, setMensagem] = useState('');

  const carregar = () => {
    setLoading(true);
    api.getAgendas()
      .then(setAgendas)
      .catch(() => setErro('Erro ao carregar agendas. Verifique se o serviço de agendamentos está rodando.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    carregar();
    api.getMedicos().then(setMedicos);
  }, []);

  const nomeMedico = (id) => {
    const m = medicos.find(m => m.id === id);
    return m ? m.nome : `ID ${id}`;
  };

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    setForm(f => ({ ...f, [name]: type === 'checkbox' ? checked : value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setSalvando(true);
    setMensagem('');
    try {
      const resultado = await api.createAgenda({
        ...form,
        medico_id: Number(form.medico_id),
      });
      if (resultado.id) {
        setMensagem('Agenda criada com sucesso!');
        setForm(initForm);
        carregar();
      } else {
        setMensagem('Erro: ' + JSON.stringify(resultado));
      }
    } catch {
      setMensagem('Erro ao criar agenda.');
    } finally {
      setSalvando(false);
    }
  };

  const handleExcluir = async (id) => {
    if (!window.confirm('Excluir esta agenda?')) return;
    await api.deleteAgenda(id);
    carregar();
  };

  return (
    <div>
      <div className="card">
        <h2>Nova Agenda</h2>
        <form onSubmit={handleSubmit} className="form-grid">
          <label>
            Médico
            <select name="medico_id" value={form.medico_id} onChange={handleChange} required>
              <option value="">— Selecione o médico —</option>
              {medicos.map(m => (
                <option key={m.id} value={m.id}>{m.nome}</option>
              ))}
            </select>
          </label>
          <label>
            Data
            <input name="data" type="date" value={form.data} onChange={handleChange} required />
          </label>
          <label>
            Horário
            <input name="horario" type="time" value={form.horario} onChange={handleChange} required />
          </label>
          <label className="checkbox-label">
            <input name="disponivel" type="checkbox" checked={form.disponivel} onChange={handleChange} />
            Disponível
          </label>
          <button type="submit" disabled={salvando}>
            {salvando ? 'Salvando...' : 'Criar Agenda'}
          </button>
        </form>
        {mensagem && <p className={mensagem.startsWith('Erro') ? 'erro' : 'sucesso'}>{mensagem}</p>}
      </div>

      <div className="card">
        <h2>Agendas Cadastradas</h2>
        {loading ? (
          <p className="info">Carregando...</p>
        ) : erro ? (
          <p className="erro">{erro}</p>
        ) : agendas.length === 0 ? (
          <p className="info">Nenhuma agenda cadastrada.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Médico</th>
                <th>Data</th>
                <th>Horário</th>
                <th>Disponível</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {agendas.map(a => (
                <tr key={a.id}>
                  <td>{a.id}</td>
                  <td>{nomeMedico(a.medico_id)}</td>
                  <td>{a.data}</td>
                  <td>{a.horario}</td>
                  <td>{a.disponivel ? '✅' : '❌'}</td>
                  <td>
                    <button className="btn-excluir" onClick={() => handleExcluir(a.id)}>Excluir</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
