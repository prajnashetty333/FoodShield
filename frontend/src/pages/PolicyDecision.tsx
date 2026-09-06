import React, { useEffect, useState } from 'react';
import { fetchPolicy } from '../services/api';
import { PolicyResponse } from '../types';
import { ProfileBadge } from '../components/ProfileBadge';

export const PolicyDecision = () => {
  const [data, setData] = useState<PolicyResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPolicy()
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-slate-400">Loading policy framework...</div>;
  if (error) return <div className="text-red-400">Error: {error}</div>;
  if (!data) return <div className="text-slate-400">No data available</div>;

  return (
    <div className="space-y-12">
      <header className="border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-light text-slate-100 mb-2">Policy & Decision Support (Step 9)</h1>
        <p className="text-slate-400 font-light">
          Decision-support implications of the modeled trade-replacement framework.
        </p>
      </header>

      <div className="bg-amber-950/20 border border-amber-900/30 p-6 rounded-lg text-amber-400/90 text-sm font-medium">
        Disclaimer: {data.disclaimer}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {data.framework.map(rec => (
          <div key={rec.profile} className="bg-slate-900 border border-slate-800 p-8 rounded-lg flex flex-col h-full">
            <div className="mb-6">
              <ProfileBadge profile={rec.profile} showLabel className="text-sm px-3 py-1.5" />
            </div>
            
            <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-4">Strategic Directions</h3>
            
            <ul className="space-y-3 flex-1">
              {rec.directions.map((dir, idx) => (
                <li key={idx} className="flex items-start text-slate-300">
                  <span className="text-blue-500 mr-3 mt-1">•</span>
                  <span className="leading-relaxed font-light">{dir}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};
