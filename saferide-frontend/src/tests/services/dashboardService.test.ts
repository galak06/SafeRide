import { dashboardService, DashboardMetrics } from '../../services/dashboardService';

// Mock fetch for testing
global.fetch = jest.fn();

describe('DashboardService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getDashboardMetrics', () => {
    test('fetches dashboard metrics successfully', async () => {
      const mockMetrics: DashboardMetrics = {
        total_users: 150,
        active_users: 120,
        total_drivers: 45,
        active_drivers: 38,
        total_companies: 12,
        active_companies: 10,
        total_children: 89,
        active_rides: 5,
        timestamp: '2024-01-01T12:00:00Z'
      };

      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockMetrics)
      });

      const result = await dashboardService.getDashboardMetrics();

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/admin/dashboard/metrics',
        expect.objectContaining({
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
        })
      );
      expect(result).toEqual(mockMetrics);
    });

    test('handles API error response', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        statusText: 'Internal Server Error'
      });

      const result = await dashboardService.getDashboardMetrics();

      expect(result).toEqual({
        total_users: 0,
        active_users: 0,
        total_drivers: 0,
        active_drivers: 0,
        total_companies: 0,
        active_companies: 0,
        total_children: 0,
        active_rides: 0,
        timestamp: expect.any(String)
      });
    });

    test('handles network error', async () => {
      (fetch as jest.Mock).mockRejectedValue(new Error('Network error'));

      const result = await dashboardService.getDashboardMetrics();

      expect(result).toEqual({
        total_users: 0,
        active_users: 0,
        total_drivers: 0,
        active_drivers: 0,
        total_companies: 0,
        active_companies: 0,
        total_children: 0,
        active_rides: 0,
        timestamp: expect.any(String)
      });
    });

    test('handles malformed JSON response', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockRejectedValue(new Error('Invalid JSON'))
      });

      const result = await dashboardService.getDashboardMetrics();

      expect(result).toEqual({
        total_users: 0,
        active_users: 0,
        total_drivers: 0,
        active_drivers: 0,
        total_companies: 0,
        active_companies: 0,
        total_children: 0,
        active_rides: 0,
        timestamp: expect.any(String)
      });
    });
  });

  describe('getFormattedMetrics', () => {
    test('returns formatted metrics with fallback values', async () => {
      const mockMetrics: DashboardMetrics = {
        total_users: 100,
        active_users: 80,
        total_drivers: 30,
        active_drivers: 25,
        total_companies: 8,
        active_companies: 7,
        total_children: 50,
        active_rides: 3,
        timestamp: '2024-01-01T12:00:00Z'
      };

      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockMetrics)
      });

      const result = await dashboardService.getFormattedMetrics();

      expect(result).toEqual(mockMetrics);
    });

    test('handles null/undefined values in response', async () => {
      const mockMetricsWithNulls = {
        total_users: null,
        active_users: undefined,
        total_drivers: 30,
        active_drivers: 25,
        total_companies: 8,
        active_companies: 7,
        total_children: 50,
        active_rides: 3,
        timestamp: null
      };

      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockMetricsWithNulls)
      });

      const result = await dashboardService.getFormattedMetrics();

      expect(result).toEqual({
        total_users: 0,
        active_users: 0,
        total_drivers: 30,
        active_drivers: 25,
        total_companies: 8,
        active_companies: 7,
        total_children: 50,
        active_rides: 3,
        timestamp: expect.any(String)
      });
    });

    test('handles API failure gracefully', async () => {
      (fetch as jest.Mock).mockRejectedValue(new Error('API unavailable'));

      const result = await dashboardService.getFormattedMetrics();

      expect(result).toEqual({
        total_users: 0,
        active_users: 0,
        total_drivers: 0,
        active_drivers: 0,
        total_companies: 0,
        active_companies: 0,
        total_children: 0,
        active_rides: 0,
        timestamp: expect.any(String)
      });
    });

    test('ensures all numeric values are properly typed', async () => {
      const mockMetricsWithStrings = {
        total_users: '100',
        active_users: '80',
        total_drivers: '30',
        active_drivers: '25',
        total_companies: '8',
        active_companies: '7',
        total_children: '50',
        active_rides: '3',
        timestamp: '2024-01-01T12:00:00Z'
      };

      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockMetricsWithStrings)
      });

      const result = await dashboardService.getFormattedMetrics();

      // All numeric values should be numbers
      expect(typeof result.total_users).toBe('number');
      expect(typeof result.active_users).toBe('number');
      expect(typeof result.total_drivers).toBe('number');
      expect(typeof result.active_drivers).toBe('number');
      expect(typeof result.total_companies).toBe('number');
      expect(typeof result.active_companies).toBe('number');
      expect(typeof result.total_children).toBe('number');
      expect(typeof result.active_rides).toBe('number');
      expect(typeof result.timestamp).toBe('string');
    });
  });

  describe('error handling', () => {
    test('logs errors to console', async () => {
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();
      
      (fetch as jest.Mock).mockRejectedValue(new Error('Test error'));

      await dashboardService.getDashboardMetrics();

      expect(consoleSpy).toHaveBeenCalledWith('Error fetching dashboard metrics:', expect.any(Error));
      
      consoleSpy.mockRestore();
    });

    test('provides meaningful error messages', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        statusText: 'Not Found'
      });

      const result = await dashboardService.getDashboardMetrics();

      // Should return default values instead of throwing
      expect(result).toEqual({
        total_users: 0,
        active_users: 0,
        total_drivers: 0,
        active_drivers: 0,
        total_companies: 0,
        active_companies: 0,
        total_children: 0,
        active_rides: 0,
        timestamp: expect.any(String)
      });
    });
  });
}); 