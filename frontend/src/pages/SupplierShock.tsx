import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchCountryOptions, fetchShockAnalysis } from '../services/api';
import { CountryOptions, ShockAnalysisResponse } from '../types';
import { KPICard } from '../components/KPICard';

function fmt(value: number | null | undefined, decimals = 1) { return value == null ? '--' : value.toFixed(decimals); }
function fmtLocale(value: number | null | undefined) { return value == null ? '--' : value.toLocaleString(undefined, { maximumFractionDigits: 0 }); }

export const SupplierShock = () => {
  const [options, setOptions] = useState<CountryOptions | null>(null);
  const [country, setCountry] = useState('');
  const [commodity, setCommodity] = useState('');
  const [year, setYear] = useState(0);
  const [rank, setRank] = useState(1);
  const [data, setData] = useState<ShockAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCountryOptions().then(res => {
      setOptions(res);
      setCountry(res.countries.includes('Japan') ? 'Japan' : res.countries[0] ?? '');
      setCommodity(res.commodities.includes('Maize') ? 'Maize' : res.commodities[0] ?? '');
      setYear(res.years.includes(2011) ? 2011 : res.years[res.years.length - 1] ?? 0);
    });
  }, []);

  const runShock = () => {
    if (!country || !commodity || !year) return;
    setLoading(true); setError(null);
    fetchShockAnalysis(country, commodity, year, rank)
      .then(setData)
      .catch(err => { setData(null); setError(err.response?.status === 404 ? `No validated FOODSHIELD observation for Rank ${rank} shock.` : err.message); })
      .finally(() => setLoading(false));
  };

  return <div className="space-y-28 md:space-y-40 max-w-6xl mx-auto">
    <header className="pt-2 pb-16 border-b border-line">
      <p className="text-xs font-semibold text-[#e23b2a] uppercase tracking-[.2em] mb-6">04 — The Shock</p>
      <h1 className="font-serif text-5xl md:text-7xl leading-[.95] text-ink uppercase">Remove the dominant supplier.</h1>
      <p className="mt-8 max-w-3xl text-xl md:text-2xl font-light leading-relaxed text-body">How much imported supply is immediately exposed when the largest foreign supplier disappears?</p>
      <p className="mt-8 max-w-3xl text-base font-light leading-relaxed text-muted">FOODSHIELD runs a defined thought experiment: it removes one selected supplier from an importer’s observed trade in a given year. The result is modeled exposure — not a forecast that the supplier will disappear.</p>
    </header>

    <section className="grid grid-cols-1 lg:grid-cols-[.8fr_1.2fr] gap-12 lg:gap-20 items-center">
      <div><p className="text-xs font-semibold uppercase tracking-[.2em] text-[#e23b2a] mb-5">The scale of the interruption</p><div className="font-serif text-7xl md:text-8xl text-[#e23b2a]">67.17%</div><h2 className="mt-4 font-serif text-3xl md:text-4xl text-ink">of baseline imports are lost, on average, when the largest supplier is removed.</h2></div>
      <p className="border-l-2 border-[#e23b2a] pl-6 text-lg font-light leading-relaxed text-body">This is the average modeled shock loss across the validated Rank‑1 scenarios. It is the removed supplier’s share of baseline imports — not a share of all food consumed. When that share is large, more supply has to be found elsewhere.</p>
    </section>

    <section>
      <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-4 mb-10"><div><p className="text-xs font-semibold uppercase tracking-[.2em] text-[#e23b2a] mb-4">The interruption</p><h2 className="font-serif text-3xl md:text-4xl text-ink">Before → shock</h2></div><p className="max-w-md text-sm font-light leading-relaxed text-muted">A conceptual view of the same import system before and after its largest link is removed.</p></div>
      <div className="grid grid-cols-1 md:grid-cols-[1fr_auto_1fr] border border-line bg-wash overflow-hidden">
        <div className="p-8 md:p-10"><p className="text-[10px] font-semibold uppercase tracking-[.18em] text-muted mb-8">Baseline import network</p><div className="space-y-5"><div className="h-10 bg-[#1565c0] flex items-center px-4 text-xs font-semibold uppercase tracking-wider text-white">Largest supplier</div><div className="h-6 bg-[#9bbce0] w-2/3"/><div className="h-6 bg-[#c9d9e8] w-1/2"/><div className="h-6 bg-[#dce7f0] w-1/3"/></div><p className="mt-8 text-sm font-light text-body">Several suppliers can be present, while one supplier may account for a substantial observed share.</p></div>
        <div className="flex md:flex-col items-center justify-center gap-3 px-7 py-6 bg-paper border-y md:border-y-0 md:border-x border-line"><span className="text-3xl text-[#e23b2a]">→</span><span className="text-[10px] font-semibold uppercase tracking-[.18em] text-[#e23b2a]">Shock</span></div>
        <div className="p-8 md:p-10"><p className="text-[10px] font-semibold uppercase tracking-[.18em] text-muted mb-8">After shock</p><div className="space-y-5"><div className="h-10 border-2 border-dashed border-[#e23b2a] bg-[#e23b2a]/5 flex items-center px-4 text-xs font-semibold uppercase tracking-wider text-[#e23b2a]">Largest supplier removed</div><div className="h-6 bg-[#9bbce0] w-2/3"/><div className="h-6 bg-[#c9d9e8] w-1/2"/><div className="h-6 bg-[#dce7f0] w-1/3"/></div><p className="mt-8 text-sm font-light text-body">The missing block is the immediate supply requirement that the next chapter examines.</p></div>
      </div>
    </section>

    <section className="bg-ink text-white p-8 md:p-14"><div className="grid grid-cols-1 md:grid-cols-[.8fr_1.2fr] gap-10"><h2 className="font-serif text-3xl md:text-4xl leading-tight">A dominant supplier can turn one broken link into a large replacement task.</h2><p className="text-lg font-light leading-relaxed text-gray-300">The shock does not say other suppliers cannot help. It first establishes the amount that has been removed. FOODSHIELD then tests the modeled replacement pathways separately, using observed trade relationships and historical export-expansion capacity.</p></div></section>

    <section className="border-t border-line pt-14">
      <p className="text-xs font-semibold uppercase tracking-[.2em] text-[#e23b2a] mb-5">Case study</p>
      <div className="flex flex-col lg:flex-row lg:justify-between lg:items-end gap-6 mb-10"><div><h2 className="font-serif text-4xl md:text-5xl text-ink">Test a specific supplier shock.</h2><p className="mt-4 max-w-2xl text-lg font-light leading-relaxed text-body">Choose an observed country, food, year, and supplier rank. Every result below is returned by the existing FOODSHIELD API.</p></div>{data && <p className="text-sm text-muted">Showing <strong className="text-ink">{data.importer} · {data.commodity} · {data.year} · Rank {data.supplier_rank}</strong></p>}</div>
      <div className="border border-line bg-paper p-6 md:p-10"><div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-7"><label className="block text-xs font-semibold text-muted uppercase tracking-widest">Country<select className="mt-3 w-full bg-transparent border-b border-line text-ink text-xl py-2 outline-none" value={country} onChange={e => setCountry(e.target.value)}>{options?.countries.map(item => <option key={item} value={item}>{item}</option>)}</select></label><label className="block text-xs font-semibold text-muted uppercase tracking-widest">Food<select className="mt-3 w-full bg-transparent border-b border-line text-ink text-xl py-2 outline-none" value={commodity} onChange={e => setCommodity(e.target.value)}>{options?.commodities.map(item => <option key={item} value={item}>{item}</option>)}</select></label><label className="block text-xs font-semibold text-muted uppercase tracking-widest">Year<select className="mt-3 w-full bg-transparent border-b border-line text-ink text-xl py-2 outline-none" value={year} onChange={e => setYear(Number(e.target.value))}>{options?.years.map(item => <option key={item} value={item}>{item}</option>)}</select></label><label className="block text-xs font-semibold text-muted uppercase tracking-widest">Supplier shock<select className="mt-3 w-full bg-transparent border-b border-line text-ink text-xl py-2 outline-none" value={rank} onChange={e => setRank(Number(e.target.value))}><option value={1}>Rank 1 supplier</option><option value={2}>Rank 2 supplier</option><option value={3}>Rank 3 supplier</option></select></label></div><button onClick={runShock} className="mt-10 bg-[#1565c0] text-white px-8 py-3 text-sm font-semibold uppercase tracking-widest hover:bg-[#0d47a1] transition-colors">Run the case study</button></div>
      {loading && <div className="py-12 text-center text-muted animate-pulse">Running the modeled shock…</div>}
      {error && <div className="mt-8 border border-[#e23b2a] bg-[#e23b2a]/5 p-7 text-center text-[#e23b2a]">{error}</div>}
      {data && !loading && <div className="mt-10 space-y-10"><div className="border-l-4 border-[#e23b2a] pl-6"><p className="text-[10px] font-semibold uppercase tracking-[.18em] text-muted">Selected scenario</p><h3 className="mt-3 font-serif text-3xl text-ink">{data.shocked_supplier} disappears from {data.importer}’s {data.commodity} imports.</h3><p className="mt-3 text-body font-light">{data.year} · Rank {data.supplier_rank} supplier shock</p></div><div className="grid grid-cols-1 md:grid-cols-3 gap-6"><KPICard title="Lost supply" value={fmtLocale(data.lost_supply_tonnes)} subtitle="tonnes removed" className="border-[#e23b2a] bg-[#e23b2a]/5"/><KPICard title="Supplier share lost" value={`${fmt(data.shock_loss_share)}%`} subtitle="of baseline imports"/><KPICard title="Supply still connected" value={`${fmt(data.remaining_import_share)}%`} subtitle="from unaffected suppliers"/></div></div>}
    </section>

    <section className="py-24 text-center bg-wash border-t border-line"><p className="text-xs font-semibold uppercase tracking-[.2em] text-[#1565c0] mb-6">Next: the replacement</p><h2 className="font-serif text-5xl md:text-6xl text-ink">Can the network fill it?</h2><p className="mt-7 max-w-2xl mx-auto text-body font-light leading-relaxed">The next chapter tests how much of the modeled lost supply can be replaced through current suppliers, historical suppliers, and eligible new origins.</p><Link to="/replacement" className="inline-flex mt-12 px-12 py-5 bg-ink text-white text-sm font-semibold uppercase tracking-widest hover:bg-[#1a365d] transition-colors">05 — The Replacement →</Link></section>
  </div>;
};
