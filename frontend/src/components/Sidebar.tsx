import { NavLink } from 'react-router-dom';

const navItems = [
  { path: '/', number: '01', label: 'THE QUESTION' },
  { path: '/country', number: '02', label: 'THE EXPOSURE' },
  { path: '/network', number: '03', label: 'THE NETWORK' },
  { path: '/shock', number: '04', label: 'THE SHOCK' },
  { path: '/replacement', number: '05', label: 'THE RECOVERY' },
  { path: '/sensitivity', number: '06', label: 'THE ROBUSTNESS' },
  { path: '/policy', number: '07', label: 'THE DECISION' },
  { path: '/methodology', number: '08', label: 'THE METHOD' },
];

export const Sidebar = () => {
  return (
    <div className="w-[320px] bg-paper border-r border-line h-screen sticky top-0 flex flex-col shrink-0">
      <div className="p-10 border-b border-line">
        <h1 className="text-2xl font-normal text-ink tracking-tight font-serif mb-1">FOODSHIELD</h1>
        <p className="text-[10px] text-muted uppercase tracking-[0.2em] font-medium">Food Trade Resilience</p>
      </div>
      
      <nav className="flex-1 px-10 py-12 space-y-6 overflow-y-auto">
        <div className="text-[10px] font-semibold text-muted mb-8 uppercase tracking-[0.2em]">Research Journey</div>
        
        <div className="relative">
          {/* Vertical connection line */}
          <div className="absolute left-[11px] top-4 bottom-4 w-px bg-line -z-10" />
          
          <div className="space-y-8">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-start gap-5 group transition-all duration-300 ${
                    isActive ? 'opacity-100' : 'opacity-60 hover:opacity-100'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <div className={`mt-1 flex items-center justify-center w-6 h-6 rounded-full border-2 bg-paper transition-colors duration-300 ${
                      isActive ? 'border-[#1565c0] shadow-[0_0_0_2px_rgba(21,101,192,0.2)]' : 'border-line group-hover:border-muted'
                    }`}>
                      {isActive && <div className="w-2 h-2 rounded-full bg-[#1565c0]" />}
                    </div>
                    <div>
                      <div className={`text-xs font-serif italic mb-0.5 transition-colors ${
                        isActive ? 'text-[#1565c0]' : 'text-muted'
                      }`}>
                        {item.number}
                      </div>
                      <div className={`text-sm font-semibold tracking-widest uppercase transition-colors ${
                        isActive ? 'text-ink' : 'text-body'
                      }`}>
                        {item.label}
                      </div>
                    </div>
                  </>
                )}
              </NavLink>
            ))}
          </div>
        </div>
      </nav>
      
    </div>
  );
};
