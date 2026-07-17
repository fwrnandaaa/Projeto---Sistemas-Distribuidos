import { useEffect, useState } from 'react';
import { api } from '../../api';

export default function Relatorios() {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState('');

  const carregar = async () => {
    setLoading(true);
    setErro('');
    try {
      setDados(await api.getDashboardRelatorios());
    } catch {
      setErro('Não foi possível carregar o dashboard. Verifique se o gateway e o serviço gRPC de relatórios estão em execução.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { carregar(); }, []);

  if (loading) return <p className="info">Carregando dados do serviço de relatórios...</p>;

  return (
    <section className="card">
      <div className="dashboard-cabecalho">
        <div>
          <h2>Dashboard de Relatórios</h2>
          <p className="dashboard-descricao">
            Dados consolidados pelo serviço gRPC a partir dos microsserviços de médicos e agendamentos.
          </p>
        </div>
        <button className="btn-atualizar" onClick={carregar}>Atualizar</button>
      </div>

      {erro ? (
        <p className="erro">{erro}</p>
      ) : (
        <div className="dashboard-grade">
          <article className="indicador">
            <span>Total de médicos</span>
            <strong>{dados.total_medicos}</strong>
          </article>
          <article className="indicador">
            <span>Total de consultas</span>
            <strong>{dados.total_consultas}</strong>
          </article>
          <article className="indicador">
            <span>Consultas hoje</span>
            <strong>{dados.consultas_hoje}</strong>
          </article>
          <article className="indicador indicador-texto">
            <span>Especialidade mais procurada</span>
            <strong>{dados.especialidade_mais_procurada}</strong>
          </article>
          <article className="indicador indicador-texto">
            <span>Médico mais procurado</span>
            <strong>{dados.medico_mais_procurado}</strong>
          </article>
        </div>
      )}
    </section>
  );
}
