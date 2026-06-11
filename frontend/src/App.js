import { useState } from 'react';
import './App.css';
import Medicos from './components/paginas/Medicos';
import Agendas from './components/paginas/Agendas';
import Agendamentos from './components/paginas/Agendamentos';
import NovoAgendamento from './components/paginas/NovoAgendamento';
import GerenciarMedicos from './components/paginas/GerenciarMedicos';
import Convenio from './components/paginas/Convenio';
import NotificacoesWebSocket from './components/NotificacoesWebSocket';

const ABAS = [
  { id: 'marcar', label: 'Marcar Consulta' },
  { id: 'agendamentos', label: 'Consultas Agendadas' },
  { id: 'agendas', label: 'Gerenciar Agendas' },
  { id: 'medicos', label: 'Médicos' },
  { id: 'gerenciar-medicos', label: 'Gerenciar Médicos' },
  { id: 'convenio', label: 'Convênio' },
];

function App() {
  const [abaAtiva, setAbaAtiva] = useState('marcar');

  return (
    <div className="App">
      <header className="app-header">
        <h1>Sistema de Agendamento de Consultas</h1>
        <nav className="nav-abas">
          {ABAS.map(aba => (
            <button
              key={aba.id}
              className={`aba-btn${abaAtiva === aba.id ? ' ativa' : ''}`}
              onClick={() => setAbaAtiva(aba.id)}
            >
              {aba.label}
            </button>
          ))}
        </nav>
      </header>
            
      <main className="conteudo">
          <NotificacoesWebSocket />
        {abaAtiva === 'marcar' && <NovoAgendamento onSucesso={() => setAbaAtiva('agendamentos')} />}
        {abaAtiva === 'agendamentos' && <Agendamentos />}
        {abaAtiva === 'agendas' && <Agendas />}
        {abaAtiva === 'convenio' && <Convenio />}
        {abaAtiva === 'medicos' && ( <Medicos onVerAgendamentos={() => setAbaAtiva('agendamentos')} /> )}
        {abaAtiva === 'gerenciar-medicos' && <GerenciarMedicos />}
      </main>
    </div>
  );
}

export default App;
