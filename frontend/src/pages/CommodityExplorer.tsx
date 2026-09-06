import React, { useEffect, useState } from 'react';
import { fetchCommodities, fetchCommodityAnalysis } from '../services/api';
import { CommodityAnalysisResponse } from '../types';
import { KPICard } from '../components/KPICard';
import { ProfileBadge } from '../components/ProfileBadge';

function fmt(val: number | null | undefined, decimals = 1): string {
  if (val == null) return '--';
  return val.toFixed(decimals);
}

function fmtInt(val: number | null | undefined): string {
  if (val == null) return '--';
  return val.toLocaleString();
}

export const CommodityExplorer = () => {
  const [commodities, setCommodities] = useState<string[]>([]);
  const [commodity, setCommodity] = useState<string>('');
  
  const [data, setData] = useState<CommodityAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCommodities().then(res => {
      setCommodities(res);
      if (res.length > 0) setCommodity(res[0]);
    });
  }, []);

  useEffect(() => {
    if (!commodity) return;
    
    setLoading(true);
    setError(null);
    fetchCommodityAnalysis(commodity)
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [commodity]);

  return (
    <div className="space-y-8">
      <header className="border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-light text-slate-100 mb-2">Commodity Explorer</h1>
        <p className="text-slate-400 font-light">
          Explore aggregate modeled resilience metrics across all validated scenarios for one of the six locked commodities.
        </p>
      </header>

      <div className="flex flex-wrap gap-4 bg-slate-900 border border-slate-800 p-4 rounded-lg">
        <div className="flex-1 min-w-[200px] max-w-md">
          <label className="block text-xs font-medium text-slate-400 mb-1 uppercase tracking-wider">Commodity</label>
          <select
            className="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded p-2 focus:ring-1 focus:ring-blue-500 outline-none"
            value={commodity}
            onChange={(e) => setCommodity(e.target.value)}
          >
            {commodities.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
      </div>

      {loading && <div className="text-slate-400 py-12 text-center animate-pulse">Aggregating commodity data...</div>}
      
      {error && (
        <div className="bg-slate-900 border border-slate-800 p-8 rounded-lg text-center">
          <p className="text-slate-400 font-light text-lg">Error: {error}</p>
        </div>
      )}

      {data && !loading && (
        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <KPICard
              title="Total Scenarios"
              value={fmtInt(data.total_scenarios)}
              subtitle="Country x Year combinations"
            />
            <KPICard
              title="Mean Modeled Replacement"
              value={`${fmt(data.mean_replacement_rate)}%`}
            />
            <KPICard
              title="Mean Shock Loss Share"
              value={`${fmt(data.mean_shock_loss_share)}%`}
              subtitle="Average % of imports lost in Rank-1 shock"
            />
            <KPICard
              title="Mean Supplier HHI"
              value={fmt(data.mean_hhi, 3)}
              subtitle="Average market concentration index"
            />
          </div>

          <section>
            <h2 className="text-xs font-medium text-slate-500 mb-6 uppercase tracking-widest">Modeled Resilience Profile Distribution — {data.commodity}</h2>
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
        </div>
      )}
    </div>
  );
};
