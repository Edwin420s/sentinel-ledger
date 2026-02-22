import { useEffect, useRef, useState, useCallback } from 'react';
import { wsService } from '../services/api/websocket';

export const useWebSocket = (event, callback) => {
  const [isConnected, setIsConnected] = useState(false);
  const callbackRef = useRef(callback);

  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  useEffect(() => {
    const handleEvent = (data) => {
      callbackRef.current?.(data);
    };

    wsService.on(event, handleEvent);
    
    // Connect if not already connected
    if (!wsService.socket) {
      wsService.connect();
      wsService.socket?.on('connect', () => setIsConnected(true));
      wsService.socket?.on('disconnect', () => setIsConnected(false));
    }

    return () => {
      wsService.off(event, handleEvent);
    };
  }, [event]);

  const subscribe = useCallback((tokenAddress) => {
    wsService.subscribe(tokenAddress);
  }, []);

  const unsubscribe = useCallback((tokenAddress) => {
    wsService.unsubscribe(tokenAddress);
  }, []);

  return { isConnected, subscribe, unsubscribe };
};