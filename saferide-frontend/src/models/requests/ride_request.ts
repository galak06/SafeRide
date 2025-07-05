import { Location } from '../types/location'

/**
 * Ride request interface for booking rides
 */
export interface RideRequest {
  user_id: string
  origin: Location
  destination: Location
  passenger_count: number
} 