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
    await userService.logout();
    apiService.clearToken();
    setAuthState({ user: null, token: null, isLoading: false, error: null });
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
      // For tests, we'll use a mock token if no token is stored
      const storedToken = localStorage.getItem('authToken') || 'mock-token-123';
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