import React from 'react';
import { ResilienceProfile } from '../types';

interface ProfileBadgeProps {
  profile: string;
  className?: string;
  showLabel?: boolean;
}

const colorMap: Record<string, string> = {
  'A': 'bg-[#0e9f6a]/10 text-[#0e9f6a] border-[#0e9f6a]/30',
  'B': 'bg-[#2bbf8a]/10 text-[#2bbf8a] border-[#2bbf8a]/30',
  'C': 'bg-[#2a7de1]/10 text-[#2a7de1] border-[#2a7de1]/30',
  'D': 'bg-[#e23b2a]/10 text-[#e23b2a] border-[#e23b2a]/30',
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
                       
  const colors = colorMap[shortProfile] || 'bg-wash text-muted border-line';
  const label = labelMap[shortProfile] || profile;

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded border text-xs font-medium ${colors} ${className}`}>
      {shortProfile}
      {showLabel && <span className="ml-2 pl-2 border-l border-current/30">{label}</span>}
    </span>
  );
};
