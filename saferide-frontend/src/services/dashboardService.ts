/**
 * Service for fetching dashboard metrics and statistics
 * Follows SOLID principles and provides comprehensive dashboard data management
 */

export interface DashboardMetrics {
  total_users: number;
  active_users: number;
  total_drivers: number;
  active_drivers: number;
  total_companies: number;
  active_companies: number;
  total_children: number;
  active_rides: number;
  timestamp: string;
}

class DashboardService {
  private baseUrl: string = 'http://localhost:8000';

  /**
   * Get dashboard metrics from the backend
   * Returns comprehensive statistics for the admin dashboard
   */
  async getDashboardMetrics(): Promise<DashboardMetrics> {
    try {
      const response = await fetch(`${this.baseUrl}/api/admin/dashboard/metrics`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch dashboard metrics: ${response.statusText}`);
      }

      const data = await response.json();
      return data as DashboardMetrics;
    } catch (error) {
      console.error('Error fetching dashboard metrics:', error);
      // Return default values if API fails
      return {
        total_users: 0,
        active_users: 0,
        total_drivers: 0,
        active_drivers: 0,
        total_companies: 0,
        active_companies: 0,
        total_children: 0,
        active_rides: 0,
        timestamp: new Date().toISOString(),
      };
    }
  }

  /**
   * Get formatted dashboard metrics with proper error handling
   * Returns metrics with fallback values if API is unavailable
   */
  async getFormattedMetrics(): Promise<DashboardMetrics> {
    try {
      const metrics = await this.getDashboardMetrics();
      return {
        ...metrics,
        // Ensure all values are numbers and have fallbacks
        total_users: Number(metrics.total_users) || 0,
        active_users: Number(metrics.active_users) || 0,
        total_drivers: Number(metrics.total_drivers) || 0,
        active_drivers: Number(metrics.active_drivers) || 0,
        total_companies: Number(metrics.total_companies) || 0,
        active_companies: Number(metrics.active_companies) || 0,
        total_children: Number(metrics.total_children) || 0,
        active_rides: Number(metrics.active_rides) || 0,
        timestamp: metrics.timestamp || new Date().toISOString(),
      };
    } catch (error) {
      console.error('Error getting formatted metrics:', error);
      // Return safe default values
      return {
        total_users: 0,
        active_users: 0,
        total_drivers: 0,
        active_drivers: 0,
        total_companies: 0,
        active_companies: 0,
        total_children: 0,
        active_rides: 0,
        timestamp: new Date().toISOString(),
      };
    }
  }
}

// Export singleton instance
export const dashboardService = new DashboardService(); 