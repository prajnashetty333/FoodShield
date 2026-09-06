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

  if (loading) return <div className="text-muted animate-pulse">Loading sensitivity analysis...</div>;
  if (error) return <div className="border border-[#e23b2a] bg-[#e23b2a]/5 p-8 rounded-sm"><p className="text-[#e23b2a] font-light text-lg">Error: {error}</p></div>;
  if (!data) return <div className="text-muted">No data available</div>;

  return (
    <div className="space-y-16">
      <header className="border-b border-line pb-12">
        <p className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-4">06 &mdash; The Robustness</p>
        
        <div className="mb-8 p-6 bg-[#1565c0]/5 border-l-4 border-[#1565c0]">
          <div className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-2">RQ 5 &mdash; Sensitivity to Capacity</div>
          <h2 className="text-2xl font-serif text-ink mb-0">How sensitive are replacement outcomes to the assumed historical export-expansion capacity?</h2>
        </div>

        <h1 className="text-4xl md:text-5xl font-normal text-ink mb-6 font-serif">
          How much does the result depend on our assumptions?
        </h1>
        <p className="text-body text-xl font-light mb-8 max-w-3xl">
          Assessing the robustness of modeled resilience profiles when the Historical Export-Expansion Capacity (HEEC) proxy is scaled down.
        </p>

        <div className="bg-wash border-l-4 border-l-[#1565c0] p-6 max-w-4xl text-body text-sm leading-relaxed">
          <strong className="text-ink font-semibold">HEEC Note:</strong> HEEC is a historical export-expansion capacity proxy derived from past global outward trade. It should not be interpreted as guaranteed spare physical capacity or predicted future exports.
        </div>
      </header>

      <section>
        <h2 className="text-xs font-semibold text-ink mb-6 uppercase tracking-widest border-b border-line pb-2">What changes when the assumption changes?</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {HEEC_SCALES.map(({ label, experiment }) => {
            const sum = data.summaries.find(s => s.experiment === experiment);
            return (
              <div key={experiment} className="bg-paper border border-line p-6 rounded-md">
                <h3 className="text-xs font-semibold text-muted uppercase tracking-widest mb-6">{label}</h3>
                <div className="space-y-6">
                  <div>
                    <div className="text-[10px] text-muted uppercase tracking-widest mb-1 font-semibold">Mean Replacement</div>
                    <div className="text-3xl font-light text-ink">{sum ? fmt(sum.mean_replacement_rate) : '--'}%</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-muted uppercase tracking-widest mb-1 font-semibold">Current Network Share</div>
                    <div className="text-2xl font-light text-[#0e9f6a]">{sum ? fmt(sum.type_A_share) : '--'}%</div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="bg-wash p-8 rounded-sm border border-line">
        <h2 className="text-sm font-semibold text-ink mb-6 uppercase tracking-widest">
          Profile Transitions (100% HEEC → 25% HEEC)
        </h2>
        <p className="text-body text-lg font-light mb-8 leading-relaxed max-w-4xl">
          Restricting the HEEC proxy shifts more modeled importer–commodity–year scenarios toward less favorable replacement profiles.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <KPICard
            title="Type A to Type C Transitions"
            value={fmtInt(data.transitions_100_to_25.A_to_C)}
            subtitle="Scenarios losing current-network sufficiency"
            className="border-l-4 border-l-[#e6a817]"
          />
          <KPICard
            title="Type C to Type D Transitions"
            value={fmtInt(data.transitions_100_to_25.C_to_D)}
            subtitle="Scenarios becoming structurally constrained"
            className="border-l-4 border-l-[#e23b2a]"
          />
        </div>
      </section>

      <section className="bg-wash p-8 md:p-12 rounded-sm border border-line">
        <h2 className="text-sm font-semibold text-ink mb-4 uppercase tracking-widest">What this means</h2>
        <p className="text-body text-xl font-light leading-relaxed mb-6 font-serif">
          The modeled network structure is highly robust to HEEC proxy contractions. Even when the HEEC proxy is scaled to 25% of baseline,
          the vast majority of scenarios retain their original modeled resilience profiles.
        </p>
        <div className="text-xs text-muted border-t border-[#d7e2ec] pt-4 max-w-2xl">
          <strong>Limitation:</strong> These are modeled outcomes under specified historical trade assumptions — not predictions of real-world food security or actual available export volume during a crisis.
        </div>
      </section>
    </div>
  );
};
