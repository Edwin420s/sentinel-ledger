import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/v1/tokens', () => {
    return HttpResponse.json([
      {
        address: '0x123...',
        name: 'Test Token',
        symbol: 'TEST',
        riskScore: { final: 45, level: 'MODERATE' },
      },
    ]);
  }),
  
  http.get('/api/v1/health', () => {
    return HttpResponse.json({
      status: 'healthy',
      uptime: '99.9%',
      version: '1.0.0',
    });
  }),
];