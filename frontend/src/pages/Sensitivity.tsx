import React, { useEffect, useState } from 'react';
import { fetchSensitivity } from '../services/api';
import { SensitivityAnalysisResponse } from '../types';
import { KPICard } from '../components/KPICard';

function fmt(val: number | null | undefined, decimals = 2): string {
  if (val == null) return '--';
  return val.toFixed(decimals);
}

function fmtInt(val: number | null | undefined): string {
  if (val == null) return '--';
  return val.toLocaleString();
}

const HEEC_SCALES = [
  { scale: 1.00, label: '100% HEEC', experiment: 'A_W0_1.00' },
  { scale: 0.75, label: '75% HEEC', experiment: 'A_W0_0.75' },
  { scale: 0.50, label: '50% HEEC', experiment: 'A_W0_0.50' },
  { scale: 0.25, label: '25% HEEC', experiment: 'A_W0_0.25' },
];

export const Sensitivity = () => {
  const [data, setData] = useState<SensitivityAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchSensitivity()
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-slate-400 animate-pulse">Loading sensitivity analysis...</div>;
  if (error) return <div className="text-red-400">Error: {error}</div>;
  if (!data) return <div className="text-slate-400">No data available</div>;

  return (
    <div className="space-y-12">
      <header className="border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-light text-slate-100 mb-2">Sensitivity Analysis</h1>
        <p className="text-slate-400 font-light">
          Assessing the robustness of modeled resilience profiles when the Historical Export-Expansion Capacity (HEEC) proxy is scaled down.
        </p>
      </header>

      <div className="bg-blue-950/10 border border-blue-900/20 p-4 rounded text-slate-400 text-sm leading-relaxed">
        <strong className="text-blue-400">HEEC Note:</strong> HEEC is a historical export-expansion capacity proxy derived from past global outward trade. It should not be interpreted as guaranteed spare physical capacity or predicted future exports.
      </div>

      <section>
        <h2 className="text-xs font-medium text-slate-500 mb-6 uppercase tracking-widest">HEEC Scaling Experiments (Primary Scope: Rank 1)</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {HEEC_SCALES.map(({ label, experiment }) => {
            const sum = data.summaries.find(s => s.experiment === experiment);
            return (
              <div key={experiment} className="bg-slate-900 border border-slate-800 p-6 rounded-lg">
                <h3 className="text-sm font-medium text-slate-300 mb-5">{label}</h3>
                <div className="space-y-4">
                  <div>
                    <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">Mean Modeled Replacement</div>
                    <div className="text-2xl font-light text-slate-100">{sum ? fmt(sum.mean_replacement_rate) : '--'}%</div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">Type A Share</div>
                    <div className="text-xl font-light text-green-400">{sum ? fmt(sum.type_A_share) : '--'}%</div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="bg-slate-900 border border-slate-800 p-8 rounded-lg">
        <h2 className="text-xs font-medium text-slate-500 mb-6 uppercase tracking-widest">
          Profile Transitions — 100% HEEC to 25% HEEC
        </h2>
        <p className="text-slate-400 text-sm mb-6 leading-relaxed">
          Restricting the HEEC proxy shifts more modeled importer–commodity–year scenarios toward less favorable replacement profiles.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <KPICard
            title="Type A to Type C Transitions"
            value={fmtInt(data.transitions_100_to_25.A_to_C)}
            subtitle="Scenarios losing current-network sufficiency under 25% HEEC"
            className="border-orange-500/30"
          />
          <KPICard
            title="Type C to Type D Transitions"
            value={fmtInt(data.transitions_100_to_25.C_to_D)}
            subtitle="Scenarios becoming structurally constrained under 25% HEEC"
            className="border-red-500/30"
          />
        </div>
      </section>

      <section className="bg-blue-950/20 border border-blue-900/30 p-8 rounded-lg">
        <h2 className="text-xl font-medium text-blue-400 mb-4">Core Finding</h2>
        <p className="text-slate-300 text-lg font-light leading-relaxed">
          The modeled network structure is highly robust to HEEC proxy contractions. Even when the HEEC proxy is scaled to 25% of baseline,
          the vast majority of scenarios retain their original modeled resilience profiles, and mean modeled replacement rates remain above 98.9%.
        </p>
        <p className="text-slate-500 text-sm mt-4">
          These are modeled outcomes under specified historical trade assumptions — not predictions of real-world food security.
        </p>
      </section>
    </div>
  );
};
