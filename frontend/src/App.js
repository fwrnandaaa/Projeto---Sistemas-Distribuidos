import { useState } from 'react';
import './App.css';
import Medicos from './components/Medicos';
import Agendas from './components/Agendas';
import Agendamentos from './components/Agendamentos';
import NovoAgendamento from './components/NovoAgendamento';

const ABAS = [
  { id: 'marcar', label: 'Marcar Consulta' },
  { id: 'agendamentos', label: 'Consultas Agendadas' },
  { id: 'agendas', label: 'Gerenciar Agendas' },
  { id: 'medicos', label: 'Médicos' },
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
        {abaAtiva === 'marcar' && <NovoAgendamento onSucesso={() => setAbaAtiva('agendamentos')} />}
        {abaAtiva === 'agendamentos' && <Agendamentos />}
        {abaAtiva === 'agendas' && <Agendas />}
        {abaAtiva === 'medicos' && <Medicos />}
      </main>
    </div>
  );
}

export default App;
