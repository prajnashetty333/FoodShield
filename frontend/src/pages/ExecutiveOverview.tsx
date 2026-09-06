import React, { useEffect, useState } from 'react';
import { fetchOverview } from '../services/api';
import { OverviewResponse } from '../types';
import { KPICard } from '../components/KPICard';
import { ProfileBadge } from '../components/ProfileBadge';

const RESEARCH_PATHWAY = [
  { number: '01', title: 'EXPOSURE', description: 'Which countries and foods are vulnerable?', accent: '#1565c0' },
  { number: '02', title: 'SUBSTITUTION', description: 'Can existing suppliers replace the loss?', accent: '#0e9f6a' },
  { number: '03', title: 'HISTORICAL RESILIENCE', description: 'Can previous trade relationships provide a fallback?', accent: '#2bbf8a' },
  { number: '04', title: 'NEW ORIGINS', description: 'When are completely new suppliers required?', accent: '#2a7de1' },
  { number: '05', title: 'DETERMINANTS', description: 'What makes a country–food system resilient or fragile?', accent: '#e6a817' },
  { number: '06', title: 'SCENARIO ANALYSIS', description: 'How does resilience change under different assumptions?', accent: '#1565c0' },
];

function fmt(val: number | null | undefined, decimals = 2): string {
  if (val == null) return '--';
  return val.toFixed(decimals);
}

function fmtInt(val: number | null | undefined): string {
  if (val == null) return '--';
  return val.toLocaleString();
}

export const ExecutiveOverview = () => {
  const [data, setData] = useState<OverviewResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchOverview()
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-slate-400">Loading overview...</div>;
  if (error) return <div className="text-red-400">Error: {error}</div>;
  if (!data) return <div className="text-slate-400">No data available</div>;

  return (
    <div className="space-y-12">
      <header className="border-b border-slate-800 pb-12">
        <p className="text-xs font-semibold text-blue-400 uppercase tracking-[0.2em] mb-5">Food Trade Resilience Intelligence</p>
        <h1 className="text-5xl md:text-6xl font-normal text-slate-100 mb-4 tracking-tight">FOODSHIELD</h1>
        <p className="text-slate-300 text-xl font-light max-w-3xl leading-relaxed">
          Food Trade Resilience &amp; Supplier Disruption Intelligence
        </p>

        <div className="mt-9 max-w-4xl bg-blue-950/20 border border-blue-900/30 border-l-4 border-l-blue-600 p-6 md:p-8">
          <h2 className="text-xs font-medium text-blue-400 uppercase tracking-widest mb-3">Research Question</h2>
          <p className="text-2xl md:text-3xl text-slate-100 font-normal leading-snug">
            How resilient are countries to the disruption of their dominant food supplier, and what determines whether the lost supply can be replaced through existing trade relationships or requires new suppliers?
          </p>
          <p className="text-slate-400 text-base font-light leading-relaxed mt-4">
            FOODSHIELD evaluates supplier-disruption scenarios to determine whether lost food supply can be absorbed by existing trade networks, recovered through historical relationships, or requires new supplier origins.
          </p>
        </div>

        <div className="mt-8 grid grid-cols-2 lg:grid-cols-4 gap-3">
          <div className="bg-slate-900 border border-slate-800 border-t-2 border-t-blue-600 p-4 rounded-lg"><span className="block text-xs text-slate-500 uppercase tracking-widest mb-1">Period</span><span className="text-lg text-slate-100">2011–2023</span></div>
          <div className="bg-slate-900 border border-slate-800 border-t-2 border-t-[#0e9f6a] p-4 rounded-lg"><span className="block text-xs text-slate-500 uppercase tracking-widest mb-1">Scope</span><span className="text-lg text-slate-100">6 Commodities</span></div>
          <div className="bg-slate-900 border border-slate-800 border-t-2 border-t-[#2a7de1] p-4 rounded-lg"><span className="block text-xs text-slate-500 uppercase tracking-widest mb-1">Scenario</span><span className="text-lg text-slate-100">Rank-1 Supplier Shock</span></div>
          <div className="bg-slate-900 border border-slate-800 border-t-2 border-t-[#e6a817] p-4 rounded-lg"><span className="block text-xs text-slate-500 uppercase tracking-widest mb-1">Evidence</span><span className="text-lg text-slate-100">{fmtInt(data.total_scenarios)} Validated Scenarios</span></div>
        </div>
      </header>

      <section>
        <h2 className="text-xs font-medium text-slate-500 mb-6 uppercase tracking-widest">How We Answer the Question</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
          {RESEARCH_PATHWAY.map((stage) => (
            <article key={stage.number} className="bg-slate-900 border border-slate-800 border-l-4 p-6 rounded-lg shadow-sm transition-shadow hover:shadow-md" style={{ borderLeftColor: stage.accent }}>
              <div className="flex items-baseline gap-3 mb-3">
                <span className="text-2xl font-serif" style={{ color: stage.accent }}>{stage.number}</span>
                <h3 className="text-xs font-medium text-slate-300 uppercase tracking-widest">{stage.title}</h3>
              </div>
              <p className="text-sm text-slate-400 font-light leading-relaxed">{stage.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-xs font-medium text-slate-500 mb-6 uppercase tracking-widest">What We Found Globally</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KPICard title="Primary Scenarios" value={fmtInt(data.total_scenarios)} />
          <KPICard title="Mean Modeled Replacement" value={`${fmt(data.mean_replacement_rate)}%`} />
          <KPICard title="Type A — Current Network" value={`${fmt(data.type_a_percentage)}%`} />
          <KPICard title="Type C — New-origin Dependent" value={`${fmt(data.type_c_percentage)}%`} />
        </div>
      </section>

      <section>
        <h2 className="text-xs font-medium text-slate-500 mb-6 uppercase tracking-widest">Modeled Resilience Profiles</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {data.profile_distribution.map((dist) => (
            <div key={dist.profile} className="bg-slate-900 border border-slate-800 p-5 rounded-lg flex flex-col items-start justify-between min-h-[140px]">
              <ProfileBadge profile={dist.profile} showLabel className="mb-4" />
              <div className="w-full">
                <div className="text-2xl font-light text-slate-100">{fmt(dist.percentage)}%</div>
                <div className="text-xs text-slate-500 mt-1">{fmtInt(dist.count)} scenarios</div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-blue-950/20 border border-blue-900/30 p-8 rounded-lg">
        <h2 className="text-xl font-medium text-blue-400 mb-4">Core Interpretation</h2>
        <p className="text-slate-300 text-lg font-light leading-relaxed mb-4">
          Most modeled Rank-1 supplier shocks can be fully replaced using current-year supplier relationships under the historical export-expansion capacity proxy.
        </p>
        <p className="text-slate-400 text-sm">
          These results describe modeled trade-replacement feasibility, not guaranteed real-world food security.
        </p>
      </section>
    </div>
  );
};
