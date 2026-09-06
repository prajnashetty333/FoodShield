import React, { useEffect, useState } from 'react';
import { fetchMethodology } from '../services/api';
import { MethodologyResponse } from '../types';

export const Methodology = () => {
  const [data, setData] = useState<MethodologyResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMethodology()
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-muted animate-pulse">Loading methodology limitations...</div>;
  if (error) return <div className="border border-[#e23b2a] bg-[#e23b2a]/5 p-8 rounded-sm"><p className="text-[#e23b2a] font-light text-lg">Error: {error}</p></div>;
  if (!data) return <div className="text-muted">No data available</div>;

  return (
    <div className="space-y-16 max-w-4xl">
      <header className="border-b border-line pb-12">
        <h1 className="text-4xl md:text-5xl font-normal text-ink mb-6 font-serif">
          What we don't know
        </h1>
        <p className="text-body text-xl font-light mb-8 max-w-3xl">
          Factors explicitly excluded from the FOODSHIELD modeling framework.
        </p>

        <div className="bg-wash border-l-4 border-l-[#e23b2a] p-6 text-body text-sm leading-relaxed">
          <strong className="text-ink font-semibold">Core Disclaimer:</strong> {data.disclaimer}
        </div>
      </header>

      <div className="bg-paper">
        <h2 className="text-sm font-semibold text-ink uppercase tracking-widest mb-8 border-b border-line pb-2">What FOODSHIELD Does Not Model</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
          {data.limitations.map((limitation, idx) => (
            <div key={idx} className="flex items-start">
              <span className="text-[#e23b2a] font-serif text-lg mr-4 mt-0.5">—</span>
              <span className="text-body font-light text-lg leading-relaxed font-serif">{limitation}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
