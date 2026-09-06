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
    <div className="space-y-16">
      <header className="border-b border-line pb-12">
        <p className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-4">05 &mdash; The Recovery</p>
        
        <div className="flex flex-col md:flex-row gap-6 mb-8">
          <div className="flex-1 p-6 bg-[#1565c0]/5 border-l-4 border-[#1565c0]">
            <div className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-2">RQ 3 &mdash; Replacement Pathway</div>
            <h2 className="text-xl font-serif text-ink mb-0">When a major supplier disappears, where does replacement come from?</h2>
          </div>
          <div className="flex-1 p-6 bg-[#1565c0]/5 border-l-4 border-[#1565c0]">
            <div className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-2">RQ 4 &mdash; Recovery Pathways</div>
            <h2 className="text-xl font-serif text-ink mb-0">What proportion of modeled supplier shocks fall into each recovery pathway?</h2>
          </div>
        </div>

        <h1 className="text-4xl md:text-5xl font-normal text-ink mb-6 font-serif">
          Can existing suppliers absorb the disruption?
        </h1>
        <p className="text-body text-xl font-light mb-8 max-w-3xl">
          Modeled trade-replacement pathway — mapping how lost import supply is allocated across Tier 1, 2, and 3 supplier capacities.
        </p>

        <div className="flex flex-wrap gap-x-12 gap-y-6 max-w-4xl">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">WHO ARE WE TESTING?</label>
            <select
              className="w-full bg-paper border-b border-line text-ink text-xl py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
              value={country} onChange={(e) => setCountry(e.target.value)}
            >
              {options?.countries.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">WHAT FOOD?</label>
            <select
              className="w-full bg-paper border-b border-line text-ink text-xl py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
              value={commodity} onChange={(e) => setCommodity(e.target.value)}
            >
              {options?.commodities.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          <div className="w-28">
            <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">YEAR</label>
            <select
              className="w-full bg-paper border-b border-line text-ink text-xl py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
              value={year} onChange={(e) => setYear(Number(e.target.value))}
            >
              {options?.years.map(y => <option key={y} value={y}>{y}</option>)}
            </select>
          </div>
          
          <div className="w-40">
            <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">SHOCK RANK</label>
            <div className="w-full bg-paper border-b border-line text-ink text-xl py-2 opacity-70">
              Rank 1 (Primary)
            </div>
          </div>
        </div>
      </header>

      {loading && <div className="text-muted py-12 text-center animate-pulse">Querying validated replacement dataset...</div>}
      
      {error && (
        <div className="border border-[#e23b2a] bg-[#e23b2a]/5 p-8 rounded-sm text-center">
          <p className="text-[#e23b2a] font-light text-lg">{error}</p>
        </div>
      )}

      {data && !loading && (
        <div className="space-y-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <KPICard
              title="Modeled Replacement Rate"
              value={`${fmt(data.replacement_rate)}%`}
              className={(data.replacement_rate ?? 0) >= 99 ? 'border-l-4 border-l-[#0e9f6a]' : ''}
            />
            <KPICard title="Tier 1 Replacement" value={fmtLocale(data.tier1_replacement)} subtitle="Current-year suppliers (tonnes)" />
            <KPICard title="Tier 2 Replacement" value={fmtLocale(data.tier2_replacement)} subtitle="Historical suppliers (tonnes)" />
            <KPICard title="Tier 3 Replacement" value={fmtLocale(data.tier3_replacement)} subtitle="New-origin suppliers (tonnes)" />
          </div>

          {canRenderSankey ? (
            <div className="border-t border-line pt-12 w-full overflow-x-auto">
              <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-2">
                Modeled replacement of lost import supply
              </h3>
              <p className="text-muted text-xs mb-8">
                Source: validated replacement results dataset. Measured in tonnes.
              </p>
              <div className="min-w-[700px]">
                <Plot
                  data={[{
                    type: 'sankey',
                    orientation: 'h',
                    node: {
                      pad: 15,
                      thickness: 30,
                      line: { color: '#0a2540', width: 0.5 },
                      label: ['Lost Supply', 'Tier 1 — Current suppliers', 'Tier 2 — Historical suppliers', 'Tier 3 — New origins', 'Unreplaced'],
                      color: ['#0a2540', '#0e9f6a', '#2bbf8a', '#2a7de1', '#e23b2a']
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
                      color: ['rgba(14,159,106,0.3)', 'rgba(43,191,138,0.3)', 'rgba(42,125,225,0.3)', 'rgba(226,59,42,0.3)']
                    }
                  }]}
                  layout={{
                    width: 800,
                    height: 420,
                    margin: { l: 20, r: 20, t: 10, b: 10 },
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    font: { color: '#24364a', family: '"Source Sans 3", system-ui, sans-serif', size: 14 }
                  }}
                  config={{ responsive: true, displayModeBar: false }}
                />
              </div>
            </div>
          ) : (
            <div className="border border-line bg-wash p-8 rounded-sm text-center">
              <p className="text-muted">Sankey diagram cannot be rendered: one or more flow values are missing from the validated dataset.</p>
            </div>
          )}

          <section className="bg-wash p-8 rounded-sm border border-line">
            <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-4">What this means</h3>
            <p className="text-body text-lg font-light leading-relaxed font-serif mb-6">
              {data.replacement_rate >= 100 
                ? "The lost supply can be completely absorbed within the modeled historical limits of the existing network, without resulting in unreplaced shortfalls."
                : `The network cannot fully replace the lost supply. Despite tapping current, historical, and new suppliers, ${fmtLocale(data.unreplaced_supply)} tonnes remain unresolved.`}
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6 border-t border-[#d7e2ec]">
              <KPICard title="Unreplaced Supply" value={fmtLocale(data.unreplaced_supply)} subtitle="tonnes — modeled gap after all tiers" className="bg-paper shadow-sm" />
              <KPICard title="New-Origin Share" value={`${fmt(data.new_origin_share)}%`} subtitle="Share sourced from Tier 3 new origins" className="bg-paper shadow-sm" />
            </div>
          </section>
        </div>
      )}
    </div>
  );
};
