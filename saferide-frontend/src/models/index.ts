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

// Types
export type { Location } from './types/location'

// Interfaces
export type { User } from './interfaces/user'
export type { Ride } from './interfaces/ride'
export type { UserPreferences } from './interfaces/user_preferences'
export type { 
  ParentChildRelationship, 
  ParentChildRelationshipCreate, 
  ParentChildRelationshipUpdate, 
  UserRelationships 
} from './interfaces/parent_child_relationship'

// Enums
export { RelationshipType } from './interfaces/parent_child_relationship'

// Request Models
export type { RouteRequest } from './requests/route_request'
export type { RideRequest } from './requests/ride_request'
export type { LoginCredentials } from './requests/login_credentials'

// Response Models
export type { RouteResponse } from './responses/route_response'
export type { TrafficAlert } from './responses/traffic_alert'
export type { RideResponse, DriverInfo } from './responses/ride_response'
export type { AuthResponse } from './responses/auth_response' 