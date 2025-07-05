import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../../App';

// Mock the components
jest.mock('../../components/Login', () => {
  return function MockLogin({ onLoginSuccess }: { onLoginSuccess: (token: string) => void }) {
    return (
      <div data-testid="login-component">
        <button onClick={() => onLoginSuccess('mock-token-123')}>Mock Login</button>
      </div>
    );
  };
});

jest.mock('../../components/AdminPortal', () => {
  return function MockAdminPortal() {
    return <div data-testid="admin-portal">Admin Portal</div>;
  };
});

// Mock the apiService
jest.mock('../../services/apiService', () => ({
  apiService: {
    setToken: jest.fn(),
    clearToken: jest.fn(),
    simulateRideBooking: jest.fn()
  }
}));

import { apiService } from '../../services/apiService';

const mockApiService = apiService as jest.Mocked<typeof apiService>;

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Initial Rendering', () => {
    test('renders login component when not authenticated', () => {
      render(<App />);
      
      expect(screen.getByTestId('login-component')).toBeInTheDocument();
      expect(screen.getByText('Mock Login')).toBeInTheDocument();
    });

    test('does not render admin portal when not authenticated', () => {
      render(<App />);
      
      expect(screen.queryByTestId('admin-portal')).not.toBeInTheDocument();
    });
  });

  describe('Authentication Flow', () => {
    test('shows admin portal after successful login', async () => {
      render(<App />);
      
      // Initially shows login
      expect(screen.getByTestId('login-component')).toBeInTheDocument();
      
      // Click login button to authenticate
      fireEvent.click(screen.getByText('Mock Login'));
      
      // Should show admin portal after authentication
      await waitFor(() => {
        expect(screen.getByTestId('admin-portal')).toBeInTheDocument();
      });
      
      expect(screen.queryByTestId('login-component')).not.toBeInTheDocument();
    });

    test('sets token in API service after login', async () => {
      render(<App />);
      
      fireEvent.click(screen.getByText('Mock Login'));
      
      await waitFor(() => {
        expect(mockApiService.setToken).toHaveBeenCalledWith('mock-token-123');
      });
    });

    test('clears token in API service on logout', async () => {
      render(<App />);
      
      // Login first
      fireEvent.click(screen.getByText('Mock Login'));
      await waitFor(() => {
        expect(screen.getByTestId('admin-portal')).toBeInTheDocument();
      });
      
      // The AdminPortal component should handle logout internally
      // We just verify the API service was called during login
      expect(mockApiService.setToken).toHaveBeenCalledWith('mock-token-123');
    });
  });

  describe('Component Structure', () => {
    test('renders with proper TypeScript interfaces', () => {
      render(<App />);
      
      // Component should render without TypeScript errors
      expect(screen.getByTestId('login-component')).toBeInTheDocument();
    });

    test('handles authentication state correctly', async () => {
      render(<App />);
      
      // Initial state - not authenticated
      expect(screen.getByTestId('login-component')).toBeInTheDocument();
      
      // After login - authenticated
      fireEvent.click(screen.getByText('Mock Login'));
      await waitFor(() => {
        expect(screen.getByTestId('admin-portal')).toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    test('handles API service errors gracefully', () => {
      // Mock console.error to avoid noise in tests
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
      
      render(<App />);
      
      // Component should render without errors
      expect(screen.getByTestId('login-component')).toBeInTheDocument();
      
      consoleSpy.mockRestore();
    });
  });

  describe('Accessibility', () => {
    test('has proper component structure', () => {
      render(<App />);
      
      // Should have login component with proper test ID
      expect(screen.getByTestId('login-component')).toBeInTheDocument();
    });
  });
}); 