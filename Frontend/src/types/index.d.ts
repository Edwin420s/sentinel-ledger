// Type declarations for JavaScript users (IDE support)

declare module '*.css' {
  const content: { [className: string]: string };
  export default content;
}

declare module '*.svg' {
  const content: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  export default content;
}

declare module '*.png' {
  const content: string;
  export default content;
}

declare module '*.jpg' {
  const content: string;
  export default content;
}

// Environment variables
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_WS_URL: string;
  readonly VITE_LOG_LEVEL: string;
  readonly VITE_SENTRY_DSN?: string;
  readonly VITE_GA_TRACKING_ID?: string;
  readonly VITE_ENABLE_MOCK_API?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

// Global types
type RiskLevel = 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
type Chain = 'base' | 'ethereum' | 'both';
type DexType = 'uniswap' | 'aerodrome' | 'other';
type FlagSeverity = 'info' | 'warning' | 'critical';
type EventType = 'new_token' | 'high_risk' | 'rug_detected' | 'liquidity_change' | 'ownership_change';