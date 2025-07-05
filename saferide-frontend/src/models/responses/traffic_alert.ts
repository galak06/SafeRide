import { Location } from '../types/location'

/**
 * Traffic alert interface for traffic information
 */
export interface TrafficAlert {
  id: string
  type: string
  severity: string
  location: Location
  description: string
  created_at: string
} 