/**
 * Models package for SafeRide frontend.
 * 
 * This package contains all TypeScript interfaces and types organized by category:
 * - types/ - Basic types like Location
 * - interfaces/ - Complex interfaces like User, Ride
 * - requests/ - Request interfaces for API calls
 * - responses/ - Response interfaces for API responses
 * - enums/ - Enum types
 */

// Export all interfaces
export type { User } from './interfaces/user'
export type { Ride } from './interfaces/ride'
export type { UserPreferences } from './interfaces/user_preferences'
export type { Child, ChildCreate, ChildUpdate } from './interfaces/child'
export type { 
  ParentChildRelationship, 
  ParentChildRelationshipCreate, 
  ParentChildRelationshipUpdate,
  UserRelationships 
} from './interfaces/parent_child_relationship'

// Export all enums
export { RelationshipType } from './interfaces/parent_child_relationship'

// Export all request types
export type { LoginCredentials } from './requests/login_credentials'
export type { RideRequest } from './requests/ride_request'
export type { RouteRequest } from './requests/route_request'

// Export all response types
export type { AuthResponse } from './responses/auth_response'
export type { RideResponse } from './responses/ride_response'
export type { RouteResponse } from './responses/route_response'
export type { TrafficAlert } from './responses/traffic_alert'

// Export all types
export type { Location } from './types/location' 