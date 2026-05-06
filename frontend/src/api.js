import { extractLinks, followLink } from './lib/hateoasClient';

export const api = {
  // Médicos
  getMedicos: () =>
    fetch('/medicos/').then(r => r.json()).then(data => data.map(item => ({
      ...item,
      links: extractLinks(item),
    }))),

  getEspecialidades: () =>
    fetch('/especialidades/').then(r => r.json()).then(data => data.map(item => ({
      ...item,
      links: extractLinks(item),
    }))),

  createMedico: (data) =>
    fetch('/medicos/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(r => r.json()).then(item => ({ ...item, links: extractLinks(item) })),

  deleteMedico: (id) => fetch(`/medicos/${id}/`, { method: 'DELETE' }),

  // Agendas
  getAgendas: () =>
    fetch('/agendas/').then(r => r.json()).then(data => data.map(item => ({
      ...item,
      links: extractLinks(item),
    }))),

  createAgenda: (data) =>
    fetch('/agendas/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(r => r.json()).then(item => ({ ...item, links: extractLinks(item) })),

  deleteAgenda: (id) => fetch(`/agendas/${id}/`, { method: 'DELETE' }),

  // Agendamentos
  getAgendamentos: () =>
    fetch('/agendamentos/').then(r => r.json()).then(data => data.map(item => ({
      ...item,
      links: extractLinks(item),
    }))),

  createAgendamento: (data) =>
    fetch('/agendamentos/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(r => r.json()).then(item => ({ ...item, links: extractLinks(item) })),

  deleteAgendamento: (id) =>
    fetch(`/agendamentos/${id}/`, { method: 'DELETE' }),

  // Seguir qualquer link HATEOAS diretamente
  follow: followLink,
};