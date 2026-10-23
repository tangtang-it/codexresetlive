// Cloudflare Worker entrypoint with Static Assets binding
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // 1. Intercept /api/radar
    if (url.pathname === '/api/radar') {
      const headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'public, max-age=30, s-maxage=30'
      };

      const UPSTREAM_URL = 'https://willcodexreset.com/api/reset-radar';
      try {
        const upstreamRes = await fetch(UPSTREAM_URL, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json'
          },
          cf: { cacheTtl: 30, cacheEverything: true }
        });

        if (upstreamRes.ok) {
          const raw = await upstreamRes.json();
          const data = raw.data || raw;

          // Extract posts from tiboPosts
          const tiboPosts = (data.tiboPosts || []).map(p => ({
            id: String(p.id || '').replace(/^tibo-/, ''),
            at: p.occurredAt || p.at || new Date().toISOString(),
            type: (p.detail || p.title || '').toLowerCase().includes('reset') ? 'release' : 'regular',
            status: 'confirmed',
            text: p.detail || p.title || '',
            url: p.url || ('https://x.com/thsottiaux/status/' + String(p.id || '').replace(/^tibo-/, ''))
          }));

          const relevantPosts = (data.tiboRelevantPosts || []).map(p => ({
            id: String(p.id || '').replace(/^tibo-/, ''),
            at: p.occurredAt || p.at,
            text: p.detail || p.title || '',
            url: p.url || ('https://x.com/thsottiaux/status/' + String(p.id || '').replace(/^tibo-/, '')),
            rationale: p.resetCandidateRationale || ''
          }));

          // Extract verified reset events (e.g. manual or automated verified resets)
          let latestReset = null;
          if (Array.isArray(data.events)) {
            const resets = data.events.filter(e => e && (e.kind === 'reset' || e.resetType) && e.verified !== false);
            if (resets.length > 0) {
              const r = resets[0];
              latestReset = {
                id: String(r.id || ''),
                at: r.occurredAt || r.at || '',
                title: r.title || 'Direct quota reset',
                detail: r.detail || '',
                verified: Boolean(r.verified),
                type: r.resetType || 'usage'
              };
            }
          }

          const payload = {
            code: 0,
            source: 'edge-live',
            updatedAt: data.updatedAt || new Date().toISOString(),
            probability48h: typeof data.probability48h === 'number' ? data.probability48h : null,
            verdict: data.verdict || 'watching',
            latestReset: latestReset,
            lastResetAt: latestReset ? latestReset.at : null,
            latestRelevant: relevantPosts[0] || null,
            posts: tiboPosts.slice(0, 15)
          };

          return new Response(JSON.stringify(payload), { status: 200, headers });
        }
      } catch (err) {
        // Fallback gracefully without throwing
      }

      // Safe fallback when upstream is unavailable - do not invent false probability or user numbers
      return new Response(JSON.stringify({
        code: 0,
        source: 'edge-fallback',
        updatedAt: new Date().toISOString(),
        probability48h: null,
        verdict: 'unavailable',
        posts: []
      }), { status: 200, headers });
    }

    // 2. Delegate all other routes to Static Assets binding
    if (env.ASSETS) {
      return env.ASSETS.fetch(request);
    }
    return new Response('Asset binding not found', { status: 500 });
  }
};
