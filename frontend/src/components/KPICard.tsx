import React from 'react';

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  className?: string;
}

export const KPICard: React.FC<KPICardProps> = ({ title, value, subtitle, className = '' }) => {
  return (
    <div className={`bg-slate-900 border border-slate-800 border-t-2 border-t-blue-600 p-5 rounded-lg shadow-sm ${className}`}>
      <h3 className="text-xs font-medium text-slate-400 mb-2 uppercase tracking-widest">{title}</h3>
      <div className="text-3xl font-light text-slate-100">{value}</div>
      {subtitle && <p className="text-xs text-slate-500 mt-2">{subtitle}</p>}
    </div>
  );
};
