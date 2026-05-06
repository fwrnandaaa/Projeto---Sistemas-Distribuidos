export function extractLinks(data) {
  if (!data || typeof data !== 'object') return {};
  const raw = data._links || {};
  const result = {};
  for (const [rel, value] of Object.entries(raw)) {
    if (!value) continue;
    result[rel] = {
      href: typeof value === 'string' ? value : value.href,
      method: value.method?.toUpperCase() ?? 'GET',
    };
  }
  return result;
}

export async function followLink(link, body = null) {
  const options = { method: link.method || 'GET', headers: { 'Content-Type': 'application/json' } };
  if (body && options.method !== 'GET') options.body = JSON.stringify(body);
  const res = await fetch(link.href, options);
  if (res.status === 204) return null;
  if (!res.ok) throw new Error(`Erro ${res.status}`);
  return res.json();
}