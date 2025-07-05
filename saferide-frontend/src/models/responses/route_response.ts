import { Location } from '../types/location'

/**
 * Route response interface for route calculation results
 */
export interface RouteResponse {
  distance: number
  duration: number
  traffic_delay: number
  route_points: Location[]
  eta: string
} 