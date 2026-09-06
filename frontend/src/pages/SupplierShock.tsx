import React, { useEffect, useState } from 'react';
import { fetchCountryOptions, fetchShockAnalysis } from '../services/api';
import { CountryOptions, ShockAnalysisResponse } from '../types';
import { KPICard } from '../components/KPICard';

function fmt(val: number | null | undefined, decimals = 1): string {
  if (val == null) return '--';
  return val.toFixed(decimals);
}

function fmtLocale(val: number | null | undefined): string {
  if (val == null) return '--';
  return val.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

export const SupplierShock = () => {
  const [options, setOptions] = useState<CountryOptions | null>(null);
  
  const [country, setCountry] = useState<string>('');
  const [commodity, setCommodity] = useState<string>('');
  const [year, setYear] = useState<number>(0);
  const [rank, setRank] = useState<number>(1);
  
  const [data, setData] = useState<ShockAnalysisResponse | null>(null);
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

  const handleRunShock = () => {
    if (!country || !commodity || !year || !rank) return;
    
    setLoading(true);
    setError(null);
    fetchShockAnalysis(country, commodity, year, rank)
      .then(setData)
      .catch(err => {
        setData(null);
        if (err.response?.status === 404) {
           setError(`No validated FOODSHIELD observation for Rank ${rank} shock.`);
        } else {
           setError(err.message);
        }
      })
      .finally(() => setLoading(false));
  };

  return (
    <div className="space-y-16">
      <header className="border-b border-line pb-12">
        <p className="text-xs font-semibold text-[#e23b2a] uppercase tracking-[0.2em] mb-4">04 &mdash; The Shock</p>
        <div className="mb-8 p-6 bg-[#e23b2a]/5 border-l-4 border-[#e23b2a]">
          <div className="text-xs font-semibold text-[#e23b2a] uppercase tracking-[0.2em] mb-2">RQ 2 &mdash; Shock Severity</div>
          <h2 className="text-2xl font-serif text-ink mb-0">How large is the modeled loss when the largest supplier disappears?</h2>
        </div>
        <h1 className="text-4xl md:text-5xl font-normal text-ink mb-6 font-serif">
          What happens if the dominant supplier disappears?
        </h1>
        <p className="text-body text-xl font-light mb-8 max-w-3xl">
          Simulate the complete loss of supply from a major trading partner to measure the immediate impact on the import network.
        </p>

        <div className="flex flex-wrap items-end gap-x-12 gap-y-6 max-w-5xl">
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
          
          <div className="w-48">
            <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">DISRUPTION LEVEL</label>
            <select
              className="w-full bg-paper border-b border-line text-ink text-xl py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
              value={rank} onChange={(e) => setRank(Number(e.target.value))}
            >
              <option value={1}>Rank 1 Supplier</option>
              <option value={2}>Rank 2 Supplier</option>
              <option value={3}>Rank 3 Supplier</option>
            </select>
          </div>
          
          <button 
            onClick={handleRunShock}
            className="bg-[#1565c0] text-white px-8 py-3 text-sm font-semibold uppercase tracking-widest hover:bg-[#0d47a1] transition-colors"
          >
            Run Shock Scenario
          </button>
        </div>
      </header>

      {loading && <div className="text-muted py-12 text-center animate-pulse">Running shock scenario...</div>}
      
      {error && (
        <div className="border border-[#e23b2a] bg-[#e23b2a]/5 p-8 rounded-sm text-center">
          <p className="text-[#e23b2a] font-light text-lg">{error}</p>
        </div>
      )}

      {data && !loading && (
        <div className="space-y-12">
          <div className="border-l-4 border-[#e23b2a] pl-8 py-2">
            <h2 className="text-[10px] font-semibold text-muted uppercase tracking-widest mb-3">Simulated Supply Shock</h2>
            <div className="text-4xl md:text-5xl font-normal text-ink mb-2 font-serif">Total Loss of {data.shocked_supplier}</div>
            <p className="text-body text-lg font-light">
              Rank {data.supplier_rank} supplier for {data.commodity} to {data.importer} in {data.year}
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <KPICard
              title="Lost Supply Volume"
              value={fmtLocale(data.lost_supply_tonnes)}
              subtitle="tonnes"
            />
            <KPICard
              title="Shock Loss Share"
              value={`${fmt(data.shock_loss_share)}%`}
              subtitle="% of total baseline imports removed"
              className="border-[#e23b2a] bg-[#e23b2a]/5"
            />
            <KPICard
              title="Remaining Import Share"
              value={`${fmt(data.remaining_import_share)}%`}
              subtitle="From unaffected suppliers"
            />
          </div>
          
          <div className="bg-wash border border-line p-8 md:p-12 rounded-sm">
            <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-8">Import Share Composition Post-Shock</h3>
            <div className="w-full h-16 flex overflow-hidden border border-line">
              <div
                style={{ width: `${data.remaining_import_share ?? 0}%` }}
                className="bg-[#1565c0] h-full flex items-center justify-center text-sm font-semibold text-white tracking-wide"
              >
                {(data.remaining_import_share ?? 0) > 8 ? `${fmt(data.remaining_import_share)}% Remaining` : ''}
              </div>
              <div
                style={{ width: `${data.shock_loss_share ?? 0}%` }}
                className="bg-[#e23b2a] h-full flex items-center justify-center text-sm font-semibold text-white tracking-wide"
              >
                {(data.shock_loss_share ?? 0) > 8 ? `${fmt(data.shock_loss_share)}% Lost` : ''}
              </div>
            </div>
            <div className="flex gap-8 mt-6 text-sm text-body font-light">
              <span className="flex items-center gap-3"><span className="w-4 h-4 bg-[#1565c0] inline-block"></span>Remaining supply from unaffected partners</span>
              <span className="flex items-center gap-3"><span className="w-4 h-4 bg-[#e23b2a] inline-block"></span>Lost supply (shocked supplier removed)</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
