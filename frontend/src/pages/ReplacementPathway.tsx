import React, { useEffect, useState } from 'react';
import { fetchCountryOptions, fetchReplacementAnalysis } from '../services/api';
import { CountryOptions, ReplacementAnalysisResponse } from '../types';
import { KPICard } from '../components/KPICard';
import Plot from 'react-plotly.js';

const PRIMARY_SHOCK_RANK = 1;

function fmt(val: number | null | undefined, decimals = 1): string {
  if (val == null) return '--';
  return val.toFixed(decimals);
}

function fmtLocale(val: number | null | undefined): string {
  if (val == null) return '--';
  return val.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

export const ReplacementPathway = () => {
  const [options, setOptions] = useState<CountryOptions | null>(null);
  
  const [country, setCountry] = useState<string>('');
  const [commodity, setCommodity] = useState<string>('');
  const [year, setYear] = useState<number>(0);
  
  const [data, setData] = useState<ReplacementAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCountryOptions().then(res => {
      setOptions(res);
      if (res.countries.length > 0) setCountry(res.countries[0]);
      if (res.commodities.length > 0) setCommodity(res.commodities[0]);
      if (res.years.length > 0) setYear(res.years[res.years.length - 1]);
    });
  }, []);

  useEffect(() => {
    if (!country || !commodity || !year) return;
    
    setLoading(true);
    setError(null);
    fetchReplacementAnalysis(country, commodity, year, PRIMARY_SHOCK_RANK)
      .then(setData)
      .catch(err => {
        setData(null);
        if (err.response?.status === 404) {
           setError('No validated FOODSHIELD observation for the primary Rank-1 shock.');
        } else {
           setError(err.message);
        }
      })
      .finally(() => setLoading(false));
  }, [country, commodity, year]);

  // Only render Sankey if all four flow values are non-null
  const canRenderSankey = data &&
    data.tier1_replacement != null &&
    data.tier2_replacement != null &&
    data.tier3_replacement != null &&
    data.unreplaced_supply != null;

  return (
    <div className="space-y-8">
      <header className="border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-light text-slate-100 mb-2">Replacement Pathway</h1>
        <p className="text-slate-400 font-light">
          Modeled trade-replacement pathway — how lost import supply is allocated across Tier 1, 2, and 3 supplier capacities.
        </p>
      </header>

      <div className="flex flex-wrap gap-4 bg-slate-900 border border-slate-800 p-4 rounded-lg">
        <div className="flex-1 min-w-[150px]">
          <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">Country</label>
          <select
            className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded p-2 outline-none"
            value={country} onChange={(e) => setCountry(e.target.value)}
          >
            {options?.countries.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        
        <div className="flex-1 min-w-[150px]">
          <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">Commodity</label>
          <select
            className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded p-2 outline-none"
            value={commodity} onChange={(e) => setCommodity(e.target.value)}
          >
            {options?.commodities.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div className="w-28">
          <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">Year</label>
          <select
            className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded p-2 outline-none"
            value={year} onChange={(e) => setYear(Number(e.target.value))}
          >
            {options?.years.map(y => <option key={y} value={y}>{y}</option>)}
          </select>
        </div>
        
        <div className="w-40">
          <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">Shock Rank</label>
          <div className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded p-2">
            Rank 1 (Primary)
          </div>
        </div>
      </div>

      <p className="text-slate-500 text-sm leading-relaxed">
        Replacement Pathway uses the primary Rank-1 supplier shock. Rank-2 and Rank-3 shocks are evaluated independently on the Supplier Shock page and are not part of the primary replacement pathway analysis.
      </p>

      {loading && <div className="text-slate-400 py-12 text-center animate-pulse">Querying validated replacement dataset...</div>}
      
      {error && (
        <div className="bg-slate-900 border border-slate-800 p-8 rounded-lg text-center">
          <p className="text-slate-400 font-light text-lg">{error}</p>
        </div>
      )}

      {data && !loading && (
        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <KPICard
              title="Modeled Replacement Rate"
              value={`${fmt(data.replacement_rate)}%`}
              className={(data.replacement_rate ?? 0) >= 99 ? 'border-green-900/30 bg-green-950/10' : ''}
            />
            <KPICard title="Tier 1 Replacement" value={fmtLocale(data.tier1_replacement)} subtitle="Current-year suppliers (tonnes)" />
            <KPICard title="Tier 2 Replacement" value={fmtLocale(data.tier2_replacement)} subtitle="Historical suppliers (tonnes)" />
            <KPICard title="Tier 3 Replacement" value={fmtLocale(data.tier3_replacement)} subtitle="New-origin suppliers (tonnes)" />
          </div>

          {canRenderSankey ? (
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg w-full overflow-x-auto">
              <h3 className="text-xs font-medium text-slate-500 uppercase tracking-widest mb-2">
                Modeled replacement of lost import supply
              </h3>
              <p className="text-slate-500 text-xs mb-6">
                Source: validated replacement results dataset. Tonnes.
              </p>
              <div className="min-w-[700px]">
                <Plot
                  data={[{
                    type: 'sankey',
                    orientation: 'h',
                    node: {
                      pad: 15,
                      thickness: 30,
                      line: { color: '#0f172a', width: 0.5 },
                      label: ['Lost Supply', 'Tier 1 — Current suppliers', 'Tier 2 — Historical suppliers', 'Tier 3 — New origins', 'Unreplaced'],
                      color: ['#ef4444', '#3b82f6', '#f59e0b', '#8b5cf6', '#64748b']
                    },
                    link: {
                      source: [0, 0, 0, 0],
                      target: [1, 2, 3, 4],
                      value: [
                        data.tier1_replacement ?? 0,
                        data.tier2_replacement ?? 0,
                        data.tier3_replacement ?? 0,
                        data.unreplaced_supply ?? 0
                      ],
                      color: ['rgba(59,130,246,0.3)', 'rgba(245,158,11,0.3)', 'rgba(139,92,246,0.3)', 'rgba(100,116,139,0.3)']
                    }
                  }]}
                  layout={{
                    width: 800,
                    height: 420,
                    margin: { l: 20, r: 20, t: 10, b: 10 },
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    font: { color: '#94a3b8', family: 'Inter, sans-serif', size: 12 }
                  }}
                  config={{ responsive: true, displayModeBar: false }}
                />
              </div>
            </div>
          ) : (
            <div className="bg-slate-900 border border-slate-800 p-8 rounded-lg text-center">
              <p className="text-slate-400">Sankey diagram cannot be rendered: one or more flow values are missing from the validated dataset.</p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <KPICard title="Unreplaced Supply" value={fmtLocale(data.unreplaced_supply)} subtitle="tonnes — modeled gap after all tiers" />
            <KPICard title="New-Origin Share" value={`${fmt(data.new_origin_share)}%`} subtitle="Share sourced from Tier 3 new origins" />
          </div>
        </div>
      )}
    </div>
  );
};
