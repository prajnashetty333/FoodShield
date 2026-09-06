import React from 'react';

interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  className?: string;
}

export const KPICard: React.FC<KPICardProps> = ({ title, value, subtitle, className = '' }) => {
  return (
    <div className={`bg-paper border border-line p-6 transition-colors hover:bg-wash ${className}`}>
      <h3 className="text-[10px] font-semibold text-muted mb-2 uppercase tracking-widest">{title}</h3>
      <div className="text-3xl font-light text-ink font-sans">{value}</div>
      {subtitle && <p className="text-xs text-muted mt-2 font-light">{subtitle}</p>}
    </div>
  );
};
