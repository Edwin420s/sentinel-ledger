import toast from 'react-hot-toast';

export class AppError extends Error {
  constructor(message, code, status = 500) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.status = status;
  }
}

export const handleApiError = (error) => {
  console.error('API Error:', error);

  let message = 'An unexpected error occurred';
  let code = 'UNKNOWN_ERROR';

  if (error.response) {
    // Server responded with error
    message = error.response.data?.message || `Error ${error.response.status}`;
    code = error.response.data?.code || `HTTP_${error.response.status}`;
    
    switch (error.response.status) {
      case 400:
        message = 'Bad request - please check your input';
        break;
      case 401:
        message = 'Unauthorized - please check your API key';
        break;
      case 403:
        message = 'Forbidden - insufficient permissions';
        break;
      case 404:
        message = 'Resource not found';
        break;
      case 429:
        message = 'Rate limit exceeded - please try again later';
        break;
      case 500:
        message = 'Server error - please try again later';
        break;
      case 503:
        message = 'Service temporarily unavailable';
        break;
    }
  } else if (error.request) {
    // Request made but no response
    message = 'Network error - please check your connection';
    code = 'NETWORK_ERROR';
  }

  toast.error(message);
  return new AppError(message, code);
};

export const handleWebSocketError = (error) => {
  console.error('WebSocket Error:', error);
  toast.error('Connection error - attempting to reconnect...');
};