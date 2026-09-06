import React from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { Sidebar } from './Sidebar';

export const Layout = () => {
  const { pathname } = useLocation();
  const journey = [
    { path: '/', label: 'The Question' },
    { path: '/country', label: 'The Exposure' },
    { path: '/network', label: 'The Network' },
    { path: '/shock', label: 'The Shock' },
    { path: '/replacement', label: 'The Replacement' },
    { path: '/sensitivity', label: 'The Robustness' },
    { path: '/policy', label: 'The Decision' },
    { path: '/methodology', label: 'The Methodology' },
  ];
  const index = journey.findIndex((item) => item.path === pathname);
  const previous = index > 0 ? journey[index - 1] : null;
  const next = index >= 0 && index < journey.length - 1 ? journey[index + 1] : null;

  return (
    <div className="flex min-h-screen flex-col md:flex-row bg-paper text-body">
      <Sidebar />
      <main className="flex-1 overflow-x-hidden flex flex-col">
        <div className="max-w-[1440px] mx-auto w-full p-5 sm:p-8 md:p-12 lg:p-20 flex-1">
          <nav aria-label="Research journey controls" className="mb-10 flex flex-wrap items-center justify-between gap-4 border-b border-line pb-5">
            {previous ? <Link to={previous.path} className="text-xs font-semibold uppercase tracking-widest text-body hover:text-ink transition-colors">← Previous: {previous.label}</Link> : <span />}
            {next && <Link to={next.path} className="inline-flex items-center bg-ink px-5 py-3 text-xs font-semibold uppercase tracking-widest text-white hover:bg-[#935073] transition-colors">Next step: {next.label} →</Link>}
          </nav>
          <Outlet />
        </div>
        <footer className="border-t border-line py-8 px-8 md:px-16 lg:px-24 bg-wash mt-auto">
          <div className="max-w-[1440px] mx-auto">
            <p className="text-xs text-muted leading-relaxed max-w-3xl">
              <strong className="text-ink font-medium">Disclaimer:</strong> FOODSHIELD is a modeled trade-replacement framework. It is not a forecast or guarantee of real-world food security. The analysis relies on the historical export-expansion capacity proxy and assumes trade flows can be perfectly reallocated up to observed historical limits.
            </p>
          </div>
        </footer>
      </main>
    </div>
  );
};
