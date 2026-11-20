import React, { useState } from 'react';

interface Citation {
  chunk_id: string;
  source_name: string;
  text: string;
  score: number;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  latency?: number;
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Welcome to Enterprise RAG Assistant. Ask me anything grounded in our architectural policies and compliance blueprints!'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/v1/chat/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMsg, top_k: 3 })
      });
      const data = await res.json();
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.answer,
          citations: data.citations,
          latency: data.latency_ms
        }
      ]);
    } catch {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Connection to local RAG backend failed. Please verify FastAPI is running on port 8000.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', maxWidth: 900, margin: '40px auto', padding: '0 20px' }}>
      <header style={{ borderBottom: '1px solid #e2e8f0', paddingBottom: 16, marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 700, margin: 0 }}>🏢 Enterprise RAG Document Assistant</h1>
        <p style={{ color: '#64748b', fontSize: 14, margin: '6px 0 0 0' }}>Grounded retrieval with source citations & microservice architecture.</p>
      </header>

      <div style={{ minHeight: 400, background: '#f8fafc', borderRadius: 8, padding: 20, marginBottom: 20, overflowY: 'auto' }}>
        {messages.map((m, idx) => (
          <div key={idx} style={{ marginBottom: 16, display: 'flex', flexDirection: 'column', alignItems: m.role === 'user' ? 'flex-end' : 'flex-start' }}>
            <div style={{
              maxWidth: '80%',
              padding: '12px 16px',
              borderRadius: 8,
              background: m.role === 'user' ? '#3b82f6' : '#ffffff',
              color: m.role === 'user' ? '#ffffff' : '#0f172a',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
              <p style={{ margin: 0, whiteSpace: 'pre-wrap' }}>{m.content}</p>
              {m.latency && <small style={{ display: 'block', marginTop: 8, color: '#94a3b8' }}>⚡ Retrieved in {m.latency}ms</small>}
            </div>

            {m.citations && m.citations.length > 0 && (
              <div style={{ maxWidth: '80%', marginTop: 8, background: '#f1f5f9', padding: '10px 14px', borderRadius: 6, fontSize: 13 }}>
                <strong>Verified Sources:</strong>
                <ul style={{ margin: '6px 0 0 16px', padding: 0 }}>
                  {m.citations.map(c => (
                    <li key={c.chunk_id}>
                      <strong>{c.source_name}</strong> (Relevance: {c.score}): <em>"{c.text.slice(0, 100)}..."</em>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
        {loading && <p style={{ color: '#64748b' }}>🔍 Retrieving verified documentation chunks...</p>}
      </div>

      <form onSubmit={handleSend} style={{ display: 'flex', gap: 12 }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask a question (e.g., 'What is our encryption and key management policy?')..."
          style={{ flex: 1, padding: '12px 16px', borderRadius: 6, border: '1px solid #cbd5e1', fontSize: 15 }}
        />
        <button type="submit" style={{ padding: '12px 24px', background: '#3b82f6', color: '#fff', border: 'none', borderRadius: 6, fontWeight: 600, cursor: 'pointer' }}>
          Query RAG
        </button>
      </form>
    </div>
  );
}
