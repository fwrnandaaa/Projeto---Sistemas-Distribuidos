const MEDICOS_API = '';
const AGENDAMENTOS_API = '';

export const api = {
  // Médicos
  getMedicos: () => fetch(`${MEDICOS_API}/medicos/`).then(r => r.json()),
  getEspecialidades: () => fetch(`${MEDICOS_API}/especialidades/`).then(r => r.json()),

  // Agendas
  getAgendas: () => fetch(`${AGENDAMENTOS_API}/agendas/`).then(r => r.json()),
  createAgenda: (data) =>
    fetch(`${AGENDAMENTOS_API}/agendas/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(r => r.json()),
  deleteAgenda: (id) => fetch(`${AGENDAMENTOS_API}/agendas/${id}/`, { method: 'DELETE' }),

  // Agendamentos
  getAgendamentos: () => fetch(`${AGENDAMENTOS_API}/agendamentos/`).then(r => r.json()),
  createAgendamento: (data) =>
    fetch(`${AGENDAMENTOS_API}/agendamentos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(r => r.json()),
  deleteAgendamento: (id) =>
    fetch(`${AGENDAMENTOS_API}/agendamentos/${id}/`, { method: 'DELETE' }),
};
