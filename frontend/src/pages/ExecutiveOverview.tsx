import React from 'react';
import { Link } from 'react-router-dom';

export const ExecutiveOverview = () => {
  return (
    <div className="space-y-32 max-w-5xl mx-auto">
      {/* 1. HERO SECTION */}
      <section className="relative pt-12 pb-24 border-b border-line">
        {/* Subtle grid background animation */}
        <div className="absolute inset-0 -z-10 overflow-hidden opacity-20 pointer-events-none">
          <div className="w-full h-[200%] bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:40px_40px] animate-grid-pan" />
        </div>
        
        <p className="text-xs font-semibold text-[#1565c0] uppercase tracking-[0.2em] mb-6">Food Trade Resilience</p>
        <h1 className="text-5xl md:text-7xl font-normal text-ink tracking-tight font-serif mb-12">
          FOODSHIELD
        </h1>
        
        <h2 className="text-2xl md:text-4xl font-light text-ink leading-tight mb-8">
          Can a food-importing country replace a major foreign supplier after a sudden loss?
        </h2>
        
        <p className="text-lg md:text-xl text-body font-light leading-relaxed max-w-3xl mb-16">
          FOODSHIELD investigates whether existing trade relationships can absorb a major supplier shock — or whether resilience requires historically observed suppliers or entirely new origins.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-6">
          <Link 
            to="/country" 
            className="inline-flex items-center justify-center px-8 py-4 bg-ink text-white text-sm font-semibold tracking-widest uppercase hover:bg-[#1a365d] transition-colors"
          >
            START THE INVESTIGATION &rarr;
          </Link>
          <Link 
            to="/methodology" 
            className="inline-flex items-center justify-center px-8 py-4 bg-transparent border border-ink text-ink text-sm font-semibold tracking-widest uppercase hover:bg-wash transition-colors"
          >
            EXPLORE THE EVIDENCE
          </Link>
        </div>
      </section>

      {/* 2. RESEARCH QUESTION / CONCEPT FLOW */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-24 items-start">
        <div>
          <h2 className="text-2xl font-serif text-ink mb-6">
            WHAT HAPPENS WHEN YOUR<br/>LARGEST SUPPLIER DISAPPEARS?
          </h2>
          <div className="space-y-6 text-lg text-body font-light leading-relaxed">
            <p>
              For each importer &times; commodity &times; year system, FOODSHIELD removes the dominant supplier and asks whether the lost import quantity can be replaced through:
            </p>
            <ul className="space-y-4 pt-4">
              <li className="flex gap-4">
                <span className="font-serif italic text-muted">Tier 1</span>
                <span>Current-year suppliers</span>
              </li>
              <li className="flex gap-4">
                <span className="font-serif italic text-muted">Tier 2</span>
                <span>Historically observed suppliers</span>
              </li>
              <li className="flex gap-4">
                <span className="font-serif italic text-muted">Tier 3</span>
                <span>New origins</span>
              </li>
            </ul>
          </div>
        </div>
        
        {/* Visual Flow diagram */}
        <div className="bg-wash border border-line p-8 md:p-12 flex flex-col items-center text-center">
          <div className="w-full max-w-xs space-y-2">
            <div className="py-3 px-4 border border-ink bg-paper text-sm font-medium text-ink uppercase tracking-wider">Largest Supplier</div>
            <div className="text-muted h-6 flex items-center justify-center text-xl">&darr;</div>
            
            <div className="py-3 px-4 bg-[#e23b2a] text-white text-sm font-medium uppercase tracking-wider">Supplier Shock</div>
            <div className="text-muted h-6 flex items-center justify-center text-xl">&darr;</div>
            
            <div className="py-3 px-4 border border-[#e23b2a] bg-paper text-[#e23b2a] text-sm font-medium uppercase tracking-wider">Lost Supply</div>
            <div className="text-muted h-6 flex items-center justify-center text-xl">&darr;</div>
            
            <div className="py-3 px-4 border border-[#0e9f6a] bg-[#f0fdf4] text-[#0e9f6a] text-sm font-medium uppercase tracking-wider flex justify-between">
              <span className="opacity-70">Tier 1</span><span>Current Suppliers</span>
            </div>
            <div className="text-muted h-6 flex items-center justify-center text-xl">&darr;</div>
            
            <div className="py-3 px-4 border border-[#2bbf8a] bg-[#f0fdf4] text-[#2bbf8a] text-sm font-medium uppercase tracking-wider flex justify-between">
              <span className="opacity-70">Tier 2</span><span>Historical Suppliers</span>
            </div>
            <div className="text-muted h-6 flex items-center justify-center text-xl">&darr;</div>
            
            <div className="py-3 px-4 border border-[#2a7de1] bg-[#eff6ff] text-[#2a7de1] text-sm font-medium uppercase tracking-wider flex justify-between">
              <span className="opacity-70">Tier 3</span><span>New Origins</span>
            </div>
            <div className="text-muted h-6 flex items-center justify-center text-xl">&darr;</div>
            
            <div className="py-3 px-4 border border-muted bg-paper text-muted text-sm font-medium uppercase tracking-wider">Unreplaced Supply</div>
          </div>
        </div>
      </section>

      {/* 3. SCALE / EVIDENCE SECTION */}
      <section className="border-t border-line pt-24 pb-12">
        <h2 className="text-[10px] font-semibold text-muted mb-16 uppercase tracking-[0.2em] text-center">The Scale of the Investigation</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-y-20 gap-x-12">
          <div className="border-l-2 border-[#1565c0] pl-6">
            <div className="text-5xl font-light text-ink mb-4 font-serif">10,953</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Modeled Dominant Supplier<br/>Disruption Scenarios</div>
          </div>
          
          <div className="border-l-2 border-[#1565c0] pl-6">
            <div className="text-5xl font-light text-ink mb-4 font-serif">6</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Locked<br/>Commodities</div>
          </div>
          
          <div className="border-l-2 border-[#1565c0] pl-6">
            <div className="text-5xl font-light text-ink mb-4 font-serif">13 Years</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Capacity-Valid<br/>Primary Analysis</div>
          </div>
          
          <div className="border-l-2 border-[#e6a817] pl-6">
            <div className="text-5xl font-light text-ink mb-4 font-serif">~67%</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Mean Share of<br/>Imports Lost</div>
          </div>
          
          <div className="border-l-2 border-[#0e9f6a] pl-6">
            <div className="text-5xl font-light text-ink mb-4 font-serif">99.83%</div>
            <div className="text-xs font-semibold text-body uppercase tracking-widest">Mean Modeled<br/>Replacement</div>
          </div>
        </div>
      </section>
    </div>
  );
};
