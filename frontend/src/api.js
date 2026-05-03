export const api = {
  // Médicos
  // caminhos relativos usados são interceptados pelo proxy do react, em setupProxy.js
  getMedicos: () => fetch('/medicos/').then(r => r.json()), 
  getEspecialidades: () => fetch('/especialidades/').then(r => r.json()),
  createMedico: (data) =>
    fetch('/medicos/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(r => r.json()),
  deleteMedico: (id) => fetch(`/medicos/${id}/`, { method: 'DELETE' }),

  // Agendas
  getAgendas: () => fetch('/agendas/').then(r => r.json()),
  createAgenda: (data) =>
    fetch('/agendas/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(r => r.json()),
  deleteAgenda: (id) => fetch(`/agendas/${id}/`, { method: 'DELETE' }),

  // Agendamentos
  getAgendamentos: () => fetch('/agendamentos/').then(r => r.json()),
  createAgendamento: (data) =>
    fetch('/agendamentos/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(r => r.json()),
  deleteAgendamento: (id) =>
    fetch(`/agendamentos/${id}/`, { method: 'DELETE' }),
};
