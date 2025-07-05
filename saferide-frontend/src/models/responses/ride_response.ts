/**
 * Driver information interface
 */
export interface DriverInfo {
  id: string
  name: string
  rating: number
  car: string
}

/**
 * Ride response interface for ride booking results
 */
export interface RideResponse {
  ride_id: string
  status: string
  driver_info?: DriverInfo
  estimated_pickup: string
  estimated_arrival: string
  fare_estimate: number
} 