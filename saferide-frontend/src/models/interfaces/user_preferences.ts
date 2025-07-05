/**
 * User preferences interface
 */
export interface UserPreferences {
  defaultPaymentMethod: 'card' | 'paypal' | 'cash'
  notifications: boolean
  language: string
} 