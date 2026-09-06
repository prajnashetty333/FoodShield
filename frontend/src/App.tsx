import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { ExecutiveOverview } from './pages/ExecutiveOverview';
import { CountryExplorer } from './pages/CountryExplorer';
import { CommodityExplorer } from './pages/CommodityExplorer';
import { SupplierShock } from './pages/SupplierShock';
import { ReplacementPathway } from './pages/ReplacementPathway';
import { Sensitivity } from './pages/Sensitivity';
import { PolicyDecision } from './pages/PolicyDecision';
import { Methodology } from './pages/Methodology';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<ExecutiveOverview />} />
          <Route path="country" element={<CountryExplorer />} />
          <Route path="commodity" element={<CommodityExplorer />} />
          <Route path="shock" element={<SupplierShock />} />
          <Route path="replacement" element={<ReplacementPathway />} />
          <Route path="sensitivity" element={<Sensitivity />} />
          <Route path="policy" element={<PolicyDecision />} />
          <Route path="methodology" element={<Methodology />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
