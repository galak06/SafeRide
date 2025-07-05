import { Location } from '../types/location'

/**
 * Route request interface for calculating routes
 */
export interface RouteRequest {
  origin: Location
  destination: Location
  mode: string
} 