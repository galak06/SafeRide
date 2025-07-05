import type {
  User,
  Ride,
  UserPreferences,
  LoginCredentials,
  AuthResponse
} from '../models'

// User service class - follows Single Responsibility Principle
class UserService {
  private baseUrl: string = 'http://localhost:8000'

  // Authenticate user - follows Single Responsibility Principle
  public async authenticateUser(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
        credentials: 'include', // Send cookies
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        return {
          success: false,
          message: errorData.detail || 'Login failed'
        }
      }

      const loginData = await response.json()
      
      // Extract token and user from the response
      const token = loginData.access_token
      const user = loginData.user
      
      return {
        success: true,
        message: 'Login successful',
        user,
        token
      }
    } catch (error) {
      console.error('Authentication error:', error)
      return {
        success: false,
        message: 'Network error during login'
      }
    }
  }

  // Get current user from backend - follows Single Responsibility Principle
  public async getCurrentUser(token?: string): Promise<User | null> {
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      }
      
      // If token is provided, use Authorization header (for localStorage-based auth)
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      const response = await fetch(`${this.baseUrl}/api/auth/me`, {
        headers,
        credentials: 'include', // Include cookies for cookie-based auth
      })

      if (!response.ok) {
        return null
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to get current user:', error)
      return null
    }
  }

  // Logout user
  public async logout(): Promise<void> {
    await fetch(`${this.baseUrl}/api/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    })
  }

  // Get user by ID - follows Single Responsibility Principle
  public async getUserById(id: string, token?: string): Promise<User | null> {
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      }
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      const response = await fetch(`${this.baseUrl}/api/users/${id}`, {
        headers
      })

      if (!response.ok) {
        return null
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to get user:', error)
      return null
    }
  }

  // Get user by email - follows Single Responsibility Principle
  public async getUserByEmail(email: string, token?: string): Promise<User | null> {
    // For now, we'll need to get all users and filter - implement proper endpoint later
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      }
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      // This would need a proper endpoint in the backend
      const response = await fetch(`${this.baseUrl}/api/users?email=${encodeURIComponent(email)}`, {
        headers
      })

      if (!response.ok) {
        return null
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to get user by email:', error)
      return null
    }
  }

  // Add new ride to user history - follows Single Responsibility Principle
  public async addRideToHistory(userId: string, destination: string, token?: string): Promise<Ride | null> {
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      }
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      const rideRequest = {
        user_id: userId,
        origin: {
          lat: 40.7128,
          lng: -74.0060,
          address: 'Current Location'
        },
        destination: {
          lat: 40.7589,
          lng: -73.9851,
          address: destination
        },
        passenger_count: 1
      }

      const response = await fetch(`${this.baseUrl}/api/rides`, {
        method: 'POST',
        headers,
        body: JSON.stringify(rideRequest)
      })

      if (!response.ok) {
        return null
      }

      const rideData = await response.json()
      return {
        id: rideData.ride_id,
        destination,
        status: rideData.status,
        createdAt: new Date().toISOString()
      }
    } catch (error) {
      console.error('Failed to add ride to history:', error)
      return null
    }
  }

  // Get user ride history - follows Single Responsibility Principle
  public async getUserRideHistory(userId: string, token?: string): Promise<Ride[]> {
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      }
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      // This would need a proper endpoint in the backend
      const response = await fetch(`${this.baseUrl}/api/users/${userId}/rides`, {
        headers
      })

      if (!response.ok) {
        return []
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to get ride history:', error)
      return []
    }
  }

  // Update user preferences - follows Single Responsibility Principle
  public async updateUserPreferences(userId: string, preferences: Partial<UserPreferences>, token?: string): Promise<boolean> {
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      }
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      // This would need a proper endpoint in the backend
      const response = await fetch(`${this.baseUrl}/api/users/${userId}/preferences`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(preferences)
      })

      return response.ok
    } catch (error) {
      console.error('Failed to update preferences:', error)
      return false
    }
  }

  // Load users from backend - follows Single Responsibility Principle
  public async loadUsers(token?: string): Promise<void> {
    // This method is used by tests to load users into memory
    // In a real implementation, this would cache users locally
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      }
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      const response = await fetch(`${this.baseUrl}/api/users`, {
        headers
      })

      if (!response.ok) {
        console.warn('Failed to load users from backend')
      }
    } catch (error) {
      console.error('Failed to load users:', error)
    }
  }

  // Get all users without passwords - follows Single Responsibility Principle
  public async getAllUsers(token?: string): Promise<Omit<User, 'password'>[]> {
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      }
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      const response = await fetch(`${this.baseUrl}/api/users`, {
        headers
      })

      if (!response.ok) {
        return []
      }

      const users = await response.json()
      // Remove passwords from response
      return users.map((user: any) => {
        const { password, ...userWithoutPassword } = user
        return userWithoutPassword
      })
    } catch (error) {
      console.error('Failed to get all users:', error)
      return []
    }
  }
}

// Export singleton instance - follows Singleton pattern
export const userService = new UserService() 