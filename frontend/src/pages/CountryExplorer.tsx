import React, { useEffect, useState, useRef } from 'react';
import Plot from 'react-plotly.js';
import { Link } from 'react-router-dom';
import { fetchCountryOptions, fetchCountryAnalysis, fetchCommodityAnalysis } from '../services/api';
import { CountryOptions, CountryAnalysisResponse, CommodityAnalysisResponse } from '../types';
import { KPICard } from '../components/KPICard';
import { ProfileBadge } from '../components/ProfileBadge';
import { fetchShockAnalysis } from '../services/api';

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
  const [shockData, setShockData] = useState<any | null>(null);
  const [loadingData, setLoadingData] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [commodityCompareData, setCommodityCompareData] = useState<CommodityAnalysisResponse[]>([]);
  const profileRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchCountryOptions().then(res => {
      setOptions(res);
      // Wait for user click to set country instead of defaulting, but if we need to load options...
      // We'll leave country empty initially.
      if (res.commodities.length > 0) setCommodity(res.commodities[0]);
      if (res.years.length > 0) setYear(res.years[res.years.length - 1]);
      setLoadingOptions(false);
    });

    const lockedCommodities = ['Wheat', 'Rice', 'Maize', 'Palm Oil', 'Sugar', 'Sunflower Oil'];
    Promise.all(lockedCommodities.map(c => fetchCommodityAnalysis(c)))
      .then(setCommodityCompareData)
      .catch(console.error);
  }, []);

  useEffect(() => {
    if (!country || !commodity || !year) return;
    
    setLoadingData(true);
    setError(null);
    fetchCountryAnalysis(country, commodity, year)
      .then(res => {
        setData(res);
        // Ensure scroll to profile is complete
        setTimeout(() => profileRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
      })
      .catch(err => {
        setData(null);
        if (err.response?.status === 404) {
           setError('No validated FOODSHIELD observation is available for this country × commodity × year.');
        } else {
           setError(err.message);
        }
      });
      
    fetchShockAnalysis(country, commodity, year, 1)
      .then(res => setShockData(res))
      .catch(() => setShockData(null))
      .finally(() => setLoadingData(false));
  }, [country, commodity, year]);

  if (loadingOptions) return <div className="text-muted animate-pulse">Initializing Research Environment...</div>;
  if (!options) return null;

  return (
    <div className="space-y-32 max-w-5xl mx-auto">
      {/* HEADER */}
      <section className="border-b border-line pb-16">
        <p className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-4">02 &mdash; The Exposure</p>
        <h1 className="text-5xl md:text-6xl font-normal text-ink font-serif mb-8 leading-tight">
          How vulnerable is the trade network before a shock?
        </h1>
        <p className="text-xl text-body font-light leading-relaxed max-w-3xl">
          FOODSHIELD first examines the structure of food-import dependence before introducing a supplier shock. 
          A country's exposure to food-trade disruption depends not only on how much it imports, but also on how 
          concentrated those imports are across foreign suppliers. High imports do not automatically mean high concentration.
        </p>
      </section>

      {/* GLOBAL SCALE */}
      <section className="bg-wash p-12 border border-line">
        <h2 className="text-[10px] font-semibold text-muted mb-12 uppercase tracking-[0.2em]">Validated Network Scale</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-y-16 gap-x-12">
          <div>
            <div className="text-4xl font-light text-ink mb-2 font-serif">178</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Importing Countries</div>
          </div>
          <div>
            <div className="text-4xl font-light text-ink mb-2 font-serif">197</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Supplying Countries</div>
          </div>
          <div>
            <div className="text-4xl font-light text-ink mb-2 font-serif">128,486</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Positive-flow relationships</div>
          </div>
          <div>
            <div className="text-4xl font-light text-ink mb-2 font-serif">6</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Locked Commodities</div>
          </div>
          <div>
            <div className="text-4xl font-light text-ink mb-2 font-serif">14 Years</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Trade-analysis period</div>
          </div>
        </div>
        <div className="mt-12 text-xs text-muted font-medium border-t border-line pt-6">
          Trade-network construction uses 2010–2023; primary capacity-constrained resilience analysis uses 2011–2023 because 2010 lacks pre-shock history.
        </div>
      </section>

      {/* SUPPLIER CONCENTRATION */}
      <section>
        <div className="mb-8 p-6 bg-[#1565c0]/5 border-l-4 border-[#1565c0]">
          <div className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-2">RQ 1 &mdash; Supplier Concentration</div>
          <h2 className="text-2xl font-serif text-ink mb-0">How concentrated are food imports among suppliers before the shock?</h2>
        </div>
        <p className="text-lg text-body font-light leading-relaxed mb-12">
          One number changes the way we think about disruption: the share controlled by the largest supplier. 
          Largest supplier share measures how much of an importer's baseline imports come from its dominant foreign supplier.
        </p>
        <div className="mb-6">
          <img src="/images/fig01_supplier_concentration.png" alt="Supplier Concentration" className="w-full border border-line" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-sm pt-4 border-t border-line">
          <div>
            <span className="block font-semibold text-ink uppercase tracking-wider text-xs mb-1">Why it matters</span>
            <span className="text-body">The largest supplier can account for a substantial share of baseline imports.</span>
          </div>
          <div>
            <span className="block font-semibold text-ink uppercase tracking-wider text-xs mb-1">Source / Scope</span>
            <span className="text-body font-mono text-xs">foodshield_resilience_metrics_2010_2023.csv<br/>Rank 1 | 2011–2023 | Capacity-valid</span>
          </div>
        </div>
      </section>

      {/* TRANSITION */}
      <section className="py-16 text-center border-y border-line bg-wash">
        <p className="text-2xl font-serif text-ink mb-12">Now imagine that supplier disappears.</p>
        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="w-full max-w-md h-8 bg-ink rounded-sm"></div>
          <div className="text-xs font-semibold uppercase tracking-widest text-muted">Largest Supplier</div>
          
          <div className="text-2xl text-muted py-2">&darr;</div>
          
          <div className="w-full max-w-md h-8 border-2 border-dashed border-[#e23b2a] bg-[#e23b2a]/10 rounded-sm"></div>
          <div className="text-xs font-semibold uppercase tracking-widest text-[#e23b2a]">Supplier Removed</div>
          
          <div className="text-2xl text-muted py-2">&darr;</div>
          
          <div className="w-full max-w-md h-4 bg-line rounded-sm"></div>
          <div className="text-xs font-semibold uppercase tracking-widest text-muted">Remaining Network</div>
        </div>
        <p className="mt-12 text-body font-light text-lg">
          A highly concentrated import system can expose a larger share of baseline imports to a single-supplier shock.
        </p>
      </section>

      {/* INTERACTIVE WORLD MAP */}
      <section>
        <h2 className="text-2xl font-serif text-ink mb-4 uppercase">Where is exposure concentrated?</h2>
        <p className="text-lg text-body font-light leading-relaxed mb-8">
          Select a country on the map to analyze its structural trade exposure and modeled resilience profile.
        </p>
        <div className="bg-wash border border-line relative overflow-hidden">
          <Plot
            data={[
              {
                type: 'choropleth',
                locationmode: 'country names',
                locations: options.countries,
                z: options.countries.map(() => 1),
                text: options.countries,
                colorscale: [
                  [0, '#e5e7eb'],
                  [1, '#1565c0']
                ],
                showscale: false,
                marker: {
                  line: { color: '#ffffff', width: 0.5 }
                },
                hoverinfo: 'text',
                hovertemplate: '%{text}<br>Data available<extra></extra>'
              }
            ]}
            layout={{
              geo: {
                showframe: false,
                showcoastlines: true,
                projection: { type: 'equirectangular' },
                bgcolor: 'transparent'
              },
              margin: { l: 0, r: 0, t: 0, b: 0 },
              paper_bgcolor: 'transparent',
              plot_bgcolor: 'transparent',
              dragmode: false,
              autosize: true
            }}
            useResizeHandler={true}
            style={{ width: '100%', height: '500px' }}
            onClick={(mapData) => {
              if (mapData.points && mapData.points.length > 0) {
                const selectedCountry = mapData.points[0].location;
                if (selectedCountry) {
                  setCountry(selectedCountry);
                }
              }
            }}
          />
        </div>
        <div className="mt-4 text-xs font-medium text-muted uppercase tracking-widest flex items-center gap-2">
          <div className="w-3 h-3 bg-[#1565c0]"></div> Countries with available analytical observations
        </div>
      </section>

      {/* COUNTRY EXPLORER (Detailed Profile) */}
      <div ref={profileRef} className="scroll-mt-16">
        {country && (
          <section className="border border-[#1565c0] p-8 md:p-12 bg-white relative">
            <h3 className="text-[10px] font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-8">Country Profile</h3>
            
            <div className="flex flex-wrap gap-x-12 gap-y-6 max-w-4xl mb-12 pb-8 border-b border-line">
              <div className="flex-1 min-w-[200px]">
                <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">Country</label>
                <select
                  className="w-full bg-transparent border-b border-line text-ink text-2xl font-serif py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
                  value={country}
                  onChange={(e) => setCountry(e.target.value)}
                >
                  <option value="" disabled>Select Country</option>
                  {options.countries.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              
              <div className="flex-1 min-w-[200px]">
                <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">Food / Commodity</label>
                <select
                  className="w-full bg-transparent border-b border-line text-ink text-2xl font-serif py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
                  value={commodity}
                  onChange={(e) => setCommodity(e.target.value)}
                >
                  {options.commodities.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>

              <div className="w-32">
                <label className="block text-xs font-semibold text-muted mb-2 uppercase tracking-widest">Year</label>
                <select
                  className="w-full bg-transparent border-b border-line text-ink text-2xl font-serif py-2 focus:border-[#1565c0] focus:ring-0 outline-none appearance-none cursor-pointer"
                  value={year}
                  onChange={(e) => setYear(Number(e.target.value))}
                >
                  {options.years.map(y => <option key={y} value={y}>{y}</option>)}
                </select>
              </div>
            </div>

            {loadingData && <div className="text-muted py-12 animate-pulse font-serif text-xl">Loading validated profile...</div>}
            
            {error && !loadingData && (
              <div className="py-12 border-l-2 border-[#e23b2a] pl-6 text-[#e23b2a]">
                <p className="text-lg font-light">{error}</p>
              </div>
            )}

            {data && !loadingData && (
              <div className="space-y-16">
                
                <div className="flex flex-col md:flex-row justify-between items-start border-l-4 border-[#1565c0] pl-6 gap-6">
                  <div>
                    <div className="text-[10px] font-semibold text-muted uppercase tracking-[0.2em] mb-2">Resilience Classification</div>
                    <ProfileBadge profile={data.resilience_profile} showLabel className="text-xl bg-transparent px-0 border-none" />
                  </div>
                  <div>
                     <div className="text-[10px] font-semibold text-muted uppercase tracking-[0.2em] mb-2">Interpretation</div>
                     <div className="text-body font-serif text-lg max-w-lg">
                        {data.shock_loss_share > 50 
                          ? "Extremely high vulnerability to dominant supplier, requiring significant alternative capacity."
                          : "Moderate-to-low exposure profile, indicating distributed risk."}
                        {' '}
                        {data.replacement_rate >= 100 
                          ? "Modeled shock was fully absorbed."
                          : "Modeled shock could not be fully absorbed."}
                     </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
                  <div className="border-t border-line pt-4">
                     <div className="text-xs font-semibold text-muted uppercase tracking-widest mb-1">Baseline Imports</div>
                     <div className="text-3xl font-light text-ink font-serif">{fmtLocale(data.baseline_imports)} t</div>
                  </div>
                  <div className="border-t border-line pt-4">
                     <div className="text-xs font-semibold text-muted uppercase tracking-widest mb-1">Import Dependence</div>
                     <div className="text-3xl font-light text-ink font-serif">{data.import_dependence != null ? `${fmt(data.import_dependence, 1)}%` : 'Not available'}</div>
                  </div>
                  <div className="border-t border-line pt-4">
                     <div className="text-xs font-semibold text-muted uppercase tracking-widest mb-1">Dominant Supplier</div>
                     <div className="text-xl font-light text-ink mt-2 break-words leading-tight">{shockData ? shockData.shocked_supplier : 'Loading...'}</div>
                  </div>
                  <div className="border-t border-line pt-4">
                     <div className="text-xs font-semibold text-muted uppercase tracking-widest mb-1">Supplier Share</div>
                     <div className="text-3xl font-light text-ink font-serif">{data.largest_supplier_share != null ? `${fmt(data.largest_supplier_share, 1)}%` : 'Not available'}</div>
                  </div>
                  <div className="border-t border-line pt-4">
                     <div className="text-xs font-semibold text-muted uppercase tracking-widest mb-1">Supplier Count</div>
                     <div className="text-3xl font-light text-ink font-serif">{data.supplier_count != null ? data.supplier_count : 'Not available'}</div>
                  </div>
                </div>

                <div className="border-t border-line pt-8">
                  <h4 className="text-[10px] font-semibold text-muted uppercase tracking-widest mb-6">Modeled Shock & Replacement</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div>
                      <div className="text-sm font-semibold text-ink mb-1">Lost Supply</div>
                      <div className="text-xl font-light text-[#e23b2a]">{fmtLocale(data.lost_supply)} t</div>
                      <div className="text-xs text-muted mt-1">({fmt(data.shock_loss_share, 1)}% of baseline)</div>
                    </div>
                    <div>
                      <div className="text-sm font-semibold text-ink mb-1">Current/Historical Repl.</div>
                      <div className="text-xl font-light text-[#0e9f6a]">{fmtLocale((data.tier1_replacement || 0) + (data.tier2_replacement || 0))} t</div>
                      <div className="text-xs text-muted mt-1">Tier 1 & Tier 2 combined</div>
                    </div>
                    <div>
                      <div className="text-sm font-semibold text-ink mb-1">New-Origin Requirement</div>
                      <div className="text-xl font-light text-[#2a7de1]">{fmtLocale(data.tier3_replacement)} t</div>
                      <div className="text-xs text-muted mt-1">Tier 3 activation</div>
                    </div>
                  </div>
                </div>

              </div>
            )}
          </section>
        )}
      </div>

      {/* COMMODITY COMPARISON */}
      <section>
        <h2 className="text-2xl font-serif text-ink mb-8 uppercase">The six commodities do not face the same exposure</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b-2 border-ink">
                <th className="py-4 text-xs font-semibold text-ink uppercase tracking-widest">Commodity</th>
                <th className="py-4 text-xs font-semibold text-ink uppercase tracking-widest">Mean HHI</th>
                <th className="py-4 text-xs font-semibold text-ink uppercase tracking-widest">Mean Shock-Loss Share</th>
              </tr>
            </thead>
            <tbody>
              {commodityCompareData.map((cmd) => (
                <tr key={cmd.commodity} className="border-b border-line hover:bg-wash transition-colors">
                  <td className="py-4 font-serif text-lg">{cmd.commodity}</td>
                  <td className="py-4 text-lg font-light">{fmt(cmd.mean_hhi, 4)}</td>
                  <td className="py-4 text-lg font-light">{fmt(cmd.mean_shock_loss_share, 1)}%</td>
                </tr>
              ))}
              {commodityCompareData.length === 0 && (
                <tr><td colSpan={3} className="py-4 text-muted text-center">Loading comparison data...</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* EXPLANATORY BLOCKS */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-12">
        <div>
          <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-3">Concentration can be measured more than one way</h3>
          <p className="text-body font-light mb-4">
            <strong className="font-semibold text-ink">HHI</strong> summarizes how concentrated supplier shares are within an importer–commodity system. Higher HHI means import quantities are more concentrated among suppliers.
          </p>
          <details className="group">
            <summary className="text-xs font-semibold text-[#1565c0] uppercase tracking-widest cursor-pointer list-none flex items-center">
              Technical detail
              <span className="ml-2 group-open:rotate-180 transition-transform">&darr;</span>
            </summary>
            <div className="pt-4 text-sm text-muted font-light leading-relaxed">
              HHI ranges from 0 to 1 in the normalized FOODSHIELD representation. Higher values indicate greater concentration.
            </div>
          </details>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-3">How evenly distributed is supply?</h3>
          <p className="text-body font-light mb-4">
            <strong className="font-semibold text-ink">Entropy</strong> measures how distributed supplier shares are. 
            <strong className="font-semibold text-ink ml-2">Supplier Count</strong> is the number of observed foreign suppliers. More suppliers can provide more alternative relationships, but supplier count alone does not describe how evenly supply is distributed.
          </p>
          <details className="group">
            <summary className="text-xs font-semibold text-[#1565c0] uppercase tracking-widest cursor-pointer list-none flex items-center">
              Technical detail
              <span className="ml-2 group-open:rotate-180 transition-transform">&darr;</span>
            </summary>
            <div className="pt-4 text-sm text-muted font-light leading-relaxed">
              Normalized Shannon entropy allows comparison across different supplier counts. FOODSHIELD does not use arbitrary thresholds for "dangerous" entropy.
            </div>
          </details>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-3">Import Dependence</h3>
          <p className="text-body font-light mb-4">
            Import Dependence provides context on the role of foreign supply in the domestic food system. It is defined as Net Imports divided by Domestic Supply.
          </p>
          <details className="group">
            <summary className="text-xs font-semibold text-[#1565c0] uppercase tracking-widest cursor-pointer list-none flex items-center">
              Technical detail
              <span className="ml-2 group-open:rotate-180 transition-transform">&darr;</span>
            </summary>
            <div className="pt-4 text-sm text-muted font-light leading-relaxed">
              Import dependence is descriptive. It does not measure the probability of food shortage or food security risk. Missing observations are left explicitly null.
            </div>
          </details>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-3">Nutritional Context</h3>
          <p className="text-body font-light mb-4">
            Trade exposure can be interpreted alongside the contribution of each commodity to national food supply via Calorie and Protein shares.
          </p>
          <details className="group">
            <summary className="text-xs font-semibold text-[#1565c0] uppercase tracking-widest cursor-pointer list-none flex items-center">
              Technical detail
              <span className="ml-2 group-open:rotate-180 transition-transform">&darr;</span>
            </summary>
            <div className="pt-4 text-sm text-muted font-light leading-relaxed">
              Food Balance Sheet domestic supply includes uses beyond direct human consumption, and national averages do not capture distributional inequality.
            </div>
          </details>
        </div>
      </section>

      {/* SHOCK SEVERITY */}
      <section>
        <h2 className="text-2xl font-serif text-ink mb-4 uppercase">What would a dominant supplier shock actually remove?</h2>
        <p className="text-lg text-body font-light leading-relaxed mb-12">
          On average, removing the largest supplier removes approximately 67.17% of baseline import quantity in the modeled Rank-1 scenarios. This is a modeled trade shock, not a forecast of real-world food availability.
        </p>
        <div className="mb-6">
          <img src="/images/fig02_shock_severity_by_commodity.png" alt="Shock Severity by Commodity" className="w-full border border-line" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-sm pt-4 border-t border-line">
          <div>
            <span className="block font-semibold text-ink uppercase tracking-wider text-xs mb-1">Why it matters</span>
            <span className="text-body">The Rank-1 shock represents a massive disruption that forces the system to rely on alternatives.</span>
          </div>
          <div>
            <span className="block font-semibold text-ink uppercase tracking-wider text-xs mb-1">Source / Scope</span>
            <span className="text-body font-mono text-xs">foodshield_resilience_metrics_2010_2023.csv<br/>Rank 1 | 2011–2023 | Capacity-valid</span>
          </div>
        </div>
      </section>

      {/* CONCEPTUAL BRIDGE / CTA */}
      <section className="py-24 text-center border-t border-line bg-wash">
        <div className="max-w-2xl mx-auto space-y-4 mb-16">
          <div className="p-4 border border-ink bg-white font-semibold uppercase tracking-widest text-sm">
            Import Dependence<br/><span className="text-xs font-light text-muted normal-case mt-1 block">Role of foreign supply</span>
          </div>
          <div className="text-xl text-muted">+</div>
          <div className="p-4 border border-ink bg-white font-semibold uppercase tracking-widest text-sm">
            Supplier Concentration<br/><span className="text-xs font-light text-muted normal-case mt-1 block">Distribution among suppliers</span>
          </div>
          <div className="text-2xl text-muted">&darr;</div>
          <div className="p-4 border border-[#e23b2a] bg-[#e23b2a]/5 text-[#e23b2a] font-semibold uppercase tracking-widest text-sm">
            Dominant Supplier Disruption<br/><span className="text-xs font-light opacity-80 normal-case mt-1 block">Modeled loss if largest supplier disappears</span>
          </div>
          <div className="text-2xl text-muted">&darr;</div>
          <div className="p-4 border border-[#1565c0] bg-[#1565c0] text-white font-semibold uppercase tracking-widest text-sm">
            Replacement Analysis<br/><span className="text-xs font-light opacity-90 normal-case mt-1 block">Can the lost import quantity be replaced?</span>
          </div>
        </div>
        
        <p className="text-2xl font-serif text-ink mb-12">
          Concentration tells us how much is exposed.<br/>
          The next question is what happens when we actually remove the supplier.
        </p>
        
        <Link 
          to="/shock" 
          className="inline-flex items-center justify-center px-12 py-5 bg-ink text-white text-sm font-semibold tracking-widest uppercase hover:bg-[#1a365d] transition-colors"
        >
          SIMULATE THE SHOCK &rarr;
        </Link>
      </section>

    </div>
  );
};
