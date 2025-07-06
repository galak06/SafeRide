import { render, screen, fireEvent } from '../utils/test-utils';
import '@testing-library/jest-dom';
import AdminPortal from '../../components/AdminPortal';

describe('AdminPortal Component', () => {
  beforeEach(() => {
    // Mock console methods to avoid noise in tests
    jest.spyOn(console, 'log').mockImplementation(() => {});
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('Initial Rendering', () => {
    test('renders admin portal with header', () => {
      render(<AdminPortal />);
      
      expect(screen.getByText('Admin Portal')).toBeInTheDocument();
      expect(screen.getByText(/Manage drivers, companies, relationships, and children in the SafeRide system/)).toBeInTheDocument();
    });

    test('renders navigation tabs with all sections', () => {
      render(<AdminPortal />);
      
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Driver & Company')).toBeInTheDocument();
      expect(screen.getByText('Companies')).toBeInTheDocument();
      expect(screen.getByText('Relationships')).toBeInTheDocument();
      expect(screen.getByText('Children Management')).toBeInTheDocument();
    });

    test('shows dashboard as default active tab', () => {
      render(<AdminPortal />);
      
      expect(screen.getByText('System Dashboard')).toBeInTheDocument();
      expect(screen.getByText('Total Drivers')).toBeInTheDocument();
      expect(screen.getByText('Total Companies')).toBeInTheDocument();
    });
  });

  describe('Dashboard Tab', () => {
    test('displays all dashboard metrics', () => {
      render(<AdminPortal />);
      
      expect(screen.getByText('Total Drivers')).toBeInTheDocument();
      expect(screen.getAllByText('0').length).toBeGreaterThan(0);
      expect(screen.getByText('Total Companies')).toBeInTheDocument();
      expect(screen.getByText('Total Children')).toBeInTheDocument();
      expect(screen.getByText('Active Rides')).toBeInTheDocument();
      expect(screen.getByText('Active drivers in the system')).toBeInTheDocument();
      expect(screen.getByText('Registered companies')).toBeInTheDocument();
      expect(screen.getByText('Children in the system')).toBeInTheDocument();
      expect(screen.getByText('Rides in progress')).toBeInTheDocument();
    });

    test('displays recent activity section', () => {
      render(<AdminPortal />);
      
      expect(screen.getByText('Recent Activity')).toBeInTheDocument();
      expect(screen.getByText('System initialized')).toBeInTheDocument();
      expect(screen.getByText('Admin portal accessed')).toBeInTheDocument();
    });
  });

  describe('Navigation', () => {
    test('switches between tabs correctly', () => {
      render(<AdminPortal />);
      
      // Dashboard should be visible by default
      expect(screen.getByText('System Dashboard')).toBeInTheDocument();
      
      // Click Driver & Company tab
      fireEvent.click(screen.getByText('Driver & Company'));
      expect(screen.getByText('Driver & Company Management')).toBeInTheDocument();
      expect(screen.queryByText('System Dashboard')).not.toBeInTheDocument();
    });
  });

  describe('Driver & Company Tab', () => {
    beforeEach(() => {
      render(<AdminPortal />);
      fireEvent.click(screen.getByText('Driver & Company'));
    });

    test('displays driver management content', () => {
      expect(screen.getByText('Driver & Company Management')).toBeInTheDocument();
      expect(screen.getByText(/This feature is currently being developed/)).toBeInTheDocument();
      expect(screen.getByText('You will be able to:')).toBeInTheDocument();
    });

    test('displays feature list', () => {
      expect(screen.getByText('Add and manage drivers')).toBeInTheDocument();
      expect(screen.getByText('Create and manage companies')).toBeInTheDocument();
      expect(screen.getByText('Assign drivers to companies')).toBeInTheDocument();
      expect(screen.getByText('View driver statistics and performance')).toBeInTheDocument();
      expect(screen.getByText('Manage company settings and policies')).toBeInTheDocument();
    });
  });

  describe('Companies Tab', () => {
    beforeEach(() => {
      render(<AdminPortal />);
      fireEvent.click(screen.getByText('Companies'));
    });

    test('displays company management component', () => {
      // CompanyManager component should be rendered (may show loading initially)
      expect(screen.getByText('Initializing Company Management...')).toBeInTheDocument();
    });
  });

  describe('Relationships Tab', () => {
    beforeEach(() => {
      render(<AdminPortal />);
      fireEvent.click(screen.getByText('Relationships'));
    });

    test('displays relationship management component', () => {
      // RelationshipManager component should be rendered (may show loading initially)
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });
  });

  describe('Children Management Tab', () => {
    beforeEach(() => {
      render(<AdminPortal />);
      fireEvent.click(screen.getByText('Children Management'));
    });

    test('displays children management component', () => {
      // ChildrenManager component should be rendered
      expect(screen.getByText('Children Management')).toBeInTheDocument();
    });
  });

  describe('Button Interactions', () => {
    test('handles tab button clicks', () => {
      render(<AdminPortal />);
      
      // Click different tabs
      fireEvent.click(screen.getByText('Driver & Company'));
      expect(screen.getByText('Driver & Company Management')).toBeInTheDocument();
      
      fireEvent.click(screen.getByText('Companies'));
      expect(screen.getByText('Initializing Company Management...')).toBeInTheDocument();
      
      fireEvent.click(screen.getByText('Dashboard'));
      expect(screen.getByText('System Dashboard')).toBeInTheDocument();
    });
  });

  describe('Data Loading', () => {
    test('shows dashboard with default values', () => {
      render(<AdminPortal />);
      
      // Check that dashboard shows with default "0" values
      const statNumbers = screen.getAllByText('0');
      expect(statNumbers.length).toBe(4); // Should have 4 stat cards with "0"
    });
  });

  describe('Accessibility', () => {
    test('has proper heading structure', () => {
      render(<AdminPortal />);
      
      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Admin Portal');
      expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('System Dashboard');
    });

    test('has proper button roles', () => {
      render(<AdminPortal />);
      
      const tabButtons = screen.getAllByRole('button');
      expect(tabButtons.length).toBeGreaterThan(0);
      
      tabButtons.forEach(button => {
        expect(button).toHaveClass('tab-button');
      });
    });
  });

  describe('Responsive Design', () => {
    test('renders all content in admin layout structure', () => {
      render(<AdminPortal />);
      
      const adminPortal = screen.getByText('Admin Portal').closest('.admin-portal');
      expect(adminPortal).toBeInTheDocument();
      
      const header = screen.getByText('Admin Portal').closest('.admin-header');
      expect(header).toBeInTheDocument();
      
      const tabs = screen.getByText('Dashboard').closest('.admin-tabs');
      expect(tabs).toBeInTheDocument();
      
      const content = screen.getByText('System Dashboard').closest('.admin-content');
      expect(content).toBeInTheDocument();
    });

    test('maintains layout structure across tab switches', () => {
      render(<AdminPortal />);
      
      // Check initial layout
      expect(screen.getByText('Dashboard').closest('.admin-tabs')).toBeInTheDocument();
      expect(screen.getByText('System Dashboard').closest('.admin-content')).toBeInTheDocument();
      
      // Switch tabs and check layout is maintained
      fireEvent.click(screen.getByText('Driver & Company'));
      expect(screen.getByText('Driver & Company').closest('.admin-tabs')).toBeInTheDocument();
      expect(screen.getByText('Driver & Company Management').closest('.admin-content')).toBeInTheDocument();
    });
  });

  describe('Error Handling', () => {
    test('handles missing data gracefully', () => {
      // Mock console.error to avoid noise in tests
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
      
      render(<AdminPortal />);
      
      // Component should render without errors even with missing data
      expect(screen.getByText('Admin Portal')).toBeInTheDocument();
      expect(screen.getByText('System Dashboard')).toBeInTheDocument();
      
      consoleSpy.mockRestore();
    });
  });
}); 