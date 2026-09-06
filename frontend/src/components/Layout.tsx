import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';

export const Layout = () => {
  return (
    <div className="flex min-h-screen bg-paper text-body">
      <Sidebar />
      <main className="flex-1 overflow-x-hidden flex flex-col">
        <div className="max-w-[1440px] mx-auto w-full p-8 md:p-16 lg:p-24 flex-1">
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
