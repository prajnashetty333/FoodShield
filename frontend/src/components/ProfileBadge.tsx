import React from 'react';
import { ResilienceProfile } from '../types';

interface ProfileBadgeProps {
  profile: string;
  className?: string;
  showLabel?: boolean;
}

const colorMap: Record<string, string> = {
  'A': 'bg-green-500/20 text-green-400 border-green-500/30',
  'B': 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  'C': 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  'D': 'bg-red-500/20 text-red-400 border-red-500/30',
};

const labelMap: Record<string, string> = {
  'A': 'Existing-network resilient',
  'B': 'Historically recoverable',
  'C': 'New-origin dependent',
  'D': 'Structurally constrained',
};

export const ProfileBadge: React.FC<ProfileBadgeProps> = ({ profile, className = '', showLabel = false }) => {
  // Handle full names returned from API
  const shortProfile = profile.startsWith('Existing') ? 'A' :
                       profile.startsWith('Historic') ? 'B' :
                       profile.startsWith('New-') ? 'C' :
                       profile.startsWith('Structural') ? 'D' : profile;
                       
  const colors = colorMap[shortProfile] || 'bg-slate-500/20 text-slate-400 border-slate-500/30';
  const label = labelMap[shortProfile] || profile;

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded border text-xs font-medium ${colors} ${className}`}>
      {shortProfile}
      {showLabel && <span className="ml-2 pl-2 border-l border-current/30">{label}</span>}
    </span>
  );
};
