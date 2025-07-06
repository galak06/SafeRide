import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LanguageProvider } from '../../contexts/LanguageContext';
import AdminPortal from '../../components/AdminPortal';

// Mock the dashboard service
jest.mock('../../services/dashboardService', () => ({
  dashboardService: {
    getFormattedMetrics: jest.fn().mockResolvedValue({
      total_users: 150,
      active_users: 120,
      total_drivers: 45,
      active_drivers: 38,
      total_companies: 12,
      active_companies: 10,
      total_children: 89,
      active_rides: 5,
      timestamp: '2024-01-01T12:00:00Z'
    })
  }
}));

// Mock the child components to avoid complex dependencies
jest.mock('../../components/ChildrenManager', () => {
  return function MockChildrenManager() {
    return <div data-testid="children-manager">Children Management Component</div>;
  };
});

jest.mock('../../components/CompanyManager', () => {
  return function MockCompanyManager() {
    return <div data-testid="company-manager">Company Management Component</div>;
  };
});

// Wrapper component to provide language context
const renderWithLanguage = (component: React.ReactElement) => {
  return render(
    <LanguageProvider>
      {component}
    </LanguageProvider>
  );
};

describe('AdminPortal Component', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
  });

  describe('Initial Render', () => {
    test('renders admin portal with correct structure', async () => {
      renderWithLanguage(<AdminPortal />);
      
      expect(screen.getByText('Admin Portal')).toBeInTheDocument();
      expect(screen.getByText('Manage drivers, companies, relationships, and children in the SafeRide system')).toBeInTheDocument();
    });

    test('displays all available tabs', async () => {
      renderWithLanguage(<AdminPortal />);
      
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Company Management')).toBeInTheDocument();
      expect(screen.getByText('Children Management')).toBeInTheDocument();
    });

    test('shows dashboard as default active tab', async () => {
      renderWithLanguage(<AdminPortal />);
      
      // Wait for dashboard to load
      await screen.findByText('System Dashboard');
      await screen.findByText('Total Drivers');
      await screen.findByText('Total Companies');
    });
  });

  describe('Dashboard Tab', () => {
    test('displays all dashboard metrics', async () => {
      renderWithLanguage(<AdminPortal />);
      
      // Wait for dashboard to load and display metrics
      await screen.findByText('Total Drivers');
      await screen.findByText('Total Companies');
      await screen.findByText('Total Children');
      await screen.findByText('Active Rides');
      
      // Check for metric descriptions using partial text matching
      expect(screen.getByText(/Active drivers in the system/)).toBeInTheDocument();
      expect(screen.getByText(/Registered companies/)).toBeInTheDocument();
      expect(screen.getByText(/Children in the system/)).toBeInTheDocument();
      expect(screen.getByText(/Rides in progress/)).toBeInTheDocument();
    });

    test('displays recent activity section', async () => {
      renderWithLanguage(<AdminPortal />);
      
      // Wait for dashboard to load
      await screen.findByText('System Dashboard');
      
      expect(screen.getByText('Recent Activity')).toBeInTheDocument();
      expect(screen.getByText('System initialized')).toBeInTheDocument();
      expect(screen.getByText('Admin portal accessed')).toBeInTheDocument();
    });
  });

  describe('Navigation', () => {
    test('switches between tabs correctly', async () => {
      renderWithLanguage(<AdminPortal />);
      
      // Wait for dashboard to load
      await screen.findByText('System Dashboard');
      
      // Click Company Management tab
      fireEvent.click(screen.getByText('Company Management'));
      expect(screen.getByTestId('company-manager')).toBeInTheDocument();
      expect(screen.queryByText('System Dashboard')).not.toBeInTheDocument();
    });
  });

  describe('Company Management Tab', () => {
    beforeEach(async () => {
      renderWithLanguage(<AdminPortal />);
      // Wait for initial load
      await screen.findByText('System Dashboard');
      fireEvent.click(screen.getByText('Company Management'));
    });

    test('displays company management component', () => {
      expect(screen.getByTestId('company-manager')).toBeInTheDocument();
      expect(screen.getByText('Company Management Component')).toBeInTheDocument();
    });
  });

  describe('Children Management Tab', () => {
    beforeEach(async () => {
      renderWithLanguage(<AdminPortal />);
      // Wait for initial load
      await screen.findByText('System Dashboard');
      fireEvent.click(screen.getByText('Children Management'));
    });

    test('displays children management component', () => {
      expect(screen.getByTestId('children-manager')).toBeInTheDocument();
      expect(screen.getByText('Children Management Component')).toBeInTheDocument();
    });
  });

  describe('Button Interactions', () => {
    test('handles tab button clicks', async () => {
      renderWithLanguage(<AdminPortal />);
      
      // Wait for dashboard to load
      await screen.findByText('System Dashboard');
      
      // Click different tabs
      fireEvent.click(screen.getByText('Company Management'));
      expect(screen.getByTestId('company-manager')).toBeInTheDocument();
      
      fireEvent.click(screen.getByText('Children Management'));
      expect(screen.getByTestId('children-manager')).toBeInTheDocument();
      
      fireEvent.click(screen.getByText('Dashboard'));
      await screen.findByText('System Dashboard');
    });
  });

  describe('Data Loading', () => {
    test('shows dashboard with loaded values', async () => {
      renderWithLanguage(<AdminPortal />);
      
      // Wait for dashboard to load and check for actual values
      await screen.findByText('45'); // Total Drivers
      await screen.findByText('12'); // Total Companies
      await screen.findByText('89'); // Total Children
      await screen.findByText('5');  // Active Rides
    });
  });

  describe('Accessibility', () => {
    test('has proper heading structure', async () => {
      renderWithLanguage(<AdminPortal />);
      
      await screen.findByText('System Dashboard');
      
      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Admin Portal');
      expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('System Dashboard');
    });

    test('has proper button roles', async () => {
      renderWithLanguage(<AdminPortal />);
      
      await screen.findByText('System Dashboard');
      
      const tabButtons = screen.getAllByRole('button');
      expect(tabButtons.length).toBeGreaterThan(0);
      
      tabButtons.forEach(button => {
        expect(button).toHaveClass('tab-button');
      });
    });
  });

  describe('Responsive Design', () => {
    test('renders all content in admin layout structure', async () => {
      renderWithLanguage(<AdminPortal />);
      
      await screen.findByText('System Dashboard');
      
      const adminPortal = screen.getByText('Admin Portal').closest('.admin-portal');
      expect(adminPortal).toBeInTheDocument();
      
      const header = screen.getByText('Admin Portal').closest('.admin-header');
      expect(header).toBeInTheDocument();
      
      const tabs = screen.getByText('Dashboard').closest('.admin-tabs');
      expect(tabs).toBeInTheDocument();
      
      const content = screen.getByText('System Dashboard').closest('.admin-content');
      expect(content).toBeInTheDocument();
    });

    test('maintains layout structure across tab switches', async () => {
      renderWithLanguage(<AdminPortal />);
      
      // Wait for dashboard to load
      await screen.findByText('System Dashboard');
      
      // Check initial layout
      expect(screen.getByText('Dashboard').closest('.admin-tabs')).toBeInTheDocument();
      expect(screen.getByText('System Dashboard').closest('.admin-content')).toBeInTheDocument();
      
      // Switch tabs and check layout is maintained
      fireEvent.click(screen.getByText('Company Management'));
      expect(screen.getByText('Company Management').closest('.admin-tabs')).toBeInTheDocument();
      expect(screen.getByTestId('company-manager').closest('.admin-content')).toBeInTheDocument();
    });
  });

  describe('Error Handling', () => {
    test('handles missing data gracefully', async () => {
      // Mock console.error to avoid noise in tests
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
      
      renderWithLanguage(<AdminPortal />);
      
      // Component should render without errors even with missing data
      expect(screen.getByText('Admin Portal')).toBeInTheDocument();
      await screen.findByText('System Dashboard');
      
      consoleSpy.mockRestore();
    });
  });

  describe('localStorage Persistence', () => {
    test('remembers active tab after page refresh', async () => {
      // Set a specific tab in localStorage
      localStorage.setItem('adminActiveTab', 'companies');
      
      renderWithLanguage(<AdminPortal />);
      
      // Should show Company Management tab as active
      expect(screen.getByTestId('company-manager')).toBeInTheDocument();
      expect(screen.queryByText('System Dashboard')).not.toBeInTheDocument();
    });

    test('defaults to dashboard when no tab is saved', async () => {
      // Ensure no tab is saved
      localStorage.removeItem('adminActiveTab');
      
      renderWithLanguage(<AdminPortal />);
      
      // Should show Dashboard as default
      await screen.findByText('System Dashboard');
    });
  });
}); 