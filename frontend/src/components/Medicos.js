import { useEffect, useState } from 'react';
import { api } from '../api';

export default function Medicos() {
  const [medicos, setMedicos] = useState([]);
  const [especialidades, setEspecialidades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState('');

  useEffect(() => {
    Promise.all([api.getMedicos(), api.getEspecialidades()])
      .then(([med, esp]) => {
        setMedicos(med);
        setEspecialidades(esp);
      })
      .catch(() => setErro('Erro ao carregar dados. Verifique se o serviço de médicos está rodando.'))
      .finally(() => setLoading(false));
  }, []);

  const nomeEspecialidade = (id) => {
    const esp = especialidades.find(e => e.id === id);
    return esp ? esp.nome : '—';
  };

  if (loading) return <p className="info">Carregando médicos...</p>;
  if (erro) return <p className="erro">{erro}</p>;

  return (
    <div className="card">
      <h2>Médicos Cadastrados</h2>
      {medicos.length === 0 ? (
        <p className="info">Nenhum médico cadastrado.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Nome</th>
              <th>CRM</th>
              <th>Especialidade</th>
            </tr>
          </thead>
          <tbody>
            {medicos.map(m => (
              <tr key={m.id}>
                <td>{m.nome}</td>
                <td>{m.crm}</td>
                <td>{nomeEspecialidade(m.especialidade)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
