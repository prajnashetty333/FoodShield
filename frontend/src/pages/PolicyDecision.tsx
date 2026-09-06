import React, { useEffect, useState } from 'react';
import { fetchPolicy, fetchCountryOptions, fetchCountryAnalysis } from '../services/api';
import { PolicyResponse, CountryOptions, CountryAnalysisResponse } from '../types';
import { ProfileBadge } from '../components/ProfileBadge';

export const PolicyDecision = () => {
  const [data, setData] = useState<PolicyResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [options, setOptions] = useState<CountryOptions | null>(null);
  const [country, setCountry] = useState<string>('');
  const [commodity, setCommodity] = useState<string>('');
  const [year, setYear] = useState<number>(0);
  
  const [analysisData, setAnalysisData] = useState<CountryAnalysisResponse | null>(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);

  useEffect(() => {
    fetchPolicy()
      .then(setData)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
      
    fetchCountryOptions().then(res => {
      setOptions(res);
      if (res.countries.length > 0) setCountry(res.countries[0]);
      if (res.commodities.length > 0) setCommodity(res.commodities[0]);
      if (res.years.length > 0) setYear(res.years[res.years.length - 1]);
    });
  }, []);

  useEffect(() => {
    if (!country || !commodity || !year) return;
    setAnalysisLoading(true);
    fetchCountryAnalysis(country, commodity, year)
      .then(setAnalysisData)
      .catch(() => setAnalysisData(null))
      .finally(() => setAnalysisLoading(false));
  }, [country, commodity, year]);

  if (loading || !options) return <div className="text-muted animate-pulse">Loading policy framework...</div>;
  if (error) return <div className="border border-[#e23b2a] bg-[#e23b2a]/5 p-8 rounded-sm"><p className="text-[#e23b2a] font-light text-lg">Error: {error}</p></div>;
  if (!data) return <div className="text-muted">No data available</div>;

  return (
    <div className="space-y-16 max-w-5xl">
      <header className="border-b border-line pb-12">
        <p className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-4">07 &mdash; The Decision</p>
        
        <div className="mb-8 p-6 bg-[#1565c0]/5 border-l-4 border-[#1565c0]">
          <div className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-2">RQ 6 &mdash; Persistent Constraints</div>
          <h2 className="text-2xl font-serif text-ink mb-0">Which country&ndash;commodity systems repeatedly experience difficult replacement pathways?</h2>
        </div>

        <h1 className="text-4xl md:text-5xl font-normal text-ink mb-6 font-serif">
          Policy & Decision Framework
        </h1>
        <p className="text-body text-xl font-light mb-8 max-w-3xl">
          Decision-support implications of the modeled trade-replacement framework. Select a country and commodity to see its targeted policy pathway based on its resilience profile.
        </p>

        <div className="flex flex-wrap items-end gap-x-12 gap-y-6 max-w-4xl mb-8">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">WHO ARE WE TESTING?</label>
            <select
              className="w-full bg-paper border-b border-line text-ink text-xl py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
              value={country} onChange={(e) => setCountry(e.target.value)}
            >
              {options.countries.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">WHAT FOOD?</label>
            <select
              className="w-full bg-paper border-b border-line text-ink text-xl py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
              value={commodity} onChange={(e) => setCommodity(e.target.value)}
            >
              {options.commodities.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          <div className="w-28">
            <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">YEAR</label>
            <select
              className="w-full bg-paper border-b border-line text-ink text-xl py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
              value={year} onChange={(e) => setYear(Number(e.target.value))}
            >
              {options.years.map(y => <option key={y} value={y}>{y}</option>)}
            </select>
          </div>
        </div>

        <div className="bg-wash border-l-4 border-l-[#e6a817] p-6 text-body text-sm leading-relaxed">
          <strong className="text-ink font-semibold">Disclaimer:</strong> {data.disclaimer}
        </div>
      </header>

      {analysisLoading ? (
        <div className="text-muted animate-pulse py-8 text-center">Analyzing selected system...</div>
      ) : analysisData ? (
        <div className="mb-16 border border-[#1565c0] bg-white p-8">
          <h3 className="text-[10px] font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-4">Contextual Policy Recommendation</h3>
          <p className="text-lg text-body font-light mb-6">
            For <strong>{analysisData.importer}</strong> importing <strong>{analysisData.commodity}</strong> (in {analysisData.year}), 
            the modeled resilience profile is <strong>Type {analysisData.resilience_profile}</strong>.
          </p>
          
          {data.framework.filter(rec => rec.profile === analysisData.resilience_profile).map(rec => (
            <div key={rec.profile} className="flex flex-col md:flex-row gap-8">
              <div className="md:w-1/3 shrink-0">
                <ProfileBadge profile={rec.profile} showLabel className="text-sm px-4 py-2 border border-[#1565c0] bg-wash shadow-sm w-full" />
              </div>
              <div className="md:w-2/3">
                <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-6 border-b border-line pb-2">Targeted Strategic Directions</h3>
                <ul className="space-y-6">
                  {rec.directions.map((dir, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-[#1565c0] mr-4 mt-1 font-serif text-lg">—</span>
                      <span className="text-body text-lg font-light leading-relaxed font-serif">{dir}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="mb-16 py-8 border border-line bg-wash text-center text-muted">
          No validated FOODSHIELD observation for this specific country &times; commodity &times; year combination. Please select another system.
        </div>
      )}

      <div className="pt-8 border-t border-line">
        <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-12">All Profile Frameworks</h3>
        <div className="grid grid-cols-1 gap-12">
          {data.framework.map(rec => (
            <div key={rec.profile} className={`flex flex-col md:flex-row gap-8 pb-12 border-b border-line last:border-0 ${analysisData?.resilience_profile === rec.profile ? 'opacity-50 grayscale' : ''}`}>
              <div className="md:w-1/3 shrink-0">
                <ProfileBadge profile={rec.profile} showLabel className="text-sm px-4 py-2 border border-line bg-wash shadow-sm w-full" />
              </div>
              
              <div className="md:w-2/3">
                <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-6 border-b border-line pb-2">Strategic Directions</h3>
                <ul className="space-y-6">
                  {rec.directions.map((dir, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-muted mr-4 mt-1 font-serif text-lg">—</span>
                      <span className="text-body text-lg font-light leading-relaxed font-serif">{dir}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
