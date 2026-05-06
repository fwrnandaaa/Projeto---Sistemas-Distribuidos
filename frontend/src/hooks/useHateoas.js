import { useState, useCallback } from "react";
import { extractLinks, followLink } from "../lib/hateoasClient";

export function useHateoas() {
  const [resource, setResource]   = useState(null);
  const [links, setLinks]         = useState({});
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState(null);

  // Carrega qualquer resposta e registra os links
  const load = useCallback(async (promiseOrData) => {
    setLoading(true);
    setError(null);
    try {
      const data = typeof promiseOrData?.then === "function"
        ? await promiseOrData
        : promiseOrData;

      // Lista retorna array — pega os links do primeiro item se existir
      if (Array.isArray(data)) {
        setResource(data);
        setLinks(data.length > 0 ? extractLinks(data[0]) : {});
      } else {
        setResource(data);
        setLinks(extractLinks(data));
      }
      return data;
    } catch (e) {
      setError(e);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  // Segue um link HATEOAS pelo rel (ex: "self", "agendamentos", "collection")
  const navigate = useCallback(async (rel, body = null) => {
    if (!links[rel]) {
      console.warn(`[HATEOAS] rel "${rel}" não disponível. Links atuais:`, links);
      return null;
    }
    return load(followLink(links[rel], body));
  }, [links, load]);

  const hasLink   = (rel) => rel in links;
  const getLink   = (rel) => links[rel] ?? null;

  return { resource, links, loading, error, load, navigate, hasLink, getLink };
}