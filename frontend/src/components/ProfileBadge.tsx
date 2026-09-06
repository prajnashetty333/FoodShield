import React from 'react';
import { ResilienceProfile } from '../types';

interface ProfileBadgeProps {
  profile: string;
  className?: string;
  showLabel?: boolean;
}

const colorMap: Record<string, string> = {
  'A': 'bg-[#935073]/10 text-[#502D55] border-[#935073]/30',
  'B': 'bg-[#935073]/10 text-[#502D55] border-[#935073]/30',
  'C': 'bg-[#F6DBC0] text-[#502D55] border-[#935073]/30',
  'D': 'bg-[#935073]/20 text-[#502D55] border-[#935073]/50',
};

const labelMap: Record<string, string> = {
  'A': 'Current suppliers',
  'B': 'Historical suppliers',
  'C': 'New origins',
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
