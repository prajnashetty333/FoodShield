import React from 'react';
import { Link } from 'react-router-dom';

export const NetworkStory = () => {
  return (
    <div className="space-y-32 max-w-5xl mx-auto">
      {/* HEADER */}
      <section className="border-b border-line pb-16">
        <p className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-4">03 &mdash; The Network</p>
        <h1 className="text-5xl md:text-6xl font-normal text-ink font-serif mb-8 leading-tight">
          Who actually supplies whom &mdash; and how stable are those relationships?
        </h1>
        <p className="text-xl text-body font-light leading-relaxed max-w-3xl">
          FOODSHIELD does not treat international food trade as a collection of isolated import totals. 
          It represents trade as a supplier network. The purpose of this chapter is to understand how broad, 
          persistent, and changing those supplier relationships are before a supplier shock is introduced.
        </p>
      </section>

      {/* NETWORK SCALE */}
      <section className="bg-wash p-12 border border-line">
        <h2 className="text-[10px] font-semibold text-muted mb-12 uppercase tracking-[0.2em]">Network Scale (2010–2023)</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-y-16 gap-x-12">
          <div className="border-l-2 border-[#1565c0] pl-6">
            <div className="text-4xl font-light text-ink mb-2 font-serif">128,486</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Network Edges / Relationships</div>
          </div>
          <div className="border-l-2 border-[#1565c0] pl-6">
            <div className="text-4xl font-light text-ink mb-2 font-serif">25,497</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Importer–Supplier–Commodity</div>
          </div>
          <div className="border-l-2 border-[#1565c0] pl-6">
            <div className="text-4xl font-light text-ink mb-2 font-serif">10,229</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Importer–Supplier Pairs</div>
          </div>
          <div className="border-l-2 border-line pl-6">
            <div className="text-4xl font-light text-ink mb-2 font-serif">178</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Importers</div>
          </div>
          <div className="border-l-2 border-line pl-6">
            <div className="text-4xl font-light text-ink mb-2 font-serif">197</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Suppliers</div>
          </div>
          <div className="border-l-2 border-line pl-6">
            <div className="text-4xl font-light text-ink mb-2 font-serif">14</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Trade-Analysis Years</div>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 pt-8 border-t border-line">
          <div>
            <div className="text-sm font-semibold text-ink mb-1">Average suppliers per system</div>
            <div className="text-2xl font-light text-body font-serif">10.98</div>
          </div>
          <div>
            <div className="text-sm font-semibold text-ink mb-1">Median suppliers per system</div>
            <div className="text-2xl font-light text-body font-serif">9</div>
          </div>
          <div>
            <div className="text-sm font-semibold text-ink mb-1">Maximum suppliers observed</div>
            <div className="text-2xl font-light text-body font-serif">79</div>
          </div>
        </div>
      </section>

      {/* NETWORK VISUAL */}
      <section>
        <h2 className="text-[10px] font-semibold text-muted mb-8 uppercase tracking-[0.2em] text-center">Conceptual Network Topology</h2>
        <div className="bg-paper border border-line py-20 px-8 flex flex-col items-center justify-center relative overflow-hidden">
          
          <div className="w-full max-w-2xl flex flex-col items-center">
            
            {/* Top Node */}
            <div className="z-10 bg-white border-2 border-ink py-3 px-6 shadow-sm rounded-sm mb-12">
              <span className="text-sm font-bold tracking-widest uppercase text-ink">Importer</span>
            </div>
            
            {/* SVG Connecting Lines */}
            <svg className="absolute w-full h-[120px] top-[100px] pointer-events-none" preserveAspectRatio="none">
              <path d="M 50% 0 L 20% 120" stroke="#d1d5db" strokeWidth="2" fill="none" strokeDasharray="4 4" />
              <path d="M 50% 0 L 35% 120" stroke="#d1d5db" strokeWidth="2" fill="none" />
              <path d="M 50% 0 L 50% 120" stroke="#1565c0" strokeWidth="3" fill="none" />
              <path d="M 50% 0 L 65% 120" stroke="#d1d5db" strokeWidth="2" fill="none" />
              <path d="M 50% 0 L 80% 120" stroke="#d1d5db" strokeWidth="2" fill="none" strokeDasharray="4 4" />
            </svg>
            
            {/* Middle Nodes (Suppliers) */}
            <div className="z-10 flex w-full justify-between items-center mb-12 relative px-4">
               <div className="bg-wash border border-muted py-2 px-4 rounded-sm opacity-50 hidden sm:block">
                  <span className="text-xs font-semibold tracking-wider uppercase text-muted">Supplier 1</span>
               </div>
               <div className="bg-wash border border-muted py-2 px-4 rounded-sm">
                  <span className="text-xs font-semibold tracking-wider uppercase text-muted">Supplier 2</span>
               </div>
               <div className="bg-[#eff6ff] border-2 border-[#1565c0] py-4 px-6 rounded-sm shadow-sm scale-110">
                  <span className="text-sm font-bold tracking-widest uppercase text-[#1565c0]">Largest Supplier</span>
               </div>
               <div className="bg-wash border border-muted py-2 px-4 rounded-sm">
                  <span className="text-xs font-semibold tracking-wider uppercase text-muted">Supplier 4</span>
               </div>
               <div className="bg-wash border border-muted py-2 px-4 rounded-sm opacity-50 hidden sm:block">
                  <span className="text-xs font-semibold tracking-wider uppercase text-muted">Supplier 5</span>
               </div>
            </div>

            {/* Bottom Nodes (Commodities) */}
            <div className="z-10 bg-white border border-line py-3 px-6 shadow-sm rounded-sm">
              <span className="text-sm font-semibold tracking-widest uppercase text-body">Commodity Flows</span>
            </div>

          </div>
        </div>
      </section>

      {/* THE NETWORK IS BROAD BUT NOT STATIC */}
      <section>
        <h2 className="text-2xl font-serif text-ink mb-6 uppercase">The network is broad &mdash; but not static</h2>
        <p className="text-lg text-body font-light leading-relaxed mb-8">
          Across 2010&ndash;2023, FOODSHIELD observes thousands of importer&ndash;supplier relationships across the six selected commodities. 
          However, relationships do not necessarily persist continuously. Supplier relationships are often intermittent rather than continuously active.
          This matters because a supplier that existed historically may not be an active supplier in a particular shock year.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mt-12 pt-12 border-t border-line">
          <div>
            <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-8">Relationship Persistence</h3>
            <div className="space-y-6">
              <div className="flex justify-between items-end border-b border-line pb-2">
                <span className="text-body font-light">Average active years per pairing</span>
                <span className="text-2xl font-serif text-ink">5.04 <span className="text-base text-muted font-sans">years</span></span>
              </div>
              <div className="flex justify-between items-end border-b border-line pb-2">
                <span className="text-body font-light">Average persistence</span>
                <span className="text-2xl font-serif text-ink">35.99%</span>
              </div>
              <div className="flex justify-between items-end border-b border-line pb-2">
                <span className="text-body font-light">Median persistence</span>
                <span className="text-2xl font-serif text-ink">21.43%</span>
              </div>
            </div>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-ink uppercase tracking-widest mb-8">Network Turnover</h3>
            <div className="space-y-6">
              <div className="flex justify-between items-end border-b border-line pb-2">
                <span className="text-body font-light">New entries observed</span>
                <span className="text-2xl font-serif text-[#0e9f6a]">34,534</span>
              </div>
              <div className="flex justify-between items-end border-b border-line pb-2">
                <span className="text-body font-light">Exits observed</span>
                <span className="text-2xl font-serif text-[#e23b2a]">31,420</span>
              </div>
            </div>
            <p className="text-sm text-muted font-light leading-relaxed mt-4">
              Observed supplier relationships enter and leave the network over time.
            </p>
          </div>
        </div>
      </section>

      {/* WHY PERSISTENCE MATTERS FOR REPLACEMENT */}
      <section className="bg-ink text-white p-12">
        <h2 className="text-2xl font-serif mb-6 uppercase text-white">Why history matters for the shock</h2>
        <p className="text-lg font-light leading-relaxed text-gray-300 mb-12">
          A supplier network is not simply a list of countries. Some suppliers are active now. Some were observed historically. 
          Others have no qualifying prior bilateral relationship. The FOODSHIELD replacement model treats those situations differently.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="border border-gray-700 p-6">
            <h3 className="text-sm font-semibold uppercase tracking-widest text-gray-400 mb-2">Tier 1</h3>
            <div className="text-xl font-serif mb-4">Current Suppliers</div>
            <p className="text-sm text-gray-400 font-light">Suppliers active in the shock year.</p>
          </div>
          <div className="border border-gray-700 p-6">
            <h3 className="text-sm font-semibold uppercase tracking-widest text-gray-400 mb-2">Tier 2</h3>
            <div className="text-xl font-serif mb-4">Historical Suppliers</div>
            <p className="text-sm text-gray-400 font-light">Suppliers that supplied the same importer and commodity in at least two distinct pre-shock years but are absent in the shock year.</p>
          </div>
          <div className="border border-gray-700 p-6">
            <h3 className="text-sm font-semibold uppercase tracking-widest text-gray-400 mb-2">Tier 3</h3>
            <div className="text-xl font-serif mb-4">New Origins</div>
            <p className="text-sm text-gray-400 font-light">Eligible new origins with no qualifying prior bilateral relationship, providing modeled contribution from a new origin.</p>
          </div>
        </div>
      </section>

      {/* EXPLANATORY BLOCKS */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-16">
        <div>
          <h3 className="text-xl font-serif text-ink uppercase mb-4">A large network does not mean an even network</h3>
          <p className="text-body font-light leading-relaxed mb-6">
            An importer may have many observed suppliers while still receiving a large share of imports from a small number of suppliers. 
            Therefore, <strong>Supplier count &ne; Supplier concentration</strong> and <strong>Supplier concentration &ne; Shock loss</strong>.
          </p>
          <div className="bg-wash border border-line p-6 flex flex-col items-center justify-center text-center space-y-2">
            <div className="text-sm font-semibold uppercase tracking-widest text-ink">Supplier Count</div>
            <div className="text-xl text-muted">+</div>
            <div className="text-sm font-semibold uppercase tracking-widest text-ink">Supplier Shares</div>
            <div className="text-xl text-muted">&darr;</div>
            <div className="text-sm font-semibold uppercase tracking-widest text-body bg-white border border-line py-2 px-4 w-full">Network Structure</div>
          </div>
        </div>

        <div>
          <h3 className="text-xl font-serif text-ink uppercase mb-4">Network structure is not the same as resilience</h3>
          <p className="text-body font-light leading-relaxed mb-6">
            The network chapter describes <em>observed trade relationships</em>. 
            The later shock and replacement chapters test what happens under a <em>defined counterfactual supplier disappearance</em>.
          </p>
          <ul className="space-y-4 text-sm font-light text-body border-l-2 border-line pl-6">
            <li><strong className="font-semibold text-ink">Observed network</strong> &rarr; descriptive evidence</li>
            <li><strong className="font-semibold text-ink">Supplier shock</strong> &rarr; counterfactual experiment</li>
            <li><strong className="font-semibold text-ink">Replacement model</strong> &rarr; modeled recovery feasibility</li>
            <li><strong className="font-semibold text-ink">Resilience profile</strong> &rarr; classification of the modeled outcome</li>
          </ul>
        </div>
      </section>

      {/* NETWORK FLOW SCALE */}
      <section className="text-center">
        <h2 className="text-[10px] font-semibold text-muted mb-4 uppercase tracking-[0.2em]">Network Quantity</h2>
        <div className="text-5xl md:text-7xl font-light text-ink font-serif mb-6">5,124,398,255</div>
        <div className="text-sm font-semibold text-body uppercase tracking-widest mb-8">Tonnes</div>
        <p className="text-body font-light max-w-2xl mx-auto text-sm">
          Network quantity represented in the Step 7B analytical network across the six locked commodities (Wheat, Rice, Maize, Palm Oil, Sugar, Sunflower Oil). 
          The network quantity reconciles exactly to the Step 6A bilateral quantity after excluding self-trade and zero/null flows.
        </p>
      </section>

      {/* TRANSITION */}
      <section className="py-24 text-center border-t border-line bg-wash">
        <h2 className="text-3xl font-serif text-ink mb-12 leading-relaxed">
          We know the network.<br/>
          Now remove its dominant supplier.
        </h2>
        
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
