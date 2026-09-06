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

  useEffect(() => {
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
  }, [country, commodity, year, rank]);

  return (
    <div className="space-y-8">
      <header className="border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-light text-slate-100 mb-2">Supplier Shock</h1>
        <p className="text-slate-400 font-light">
          Simulate the complete loss of supply from a major trading partner.
          Rank 1, 2, and 3 are independent single-supplier shocks — not cumulative.
        </p>
      </header>

      <div className="bg-amber-950/20 border border-amber-900/30 p-3 rounded text-amber-400/80 text-sm">
        Each rank represents an independent, isolated shock scenario. Selecting Rank 2 removes the Rank-2 supplier in isolation — it does NOT remove Rank 1 and Rank 2 simultaneously.
      </div>

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
        
        <div className="w-32">
          <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">Shock Rank</label>
          <select
            className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded p-2 outline-none"
            value={rank} onChange={(e) => setRank(Number(e.target.value))}
          >
            <option value={1}>Rank 1</option>
            <option value={2}>Rank 2</option>
            <option value={3}>Rank 3</option>
          </select>
        </div>
      </div>

      {loading && <div className="text-slate-400 py-12 text-center animate-pulse">Running shock scenario...</div>}
      
      {error && (
        <div className="bg-slate-900 border border-slate-800 p-8 rounded-lg text-center">
          <p className="text-slate-400 font-light text-lg">{error}</p>
        </div>
      )}

      {data && !loading && (
        <div className="space-y-8">
          <div className="bg-red-950/20 border border-red-900/30 p-6 rounded-lg text-center">
            <h2 className="text-xs font-medium text-red-400 uppercase tracking-widest mb-3">Simulated Supply Shock</h2>
            <div className="text-3xl font-light text-slate-100 mb-2">Total Loss of {data.shocked_supplier}</div>
            <p className="text-slate-400 text-sm">
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
              className="border-red-900/30 bg-red-950/10"
            />
            <KPICard
              title="Remaining Import Share"
              value={`${fmt(data.remaining_import_share)}%`}
              subtitle="From unaffected suppliers"
            />
          </div>
          
          <div className="bg-slate-900 border border-slate-800 p-8 rounded-lg">
            <h3 className="text-xs font-medium text-slate-500 uppercase tracking-widest mb-6">Import Share Composition Post-Shock</h3>
            <div className="w-full h-10 flex rounded overflow-hidden">
              <div
                style={{ width: `${data.remaining_import_share ?? 0}%` }}
                className="bg-blue-600/80 h-full flex items-center justify-center text-xs font-medium text-white"
              >
                {(data.remaining_import_share ?? 0) > 8 ? `${fmt(data.remaining_import_share)}% Remaining` : ''}
              </div>
              <div
                style={{ width: `${data.shock_loss_share ?? 0}%` }}
                className="bg-red-500/80 h-full flex items-center justify-center text-xs font-medium text-white"
              >
                {(data.shock_loss_share ?? 0) > 8 ? `${fmt(data.shock_loss_share)}% Lost` : ''}
              </div>
            </div>
            <div className="flex gap-6 mt-3 text-xs text-slate-500">
              <span className="flex items-center gap-2"><span className="w-3 h-3 bg-blue-600/80 rounded-sm inline-block"></span>Remaining supply from unaffected partners</span>
              <span className="flex items-center gap-2"><span className="w-3 h-3 bg-red-500/80 rounded-sm inline-block"></span>Lost supply (shocked supplier removed)</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
