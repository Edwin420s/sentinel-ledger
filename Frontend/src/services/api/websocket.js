import { io } from 'socket.io-client';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.listeners = new Map();
  }

  connect() {
    if (this.socket) return;

    const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
    
    this.socket = io(WS_URL, {
      transports: ['websocket'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5,
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    // Handle different event types
    this.socket.on('new_token', (data) => {
      this.emit('new_token', data);
    });

    this.socket.on('risk_alert', (data) => {
      this.emit('risk_alert', data);
    });

    this.socket.on('liquidity_change', (data) => {
      this.emit('liquidity_change', data);
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event).add(callback);
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).delete(callback);
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => callback(data));
    }
  }

  subscribe(tokenAddress) {
    if (this.socket) {
      this.socket.emit('subscribe', { token: tokenAddress });
    }
  }

  unsubscribe(tokenAddress) {
    if (this.socket) {
      this.socket.emit('unsubscribe', { token: tokenAddress });
    }
  }
}

export const wsService = new WebSocketService();