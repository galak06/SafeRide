import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Login from '../../components/Login';

// Mock the userService
jest.mock('../../services/userService', () => ({
  userService: {
    authenticateUser: jest.fn()
  }
}));

import { userService } from '../../services/userService';

const mockUserService = userService as jest.Mocked<typeof userService>;

describe('Login Component', () => {
  const mockOnLoginSuccess = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    mockUserService.authenticateUser.mockResolvedValue({
      success: true,
      message: 'Login successful',
      user: {
        id: '1',
        email: 'test@example.com',
        name: 'Test User',
        phone: '1234567890',
        profilePicture: null,
        createdAt: '2023-01-01T00:00:00Z',
        updatedAt: '2023-01-01T00:00:00Z',
        rideHistory: [],
        preferences: {
          defaultPaymentMethod: 'card',
          notifications: true,
          language: 'en'
        }
      },
      token: 'mock-token-123'
    });
  });

  describe('Component Rendering', () => {
    test('renders login form with all elements', () => {
      render(<Login onLoginSuccess={mockOnLoginSuccess} />);
      
      expect(screen.getByText('SafeRide')).toBeInTheDocument();
      expect(screen.getByText('Sign in to your account')).toBeInTheDocument();
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
      expect(screen.getByText(/test credentials/i)).toBeInTheDocument();
      expect(screen.getByText(/demo@saferide.com \/ password/i)).toBeInTheDocument();
      expect(screen.getByText(/john@example.com \/ password123/i)).toBeInTheDocument();
      expect(screen.getByText(/forgot password/i)).toBeInTheDocument();
    });

    test('renders form with correct input types', () => {
      render(<Login onLoginSuccess={mockOnLoginSuccess} />);
      
      const emailInput = screen.getByLabelText(/email/i);
      const passwordInput = screen.getByLabelText(/password/i);
      
      expect(emailInput).toHaveAttribute('type', 'email');
      expect(passwordInput).toHaveAttribute('type', 'password');
    });

    test('renders form with correct placeholders', () => {
      render(<Login onLoginSuccess={mockOnLoginSuccess} />);
      
      const emailInput = screen.getByLabelText(/email/i);
      const passwordInput = screen.getByLabelText(/password/i);
      
      expect(emailInput).toHaveAttribute('placeholder', 'Enter your email');
      expect(passwordInput).toHaveAttribute('placeholder', 'Enter your password');
    });

    test('renders form with required attributes', () => {
      render(<Login onLoginSuccess={mockOnLoginSuccess} />);
      
      const emailInput = screen.getByLabelText(/email/i);
      const passwordInput = screen.getByLabelText(/password/i);
      
      expect(emailInput).toBeRequired();
      expect(passwordInput).toBeRequired();
    });

    test('renders with correct CSS classes', () => {
      render(<Login onLoginSuccess={mockOnLoginSuccess} />);
      
      const form = screen.getByRole('form', { name: /login form/i });
      const submitButton = screen.getByRole('button', { name: /sign in/i });
      
      expect(form).toHaveClass('login-form');
      expect(submitButton).toHaveClass('login-button');
    });
  });

  describe('Form Validation', () => {
    test('shows error when submitting empty form', async () => {
      render(<Login onLoginSuccess={mockOnLoginSuccess} />);
      
      const form = screen.getByRole('form', { name: /login form/i });
      
      fireEvent.submit(form);
      
      await waitFor(() => {
        expect(screen.getByText(/please fill in all fields/i)).toBeInTheDocument();
      });
      
      expect(mockUserService.authenticateUser).not.toHaveBeenCalled();
    });

    test('shows error when email is empty', async () => {
      render(<Login onLoginSuccess={mockOnLoginSuccess} />);
      
      const passwordInput = screen.getByLabelText(/password/i);
      const form = screen.getByRole('form', { name: /login form/i });
      
      fireEvent.change(passwordInput, { target: { value: 'password123' } });
      fireEvent.submit(form);
      
      await waitFor(() => {
        expect(screen.getByText(/please fill in all fields/i)).toBeInTheDocument();
      });
    });

    test('shows error when password is empty', async () => {
      render(<Login onLoginSuccess={mockOnLoginSuccess} />);
      
      const emailInput = screen.getByLabelText(/email/i);
      const form = screen.getByRole('form', { name: /login form/i });
      
      fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
      fireEvent.submit(form);
      
      await waitFor(() => {
        expect(screen.getByText(/please fill in all fields/i)).toBeInTheDocument();
      });
    });
  });
}); 