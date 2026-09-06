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
    <div className="space-y-16">
      <header className="border-b border-line pb-12">
        <h1 className="text-4xl md:text-5xl font-normal text-ink mb-8 font-serif">
          Which foods are most exposed to concentrated supplier relationships?
        </h1>
        
        <div className="flex flex-wrap gap-x-12 gap-y-6 max-w-4xl">
          <div className="flex-1 min-w-[200px] max-w-md">
            <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">Which food?</label>
            <select
              className="w-full bg-paper border-b border-line text-ink text-xl py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
              value={commodity}
              onChange={(e) => setCommodity(e.target.value)}
            >
              {commodities.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
        </div>
      </header>

      {loading && <div className="text-muted py-12 text-center animate-pulse">Aggregating commodity data...</div>}
      
      {error && (
        <div className="border border-[#e23b2a] bg-[#e23b2a]/5 p-8 rounded-sm text-center">
          <p className="text-[#e23b2a] font-light text-lg">Error: {error}</p>
        </div>
      )}

      {data && !loading && (
        <div className="space-y-12">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <KPICard
              title="Total Scenarios"
              value={fmtInt(data.total_scenarios)}
              subtitle="Country × Year combinations"
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

          <section className="border-t border-line pt-12">
            <h2 className="text-[10px] font-semibold text-muted mb-8 uppercase tracking-widest">Modeled Resilience Profile Distribution — {data.commodity}</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {data.profile_distribution.map((dist) => (
                <div key={dist.profile} className="flex flex-col items-start border-l border-line pl-5">
                  <ProfileBadge profile={dist.profile} showLabel className="mb-4 bg-transparent border-none p-0" />
                  <div className="text-3xl font-light text-ink mb-1">{fmt(dist.percentage)}%</div>
                  <div className="text-xs text-muted font-light">{fmtInt(dist.count)} scenarios</div>
                </div>
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  );
};
