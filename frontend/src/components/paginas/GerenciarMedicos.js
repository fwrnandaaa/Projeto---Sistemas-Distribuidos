import { useEffect, useState } from 'react';
import { api } from '../../api';

const initForm = { nome: '', crm: '', especialidade: '' };

export default function GerenciarMedicos() {
  const [medicos, setMedicos] = useState([]);
  const [especialidades, setEspecialidades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState('');
  const [form, setForm] = useState(initForm);
  const [salvando, setSalvando] = useState(false);
  const [mensagem, setMensagem] = useState('');

  const carregar = () => {
    setLoading(true);
    api.getMedicos()
      .then(setMedicos)
      .catch(() => setErro('Erro ao carregar médicos. Verifique se o serviço de médicos está rodando.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    carregar();
    api.getEspecialidades().then(setEspecialidades);
  }, []);

  const nomeEspecialidade = (id) => {
    const esp = especialidades.find(e => e.id === id);
    return esp ? esp.nome : `ID ${id}`;
  };

  const handleChange = e => {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setSalvando(true);
    setMensagem('');
    try {
      const resultado = await api.createMedico({
        ...form,
        especialidade: Number(form.especialidade),
      });
      if (resultado.id) {
        setMensagem('Médico cadastrado com sucesso!');
        setForm(initForm);
        carregar();
      } else {
        setMensagem('Erro: ' + JSON.stringify(resultado));
      }
    } catch {
      setMensagem('Erro ao cadastrar médico.');
    } finally {
      setSalvando(false);
    }
  };

  const handleExcluir = async (id) => {
    if (!window.confirm('Excluir este médico?')) return;
    await api.deleteMedico(id);
    carregar();
  };

  return (
    <div>
      <div className="card">
        <h2>Novo Médico</h2>
        <form onSubmit={handleSubmit} className="form-grid">
          <label>
            Nome
            <input
              name="nome"
              type="text"
              placeholder="Fulano da Silva"
              value={form.nome}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            CRM
            <input
              name="crm"
              type="text"
              placeholder="123456"
              value={form.crm}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Especialidade
            <select name="especialidade" value={form.especialidade} onChange={handleChange} required>
              <option value="">— Selecione uma especialidade —</option>
              {especialidades.map(e => (
                <option key={e.id} value={e.id}>{e.nome}</option>
              ))}
            </select>
          </label>
          <button type="submit" disabled={salvando}>
            {salvando ? 'Salvando...' : 'Cadastrar Médico'}
          </button>
        </form>
        {mensagem && <p className={mensagem.startsWith('Erro') ? 'erro' : 'sucesso'}>{mensagem}</p>}
      </div>

      <div className="card">
        <h2>Médicos Cadastrados</h2>
        {loading ? (
          <p className="info">Carregando...</p>
        ) : erro ? (
          <p className="erro">{erro}</p>
        ) : medicos.length === 0 ? (
          <p className="info">Nenhum médico cadastrado.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>CRM</th>
                <th>Especialidade</th>
                <th>Ação</th>
              </tr>
            </thead>
            <tbody>
              {medicos.map(m => (
                <tr key={m.id}>
                  <td>{m.nome}</td>
                  <td>{m.crm}</td>
                  <td>{nomeEspecialidade(m.especialidade)}</td>
                  <td>
                    <button 
                      className="btn-delete" 
                      onClick={() => handleExcluir(m.id)}
                    >
                      Excluir
                    </button>
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
