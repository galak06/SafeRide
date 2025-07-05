import React, { useState } from 'react'
import './Login.css'
import { userService } from '../services/userService'
import type { AuthResponse } from '../models/responses/auth_response'
import type { LoginCredentials } from '../models/requests/login_credentials'

// TypeScript interface for login form state - follows Single Responsibility Principle
interface LoginFormState {
  email: string
  password: string
  isLoading: boolean
  error: string
}

// Accept onLogin as a prop
const Login: React.FC<{ onLogin: (email: string, password: string) => Promise<void> }> = ({ onLogin }) => {
  // Using TypeScript typing annotation for form state management
  const [formState, setFormState] = useState<LoginFormState>({
    email: '',
    password: '',
    isLoading: false,
    error: ''
  })

  // Event handler with proper TypeScript typing for input changes
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = event.target
    setFormState(prev => ({
      ...prev,
      [name]: value,
      error: '' // Clear error when user starts typing
    }))
  }

  // Event handler for form submission with proper error handling
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault()
    
    if (!formState.email || !formState.password) {
      setFormState(prev => ({ ...prev, error: 'Please fill in all fields' }))
      return
    }

    // Custom email validation (stricter than HTML5)
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(formState.email) || /\.\./.test(formState.email)) {
      setFormState(prev => ({ ...prev, error: 'Please enter a valid email address' }))
      return
    }

    setFormState(prev => ({ ...prev, isLoading: true, error: '' }))

    try {
      // Call the onLogin prop
      await onLogin(formState.email.trim(), formState.password.trim())
    } catch (error) {
      setFormState(prev => ({ 
        ...prev, 
        error: 'An unexpected error occurred. Please try again.' 
      }))
    } finally {
      setFormState(prev => ({ ...prev, isLoading: false }))
    }
  }

  // Use user service for authentication - follows Dependency Inversion principle
  const authenticateUser = async (credentials: LoginCredentials): Promise<AuthResponse> => {
    // Simulate network delay for better UX
    await new Promise(resolve => setTimeout(resolve, 800))
    
    return await userService.authenticateUser(credentials)
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>SafeRide</h1>
          <p>Sign in to your account</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form" aria-label="login form">
          {formState.error && (
            <div className="error-message">
              {formState.error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formState.email}
              onChange={handleInputChange}
              placeholder="Enter your email"
              disabled={formState.isLoading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formState.password}
              onChange={handleInputChange}
              placeholder="Enter your password"
              disabled={formState.isLoading}
              required
            />
          </div>

          <button 
            type="submit" 
            className="login-button"
            disabled={formState.isLoading}
          >
            {formState.isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="login-footer">
          <p>Test credentials:</p>
          <p>• admin@saferide.com / admin123</p>
          <p>• test@example.com / testpass</p>
          <a href="#" className="forgot-password">Forgot password?</a>
        </div>
      </div>
    </div>
  )
}

export default Login 