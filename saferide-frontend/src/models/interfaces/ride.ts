/**
 * Ride interface for ride history
 */
export interface Ride {
  id: string
  destination: string
  status: 'pending' | 'active' | 'completed' | 'cancelled'
  createdAt: string
} 