import type {
  RouteRequest,
  RouteResponse,
  TrafficAlert,
  RideRequest,
  RideResponse
} from '../models'

// API service class - follows Single Responsibility Principle
class ApiService {
  private baseUrl: string
  private token: string | null = null

  constructor() {
    // Use default URL for simplicity - can be overridden via environment variables in production
    this.baseUrl = 'http://localhost:8000'
  }

  // Set authentication token - follows Single Responsibility Principle
  setToken(token: string): void {
    this.token = token
  }

  // Clear authentication token - follows Single Responsibility Principle
  clearToken(): void {
    this.token = null
  }

  // Get headers with authentication - follows Single Responsibility Principle
  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json'
    }

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    return headers
  }

  // Generic API request method - follows Dependency Inversion Principle
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    
    const config: RequestInit = {
      ...options,
      headers: {
        ...this.getHeaders(),
        ...options.headers
      }
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error)
      throw error
    }
  }

  // Health check - follows Single Responsibility Principle
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return this.request<{ status: string; timestamp: string }>('/api/health')
  }

  // Calculate route - follows Single Responsibility Principle
  async calculateRoute(routeRequest: RouteRequest): Promise<RouteResponse> {
    return this.request<RouteResponse>('/api/route', {
      method: 'POST',
      body: JSON.stringify(routeRequest)
    })
  }

  // Get traffic alerts - follows Single Responsibility Principle
  async getTrafficAlerts(area: string): Promise<TrafficAlert[]> {
    return this.request<TrafficAlert[]>(`/api/traffic/${encodeURIComponent(area)}`)
  }

  // Create ride - follows Single Responsibility Principle
  async createRide(rideRequest: RideRequest): Promise<RideResponse> {
    return this.request<RideResponse>('/api/rides', {
      method: 'POST',
      body: JSON.stringify(rideRequest)
    })
  }

  // Confirm ride - follows Single Responsibility Principle
  async confirmRide(rideId: string): Promise<RideResponse> {
    return this.request<RideResponse>(`/api/rides/${rideId}/confirm`, {
      method: 'POST'
    })
  }

  // Get ride status - follows Single Responsibility Principle
  async getRideStatus(rideId: string): Promise<RideResponse> {
    return this.request<RideResponse>(`/api/rides/${rideId}`)
  }

  // Mock method for backward compatibility - follows Open/Closed Principle
  async simulateRideBooking(destination: string): Promise<{ success: boolean; message: string }> {
    try {
      // Create a mock ride request
      const rideRequest: RideRequest = {
        user_id: '1', // Mock user ID
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

      const ride = await this.createRide(rideRequest)
      
      return {
        success: true,
        message: `Ride booked successfully! Ride ID: ${ride.ride_id}, Estimated fare: $${ride.fare_estimate.toFixed(2)}`
      }
    } catch (error) {
      return {
        success: false,
        message: 'Failed to book ride. Please try again.'
      }
    }
  }
}

// Export singleton instance - follows Singleton pattern
export const apiService = new ApiService() 