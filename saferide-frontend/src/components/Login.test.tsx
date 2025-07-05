import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Login from './Login';
import type { LoginCredentials, AuthResponse } from '../models';

// Mock the userService
jest.mock('../services/userService', () => ({
  userService: {
    authenticateUser: jest.fn(),
  },
}));

// Import the mocked service
import { userService } from '../services/userService';

describe('Login Component', () => {
  const mockOnLoginSuccess = jest.fn();
  const mockAuthenticateUser = userService.authenticateUser as jest.MockedFunction<typeof userService.authenticateUser>;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders login form', () => {
    render(<Login onLoginSuccess={mockOnLoginSuccess} />);
    
    // Check if the login form elements are rendered
    expect(screen.getByRole('heading', { name: /SafeRide/i })).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  test('displays form fields correctly', () => {
    render(<Login onLoginSuccess={mockOnLoginSuccess} />);
    
    const emailInput = screen.getByPlaceholderText(/email/i);
    const passwordInput = screen.getByPlaceholderText(/password/i);
    
    expect(emailInput).toHaveAttribute('type', 'email');
    expect(passwordInput).toHaveAttribute('type', 'password');
  });

  test('handles form submission with valid credentials', async () => {
    const mockAuthResponse: AuthResponse = {
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
    };

    mockAuthenticateUser.mockResolvedValue(mockAuthResponse);

    render(<Login onLoginSuccess={mockOnLoginSuccess} />);
    
    const emailInput = screen.getByPlaceholderText(/email/i);
    const passwordInput = screen.getByPlaceholderText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockAuthenticateUser).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      } as LoginCredentials);
      // The component calls onLoginSuccess with just the token
      expect(mockOnLoginSuccess).toHaveBeenCalledWith('mock-token-123');
    });
  });

  test('handles form submission with invalid credentials', async () => {
    const mockAuthResponse: AuthResponse = {
      success: false,
      message: 'Invalid email or password'
    };

    mockAuthenticateUser.mockResolvedValue(mockAuthResponse);

    render(<Login onLoginSuccess={mockOnLoginSuccess} />);
    
    const emailInput = screen.getByPlaceholderText(/email/i);
    const passwordInput = screen.getByPlaceholderText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    fireEvent.change(emailInput, { target: { value: 'wrong@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockAuthenticateUser).toHaveBeenCalledWith({
        email: 'wrong@example.com',
        password: 'wrongpassword'
      } as LoginCredentials);
      expect(mockOnLoginSuccess).not.toHaveBeenCalled();
    });
  });

  test('handles authentication error', async () => {
    mockAuthenticateUser.mockRejectedValue(new Error('Network error'));

    render(<Login onLoginSuccess={mockOnLoginSuccess} />);
    
    const emailInput = screen.getByPlaceholderText(/email/i);
    const passwordInput = screen.getByPlaceholderText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockAuthenticateUser).toHaveBeenCalled();
      expect(mockOnLoginSuccess).not.toHaveBeenCalled();
    });
  });

  test('validates required fields', async () => {
    render(<Login onLoginSuccess={mockOnLoginSuccess} />);
    
    const submitButton = screen.getByRole('button', { name: /sign in/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockAuthenticateUser).not.toHaveBeenCalled();
    });
  });
}); 