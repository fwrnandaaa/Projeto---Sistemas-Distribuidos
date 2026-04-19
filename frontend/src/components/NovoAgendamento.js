import { useEffect, useState } from 'react';
import { api } from '../api';

const initForm = { usuario_cpf: '', agenda: '' };

export default function NovoAgendamento({ onSucesso }) {
  const [agendas, setAgendas] = useState([]);
  const [medicos, setMedicos] = useState([]);
  const [form, setForm] = useState(initForm);
  const [salvando, setSalvando] = useState(false);
  const [mensagem, setMensagem] = useState('');
  const [filtroMedico, setFiltroMedico] = useState('');

  useEffect(() => {
    api.getAgendas().then(data => setAgendas(data.filter(a => a.disponivel)));
    api.getMedicos().then(setMedicos);
  }, []);

  const nomeMedico = (id) => {
    const med = medicos.find(m => m.id === id);
    return med ? `${med.nome} (CRM: ${med.crm})` : `Médico ID ${id}`;
  };

  const agendasFiltradas = filtroMedico
    ? agendas.filter(a => String(a.medico_id) === filtroMedico)
    : agendas;

  const handleChange = e => {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setSalvando(true);
    setMensagem('');
    try {
      const resultado = await api.createAgendamento({
        usuario_cpf: form.usuario_cpf,
        agenda: Number(form.agenda),
      });
      if (resultado.id) {
        setMensagem('Consulta agendada com sucesso!');
        setForm(initForm);
        setFiltroMedico('');
        // atualiza lista de agendas disponíveis
        api.getAgendas().then(data => setAgendas(data.filter(a => a.disponivel)));
        if (onSucesso) onSucesso();
      } else {
        setMensagem('Erro: ' + JSON.stringify(resultado));
      }
    } catch {
      setMensagem('Erro ao realizar agendamento.');
    } finally {
      setSalvando(false);
    }
  };

  return (
    <div className="card">
      <h2>Marcar Consulta</h2>
      <form onSubmit={handleSubmit} className="form-grid">
        <label>
          CPF do Paciente
          <input
            name="usuario_cpf"
            type="text"
            placeholder="000.000.000-00"
            value={form.usuario_cpf}
            onChange={handleChange}
            required
            maxLength={14}
          />
        </label>

        <label>
          Filtrar por Médico
          <select value={filtroMedico} onChange={e => { setFiltroMedico(e.target.value); setForm(f => ({ ...f, agenda: '' })); }}>
            <option value="">— Todos os médicos —</option>
            {medicos.map(m => (
              <option key={m.id} value={String(m.id)}>{m.nome}</option>
            ))}
          </select>
        </label>

        <label>
          Horário Disponível
          <select name="agenda" value={form.agenda} onChange={handleChange} required>
            <option value="">— Selecione —</option>
            {agendasFiltradas.map(a => (
              <option key={a.id} value={a.id}>
                {nomeMedico(a.medico_id)} — {a.data} às {a.horario}
              </option>
            ))}
          </select>
        </label>

        <button type="submit" disabled={salvando}>
          {salvando ? 'Agendando...' : 'Confirmar Agendamento'}
        </button>
      </form>
      {mensagem && <p className={mensagem.startsWith('Erro') ? 'erro' : 'sucesso'}>{mensagem}</p>}
    </div>
  );
}
