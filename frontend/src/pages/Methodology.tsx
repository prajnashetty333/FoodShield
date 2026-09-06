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

  if (loading) return <div className="text-slate-400">Loading methodology limitations...</div>;
  if (error) return <div className="text-red-400">Error: {error}</div>;
  if (!data) return <div className="text-slate-400">No data available</div>;

  return (
    <div className="space-y-12">
      <header className="border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-light text-slate-100 mb-2">Methodology Limitations</h1>
        <p className="text-slate-400 font-light">
          Factors explicitly excluded from the FOODSHIELD modeling framework.
        </p>
      </header>

      <div className="bg-slate-900 border border-slate-800 p-8 rounded-lg">
        <h2 className="text-xl font-medium text-slate-200 mb-6">What FOODSHIELD Does Not Model</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.limitations.map((limitation, idx) => (
            <div key={idx} className="flex items-center space-x-3 p-3 rounded bg-slate-950 border border-slate-800/50">
              <span className="text-red-500 font-bold">×</span>
              <span className="text-slate-300 font-light">{limitation}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-blue-950/20 border border-blue-900/30 p-8 rounded-lg">
        <h2 className="text-xl font-medium text-blue-400 mb-4">Core Disclaimer</h2>
        <p className="text-slate-300 text-lg font-light leading-relaxed">
          {data.disclaimer}
        </p>
      </div>
    </div>
  );
};
