import { useEffect, useState } from 'react';
import { api } from '../../api';

export default function Convenio() {
  const [planos, setPlanos] = useState([]);
  const [cpf, setCpf] = useState('');
  const [planoSelecionado, setPlanoSelecionado] = useState('');
  const [mensagem, setMensagem] = useState('');
  const [erro, setErro] = useState('');
  const [salvando, setSalvando] = useState(false);

  useEffect(() => {
    api.getPlanos().then(data => setPlanos(data.planos || []));
  }, []);

  const handleCadastrar = async () => {
    if (!cpf || !planoSelecionado) return;
    setSalvando(true);
    setMensagem('');
    setErro('');
    try {
      const data = await api.cadastrarConvenio(cpf, planoSelecionado);
      setMensagem(data.resultado || 'Convênio cadastrado!');
    } catch {
      setErro('Erro ao cadastrar convênio.');
    } finally {
      setSalvando(false);
    }
  };
const handleVerificar = async () => {
    if (!cpf || !planoSelecionado) return;
    setSalvando(true);
    setMensagem('');
    setErro('');
    try {
      const resp = await fetch(`/convenio/verificar?cpf=${encodeURIComponent(cpf)}&plano=${encodeURIComponent(planoSelecionado)}`);
      const data = await resp.json();
      if (!resp.ok) {
        setErro(data.detail || 'Convênio não encontrado.');
      } else {
        setMensagem(data.resultado || 'Cobertura verificada!');
      }
    } catch {
      setErro('Erro ao verificar convênio.');
    } finally {
      setSalvando(false);
    }
  };

  return (
    <div className="card">
      <h2>Verificar Convênio</h2>
      <div className="form-grid">
        <label>
          CPF do Paciente
          <input
            type="text"
            placeholder="000.000.000-00"
            value={cpf}
            onChange={e => setCpf(e.target.value)}
            maxLength={14}
          />
        </label>

        <label>
          Plano de Saúde
          <select value={planoSelecionado} onChange={e => setPlanoSelecionado(e.target.value)}>
            <option value="">— Selecione um plano —</option>
            {planos.map(p => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
        </label>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <button onClick={handleCadastrar} disabled={salvando}>
            {salvando ? 'Aguarde...' : 'Cadastrar Convênio'}
          </button>
          <button onClick={handleVerificar} disabled={salvando}>
            {salvando ? 'Aguarde...' : 'Verificar Cobertura'}
          </button>
        </div>
      </div>

      {mensagem && <p className="sucesso">{mensagem}</p>}
      {erro && <p className="erro">{erro}</p>}
    </div>
  );
}