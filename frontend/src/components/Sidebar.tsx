import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Globe, 
  Package, 
  Zap, 
  GitMerge, 
  SlidersHorizontal, 
  FileText, 
  BookOpen 
} from 'lucide-react';

const navItems = [
  { path: '/', label: '01 Executive Overview', icon: LayoutDashboard },
  { path: '/country', label: '02 Country Explorer', icon: Globe },
  { path: '/commodity', label: '03 Commodity Explorer', icon: Package },
  { path: '/shock', label: '04 Supplier Shock', icon: Zap },
  { path: '/replacement', label: '05 Replacement Pathway', icon: GitMerge },
  { path: '/sensitivity', label: '06 Sensitivity', icon: SlidersHorizontal },
  { path: '/policy', label: '07 Policy & Decision', icon: FileText },
  { path: '/methodology', label: '08 Methodology', icon: BookOpen },
];

export const Sidebar = () => {
  return (
    <div className="w-64 bg-[#fffdf8] border-r border-slate-800 h-screen sticky top-0 flex flex-col">
      <div className="p-7 border-b border-slate-800">
        <h1 className="text-xl font-semibold text-slate-100 tracking-wide">FOODSHIELD</h1>
        <p className="text-[10px] text-slate-500 mt-2 uppercase tracking-[0.2em] font-semibold">Research Intelligence</p>
      </div>
      
      <nav className="flex-1 px-4 py-5 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-[#f0f6fb] text-[#1565c0] border border-[#b8d5ef]'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-[#f0f6fb]'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              {item.label}
            </NavLink>
          );
        })}
      </nav>
      
      <div className="p-5 border-t border-slate-800">
        <div className="text-[10px] text-slate-500 leading-tight">
          FOODSHIELD modeled trade-replacement framework. Not a real-world food security guarantee.
        </div>
      </div>
    </div>
  );
};
