export const getRiskLevelFromScore = (score) => {
  if (score < 30) return 'LOW';
  if (score < 60) return 'MODERATE';
  if (score < 80) return 'HIGH';
  return 'CRITICAL';
};

export const getRiskColor = (level) => {
  const colors = {
    LOW: 'text-risk-low',
    MODERATE: 'text-risk-moderate',
    HIGH: 'text-risk-high',
    CRITICAL: 'text-risk-critical',
  };
  return colors[level] || 'text-primary-400';
};

export const getRiskBg = (level) => {
  const backgrounds = {
    LOW: 'bg-risk-low/10',
    MODERATE: 'bg-risk-moderate/10',
    HIGH: 'bg-risk-high/10',
    CRITICAL: 'bg-risk-critical/10',
  };
  return backgrounds[level] || 'bg-primary-800';
};

export const getRiskBorder = (level) => {
  const borders = {
    LOW: 'border-risk-low/20',
    MODERATE: 'border-risk-moderate/20',
    HIGH: 'border-risk-high/20',
    CRITICAL: 'border-risk-critical/20',
  };
  return borders[level] || 'border-primary-700';
};