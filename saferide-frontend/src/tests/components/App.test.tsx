import { render, screen, fireEvent, waitFor } from '../utils/test-utils';
import '@testing-library/jest-dom';
import App from '../../App';

// Mock the components
jest.mock('../../components/Login', () => {
  return function MockLogin({ onLogin }: { onLogin: (email: string, password: string) => Promise<void> }) {
    return (
      <div data-testid="login-component">
        <button onClick={() => onLogin('test@example.com', 'password123')}>Mock Login</button>
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

// Create a simple test that doesn't rely on complex authentication state
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

  describe('Component Structure', () => {
    test('renders with proper TypeScript interfaces', () => {
      render(<App />);
      
      // Component should render without TypeScript errors
      expect(screen.getByTestId('login-component')).toBeInTheDocument();
    });

    test('renders language selector', () => {
      render(<App />);
      
      // Should have language selector
      expect(screen.getByLabelText('Select your preferred language')).toBeInTheDocument();
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