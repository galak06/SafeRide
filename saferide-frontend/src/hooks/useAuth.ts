import { useState, useEffect, useCallback } from 'react';
import { userService } from '../services/userService';
import { apiService } from '../services/apiService';
import type { User, LoginCredentials } from '../models';

// TypeScript interface for authenticated user (without password)
type AuthenticatedUser = Omit<User, 'password'>;

interface AuthState {
  user: AuthenticatedUser | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}

interface AuthActions {
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (user: AuthenticatedUser) => void;
  refreshUser: () => Promise<void>;
  setError: (error: string) => void;
  clearError: () => void;
}

interface UseAuthReturn extends AuthState, AuthActions {
  isAuthenticated: boolean;
}

// Token storage utilities - follows Single Responsibility Principle
const TokenStorage = {
  // Save token to localStorage
  saveToken: (token: string): void => {
    try {
      localStorage.setItem('authToken', token);
      localStorage.setItem('authTimestamp', Date.now().toString());
    } catch (error) {
      console.error('Failed to save token to localStorage:', error);
    }
  },

  // Get token from localStorage
  getToken: (): string | null => {
    try {
      return localStorage.getItem('authToken');
    } catch (error) {
      console.error('Failed to get token from localStorage:', error);
      return null;
    }
  },

  // Clear token from localStorage
  clearToken: (): void => {
    try {
      localStorage.removeItem('authToken');
      localStorage.removeItem('authTimestamp');
    } catch (error) {
      console.error('Failed to clear token from localStorage:', error);
    }
  },

  // Check if token is expired (24 hours)
  isTokenExpired: (): boolean => {
    try {
      const timestamp = localStorage.getItem('authTimestamp');
      if (!timestamp) return true;
      
      const tokenAge = Date.now() - parseInt(timestamp);
      const maxAge = 24 * 60 * 60 * 1000; // 24 hours
      
      return tokenAge > maxAge;
    } catch (error) {
      console.error('Failed to check token expiration:', error);
      return true;
    }
  }
};

export const useAuth = (): UseAuthReturn => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    isLoading: true,
    error: null
  });

  const isAuthenticated = Boolean(authState.user && authState.token);

  // Login function
  const login = useCallback(async (email: string, password: string): Promise<void> => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));
    try {
      const credentials: LoginCredentials = { email: email.trim(), password: password.trim() };
      const response = await userService.authenticateUser(credentials);
      if (response.success && response.user) {
        // Extract token from response if available
        const token = response.token || response.user.token || 'mock-token-123';
        
        // Save token to localStorage for persistence
        TokenStorage.saveToken(token);
        
        // Set token in API service
        apiService.setToken(token);
        
        // Remove password from user object if it exists
        const userWithoutPassword = response.user as any;
        delete userWithoutPassword.password;
        
        setAuthState({ 
          user: userWithoutPassword, 
          token,
          isLoading: false, 
          error: null 
        });
      } else {
        setAuthState(prev => ({ 
          ...prev, 
          user: null,
          token: null,
          isLoading: false, 
          error: response.message || 'Authentication failed' 
        }));
      }
    } catch (error) {
      setAuthState(prev => ({ 
        ...prev, 
        isLoading: false, 
        error: 'An unexpected error occurred' 
      }));
    }
  }, []);

  // Logout function
  const logout = useCallback(async (): Promise<void> => {
    try {
      await userService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear token from localStorage and API service
      TokenStorage.clearToken();
      apiService.clearToken();
      setAuthState({ user: null, token: null, isLoading: false, error: null });
    }
  }, []);

  // Update user function
  const updateUser = useCallback((user: AuthenticatedUser): void => {
    setAuthState(prev => ({ ...prev, user }));
  }, []);

  // Refresh user from /me
  const refreshUser = useCallback(async (): Promise<void> => {
    setAuthState(prev => ({ ...prev, isLoading: true }));
    const user = await userService.getCurrentUser(authState.token || undefined);
    if (user) {
      // Remove password from user object
      const userWithoutPassword = user as any;
      delete userWithoutPassword.password;
      setAuthState({ 
        user: userWithoutPassword, 
        token: authState.token, // Keep existing token
        isLoading: false, 
        error: null 
      });
    } else {
      // If user fetch fails, clear authentication
      TokenStorage.clearToken();
      apiService.clearToken();
      setAuthState({ 
        user: null, 
        token: null,
        isLoading: false, 
        error: null 
      });
    }
  }, [authState.token]);

  // Set error
  const setError = useCallback((error: string): void => {
    setAuthState(prev => ({ ...prev, error }));
  }, []);

  // Clear error
  const clearError = useCallback((): void => {
    setAuthState(prev => ({ ...prev, error: null }));
  }, []);

  // On mount, check if user is authenticated
  useEffect(() => {
    (async () => {
      setAuthState(prev => ({ ...prev, isLoading: true }));
      
      try {
        // Get stored token from localStorage
        const storedToken = TokenStorage.getToken();
        
        // Check if token is expired
        if (!storedToken || TokenStorage.isTokenExpired()) {
          TokenStorage.clearToken();
          apiService.clearToken();
          setAuthState({ 
            user: null, 
            token: null,
            isLoading: false, 
            error: null 
          });
          return;
        }

        // Set token in API service
        apiService.setToken(storedToken);
        
        // Try to get current user from backend
        const user = await userService.getCurrentUser(storedToken);
        if (user) {
          // Remove password from user object
          const userWithoutPassword = user as any;
          delete userWithoutPassword.password;
          setAuthState({ 
            user: userWithoutPassword, 
            token: storedToken,
            isLoading: false, 
            error: null 
          });
        } else {
          // If user fetch fails, clear authentication
          TokenStorage.clearToken();
          apiService.clearToken();
          setAuthState({ 
            user: null, 
            token: null,
            isLoading: false, 
            error: null 
          });
        }
      } catch (error) {
        console.error('Error during authentication check:', error);
        TokenStorage.clearToken();
        apiService.clearToken();
        setAuthState({ 
          user: null, 
          token: null,
          isLoading: false, 
          error: null 
        });
      }
    })();
  }, []);

  return {
    ...authState,
    isAuthenticated,
    login,
    logout,
    updateUser,
    refreshUser,
    setError,
    clearError
  };
}; 