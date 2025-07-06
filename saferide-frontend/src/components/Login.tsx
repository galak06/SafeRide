import React, { useState } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import './Login.css'

// TypeScript interface for login form state - follows Single Responsibility Principle
interface LoginFormState {
  email: string
  password: string
  isLoading: boolean
  error: string
}

// Accept onLogin as a prop
const Login: React.FC<{ onLogin: (email: string, password: string) => Promise<void> }> = ({ onLogin }) => {
  const { t } = useLanguage()
  
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
      setFormState(prev => ({ ...prev, error: t('auth.loginError') }))
      return
    }

    // Custom email validation (stricter than HTML5)
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(formState.email) || /\.\./.test(formState.email)) {
      setFormState(prev => ({ ...prev, error: t('auth.loginError') }))
      return
    }

    setFormState(prev => ({ ...prev, isLoading: true, error: '' }))

    try {
      // Call the onLogin prop
      await onLogin(formState.email.trim(), formState.password.trim())
    } catch (error) {
      setFormState(prev => ({ 
        ...prev, 
        error: t('auth.loginError')
      }))
    } finally {
      setFormState(prev => ({ ...prev, isLoading: false }))
    }
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>SafeRide</h1>
          <p>{t('auth.login')}</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form" aria-label="login form">
          {formState.error && (
            <div className="error-message">
              {formState.error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">{t('auth.email')}</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formState.email}
              onChange={handleInputChange}
              placeholder={t('auth.email')}
              disabled={formState.isLoading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">{t('auth.password')}</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formState.password}
              onChange={handleInputChange}
              placeholder={t('auth.password')}
              disabled={formState.isLoading}
              required
            />
          </div>

          <button 
            type="submit" 
            className="login-button"
            disabled={formState.isLoading}
          >
            {formState.isLoading ? t('common.loading') : t('auth.loginButton')}
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