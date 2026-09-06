import React, { useEffect, useState } from 'react';
import { fetchCountryOptions, fetchCountryAnalysis } from '../services/api';
import { CountryOptions, CountryAnalysisResponse } from '../types';
import { KPICard } from '../components/KPICard';
import { ProfileBadge } from '../components/ProfileBadge';

function fmt(val: number | null | undefined, decimals = 2): string {
  if (val == null) return '--';
  return val.toFixed(decimals);
}

function fmtLocale(val: number | null | undefined): string {
  if (val == null) return '--';
  return val.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

export const CountryExplorer = () => {
  const [options, setOptions] = useState<CountryOptions | null>(null);
  const [loadingOptions, setLoadingOptions] = useState(true);
  
  const [country, setCountry] = useState<string>('');
  const [commodity, setCommodity] = useState<string>('');
  const [year, setYear] = useState<number>(0);
  
  const [data, setData] = useState<CountryAnalysisResponse | null>(null);
  const [loadingData, setLoadingData] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCountryOptions().then(res => {
      setOptions(res);
      if (res.countries.length > 0) setCountry(res.countries[0]);
      if (res.commodities.length > 0) setCommodity(res.commodities[0]);
      if (res.years.length > 0) setYear(res.years[res.years.length - 1]);
      setLoadingOptions(false);
    });
  }, []);

  useEffect(() => {
    if (!country || !commodity || !year) return;
    
    setLoadingData(true);
    setError(null);
    fetchCountryAnalysis(country, commodity, year)
      .then(setData)
      .catch(err => {
        setData(null);
        if (err.response?.status === 404) {
           setError('No validated FOODSHIELD observation is available for this country × commodity × year.');
        } else {
           setError(err.message);
        }
      })
      .finally(() => setLoadingData(false));
  }, [country, commodity, year]);

  if (loadingOptions) return <div className="text-slate-400">Loading options...</div>;
  if (!options) return null;

  return (
    <div className="space-y-8">
      <header className="border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-light text-slate-100 mb-2">Country Explorer</h1>
        <p className="text-slate-400 font-light">Explore validated exposure and resilience profiles for a specific country × commodity × year scenario.</p>
      </header>

      <div className="flex flex-wrap gap-4 bg-slate-900 border border-slate-800 p-4 rounded-lg">
        <div className="flex-1 min-w-[200px]">
          <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">Country</label>
          <select
            className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded p-2 focus:ring-1 focus:ring-blue-500 outline-none"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
          >
            {options.countries.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        
        <div className="flex-1 min-w-[200px]">
          <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">Commodity</label>
          <select
            className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded p-2 focus:ring-1 focus:ring-blue-500 outline-none"
            value={commodity}
            onChange={(e) => setCommodity(e.target.value)}
          >
            {options.commodities.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div className="w-36">
          <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">Year</label>
          <select
            className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded p-2 focus:ring-1 focus:ring-blue-500 outline-none"
            value={year}
            onChange={(e) => setYear(Number(e.target.value))}
          >
            {options.years.map(y => <option key={y} value={y}>{y}</option>)}
          </select>
        </div>
      </div>

      {loadingData && <div className="text-slate-400 py-12 text-center animate-pulse">Querying validated dataset...</div>}
      
      {error && (
        <div className="bg-slate-900 border border-slate-800 p-8 rounded-lg text-center">
          <p className="text-slate-400 font-light text-lg">{error}</p>
        </div>
      )}

      {data && !loadingData && (
        <div className="space-y-8">
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <h2 className="text-xs font-medium text-slate-500 uppercase tracking-widest mb-3">Modeled Resilience Profile</h2>
              <ProfileBadge profile={data.resilience_profile} showLabel className="text-base px-4 py-2" />
            </div>
            <div className="text-right">
              <div className="text-xs font-medium text-slate-500 uppercase tracking-widest mb-1">Modeled Replacement Rate</div>
              <div className="text-4xl font-light text-slate-100">{fmt(data.replacement_rate)}%</div>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-medium text-slate-500 uppercase tracking-widest mb-4">Exposure Metrics</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <KPICard title="Baseline Imports" value={fmtLocale(data.baseline_imports)} subtitle="tonnes" />
              <KPICard title="Supplier Count" value={String(data.supplier_count)} subtitle="Active trading partners" />
              <KPICard title="HHI" value={fmt(data.HHI, 4)} subtitle="Market concentration index" />
              <KPICard title="Largest Supplier Share" value={`${fmt(data.largest_supplier_share, 1)}%`} />
              <KPICard title="Top 3 Suppliers Share" value={`${fmt(data.top3_supplier_share, 1)}%`} />
              <KPICard title="Import Dependence" value={data.import_dependence != null ? `${fmt(data.import_dependence, 1)}%` : 'Not available'} />
            </div>
          </div>

          <div>
            <h3 className="text-xs font-medium text-slate-500 uppercase tracking-widest mb-4">Shock Metrics (Rank-1 Supplier Removed)</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <KPICard title="Lost Supply" value={fmtLocale(data.lost_supply)} subtitle="tonnes" />
              <KPICard title="Shock Loss Share" value={`${fmt(data.shock_loss_share, 1)}%`} subtitle="Share of baseline imports lost" />
              <KPICard title="Remaining Import Share" value={`${fmt(data.remaining_import_share, 1)}%`} />
            </div>
          </div>

          <div>
            <h3 className="text-xs font-medium text-slate-500 uppercase tracking-widest mb-4">Modeled Replacement Pathway</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <KPICard title="Tier 1 Replacement" value={fmtLocale(data.tier1_replacement)} subtitle="Current-year suppliers" />
              <KPICard title="Tier 2 Replacement" value={fmtLocale(data.tier2_replacement)} subtitle="Historical suppliers" />
              <KPICard title="Tier 3 Replacement" value={fmtLocale(data.tier3_replacement)} subtitle="New-origin suppliers" />
              <KPICard title="Unreplaced Supply" value={fmtLocale(data.unreplaced_supply)} subtitle="tonnes — modeled gap" />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
