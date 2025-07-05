import { renderHook, act, waitFor } from '@testing-library/react';
import { useAuth } from '../../hooks/useAuth';
import type { User, AuthResponse } from '../../models';

// Mock the userService
jest.mock('../../services/userService', () => ({
  userService: {
    authenticateUser: jest.fn(),
    getUserById: jest.fn(),
    getCurrentUser: jest.fn(),
    logout: jest.fn()
  }
}));

// Mock the apiService
jest.mock('../../services/apiService', () => ({
  apiService: {
    setToken: jest.fn(),
    clearToken: jest.fn()
  }
}));

import { userService } from '../../services/userService';
import { apiService } from '../../services/apiService';

const mockUserService = userService as jest.Mocked<typeof userService>;
const mockApiService = apiService as jest.Mocked<typeof apiService>;

describe('useAuth Hook', () => {
  const mockUser: User = {
    id: '1',
    email: 'test@example.com',
    password: 'password123',
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
  };

  // Helper function to create user without password
  const createUserWithoutPassword = (user: User) => {
    const { password, ...userWithoutPassword } = user;
    return userWithoutPassword;
  };

  beforeEach(() => {
    jest.clearAllMocks();
    // Clear localStorage before each test
    localStorage.clear();
  });

  describe('Initial State', () => {
    test('initializes with default state when no stored auth', async () => {
      mockUserService.getCurrentUser.mockResolvedValue(null);
      
      const { result } = renderHook(() => useAuth());

      await waitFor(() => {
        expect(result.current.user).toBeNull();
        expect(result.current.token).toBeNull();
        expect(result.current.isAuthenticated).toBe(false);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBeNull();
      });
    });

    test('initializes with stored auth data from localStorage', async () => {
      const userWithoutPassword = createUserWithoutPassword(mockUser);
      
      localStorage.setItem('authToken', 'stored-token-123');
      mockUserService.getCurrentUser.mockResolvedValue(mockUser);

      const { result } = renderHook(() => useAuth());

      await waitFor(() => {
        expect(result.current.user).toEqual(userWithoutPassword);
        expect(result.current.token).toBe('stored-token-123');
        expect(result.current.isAuthenticated).toBe(true);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBeNull();
      });
    });
  });

  describe('Login Functionality', () => {
    test('successfully logs in user', async () => {
      const authResponse: AuthResponse = {
        success: true,
        message: 'Login successful',
        user: { ...mockUser },
        token: 'new-token-123'
      };

      mockUserService.authenticateUser.mockResolvedValue(authResponse);

      const { result } = renderHook(() => useAuth());

      await act(async () => {
        await result.current.login('test@example.com', 'password123');
      });

      await waitFor(() => {
        expect(mockUserService.authenticateUser).toHaveBeenCalledWith({
          email: 'test@example.com',
          password: 'password123'
        });
        expect(mockApiService.setToken).toHaveBeenCalledWith('new-token-123');
        expect(result.current.user).toEqual({ ...mockUser });
        expect(result.current.token).toBe('new-token-123');
        expect(result.current.isAuthenticated).toBe(true);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBeNull();
      });
    });

    test('handles login failure', async () => {
      const authResponse: AuthResponse = {
        success: false,
        message: 'Invalid credentials'
      };

      mockUserService.authenticateUser.mockResolvedValue(authResponse);
      mockUserService.getCurrentUser.mockResolvedValue(null); // Ensure user is null after failed login

      const { result } = renderHook(() => useAuth());

      await act(async () => {
        await result.current.login('test@example.com', 'wrongpassword');
      });

      await waitFor(() => {
        expect(mockUserService.authenticateUser).toHaveBeenCalledWith({
          email: 'test@example.com',
          password: 'wrongpassword'
        });
        expect(mockApiService.setToken).not.toHaveBeenCalled();
        expect(result.current.user).toBeNull();
        expect(result.current.token).toBeNull();
        expect(result.current.isAuthenticated).toBe(false);
        expect(result.current.isLoading).toBe(false);
        expect(result.current.error).toBe('Invalid credentials');
      });
    });
  });
}); 