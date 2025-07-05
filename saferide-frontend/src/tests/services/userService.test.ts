import { userService } from '../../services/userService';
import type { User, LoginCredentials, UserPreferences } from '../../models';

// Mock fetch for testing
global.fetch = jest.fn();

describe('UserService', () => {
  const mockUser: User = {
    id: '1',
    email: 'test@example.com',
    password: 'password123',
    name: 'Test User',
    phone: '1234567890',
    profilePicture: null,
    createdAt: '2023-01-01T00:00:00Z',
    updatedAt: '2023-01-01T00:00:00Z',
    rideHistory: [],
    preferences: {
      defaultPaymentMethod: 'card',
      notifications: true,
      language: 'en'
    }
  };

  const mockUser2: User = {
    id: '2',
    email: 'john@example.com',
    password: 'password456',
    name: 'John Doe',
    phone: '0987654321',
    profilePicture: 'https://example.com/avatar.jpg',
    createdAt: '2023-01-02T00:00:00Z',
    updatedAt: '2023-01-02T00:00:00Z',
    rideHistory: [
      {
        id: 'ride-1',
        destination: 'Times Square',
        status: 'completed',
        createdAt: '2023-01-01T10:00:00Z'
      }
    ],
    preferences: {
      defaultPaymentMethod: 'paypal',
      notifications: false,
      language: 'es'
    }
  };

  const mockUsersData = {
    users: [mockUser, mockUser2]
  };

  beforeEach(() => {
    jest.clearAllMocks();
    // Reset the users array to avoid state pollution between tests
    (userService as any).users = [];
    // Reset user objects to their original state
    mockUser.rideHistory = [];
    mockUser2.rideHistory = [
      {
        id: 'ride-1',
        destination: 'Times Square',
        status: 'completed',
        createdAt: '2023-01-01T10:00:00Z'
      }
    ];
    (fetch as jest.Mock).mockResolvedValue({
      json: jest.fn().mockResolvedValue(mockUsersData)
    });
  });

  describe('loadUsers', () => {
    test('loads users successfully', async () => {
      await userService['loadUsers']();
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/users', {
        headers: { 'Content-Type': 'application/json' }
      });
    });

    test('handles load error gracefully', async () => {
      (fetch as jest.Mock).mockRejectedValue(new Error('Network error'));
      
      await userService['loadUsers']();
      
      // Should not throw error and should log the error
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/users', {
        headers: { 'Content-Type': 'application/json' }
      });
    });

    test('handles malformed JSON response', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockRejectedValue(new Error('Invalid JSON'))
      });
      
      await userService['loadUsers']();
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/users', {
        headers: { 'Content-Type': 'application/json' }
      });
    });

    test('handles empty users array', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue([])
      });
      
      await userService['loadUsers']();
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/users', {
        headers: { 'Content-Type': 'application/json' }
      });
    });
  });

  describe('authenticateUser', () => {
    test('authenticates user with valid credentials', async () => {
      const mockResponse = {
        success: true,
        message: 'Login successful',
        user: { ...mockUser, token: 'mock-token-123' }
      };
      
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockResponse.user)
      });
      
      const credentials: LoginCredentials = {
        email: 'test@example.com',
        password: 'password123'
      };

      const result = await userService.authenticateUser(credentials);

      expect(result.success).toBe(true);
      expect(result.message).toBe('Login successful');
      expect(result.user).toBeDefined();
    });

    test('fails authentication with invalid credentials', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'Invalid credentials' })
      });
      
      const credentials: LoginCredentials = {
        email: 'wrong@example.com',
        password: 'wrongpassword'
      };

      const result = await userService.authenticateUser(credentials);

      expect(result.success).toBe(false);
      expect(result.message).toBe('Invalid credentials');
      expect(result.user).toBeUndefined();
    });

    test('handles case-insensitive email matching', async () => {
      const mockResponse = {
        success: true,
        message: 'Login successful',
        user: { ...mockUser, token: 'mock-token-123' }
      };
      
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockResponse.user)
      });
      
      const credentials: LoginCredentials = {
        email: 'TEST@EXAMPLE.COM',
        password: 'password123'
      };

      const result = await userService.authenticateUser(credentials);

      expect(result.success).toBe(true);
      expect(result.message).toBe('Login successful');
    });

    test('fails with empty email', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'Invalid email or password' })
      });
      
      const credentials: LoginCredentials = {
        email: '',
        password: 'password123'
      };

      const result = await userService.authenticateUser(credentials);

      expect(result.success).toBe(false);
      expect(result.message).toBe('Invalid email or password');
    });

    test('fails with empty password', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'Invalid email or password' })
      });
      
      const credentials: LoginCredentials = {
        email: 'test@example.com',
        password: ''
      };

      const result = await userService.authenticateUser(credentials);

      expect(result.success).toBe(false);
      expect(result.message).toBe('Invalid email or password');
    });

    test('fails with whitespace-only credentials', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'Invalid email or password' })
      });
      
      const credentials: LoginCredentials = {
        email: '   ',
        password: '   '
      };

      const result = await userService.authenticateUser(credentials);

      expect(result.success).toBe(false);
      expect(result.message).toBe('Invalid email or password');
    });

    test('handles special characters in email', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'Invalid email or password' })
      });
      
      const credentials: LoginCredentials = {
        email: 'test+tag@example.com',
        password: 'password123'
      };

      const result = await userService.authenticateUser(credentials);

      expect(result.success).toBe(false);
      expect(result.message).toBe('Invalid email or password');
    });
  });

  describe('getUserById', () => {
    test('returns user when found', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockUser)
      });
      
      const user = await userService.getUserById('1');
      
      expect(user).toEqual(mockUser);
    });

    test('returns null when user not found', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'User not found' })
      });
      
      const user = await userService.getUserById('999');
      
      expect(user).toBeNull();
    });

    test('returns null with empty string id', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'User not found' })
      });
      
      const user = await userService.getUserById('');
      
      expect(user).toBeNull();
    });

    test('returns null with null id', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'User not found' })
      });
      
      const user = await userService.getUserById(null as any);
      
      expect(user).toBeNull();
    });
  });

  describe('getUserByEmail', () => {
    test('returns user when found', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockUser)
      });
      
      const user = await userService.getUserByEmail('test@example.com');
      
      expect(user).toEqual(mockUser);
    });

    test('returns null when user not found', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'User not found' })
      });
      
      const user = await userService.getUserByEmail('nonexistent@example.com');
      
      expect(user).toBeNull();
    });

    test('handles case-insensitive email matching', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockUser)
      });
      
      const user = await userService.getUserByEmail('TEST@EXAMPLE.COM');
      
      expect(user).toEqual(mockUser);
    });

    test('returns null with empty email', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'User not found' })
      });
      
      const user = await userService.getUserByEmail('');
      
      expect(user).toBeNull();
    });
  });

  describe('addRideToHistory', () => {
    test('adds ride to user history successfully', async () => {
      const mockRideResponse = {
        ride_id: 'ride-123',
        status: 'pending'
      };
      
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockRideResponse)
      });
      
      const destination = 'Times Square';
      const ride = await userService.addRideToHistory('1', destination);
      
      expect(ride).toBeDefined();
      expect(ride?.destination).toBe(destination);
      expect(ride?.status).toBe('pending');
      expect(ride?.id).toBe('ride-123');
    });

    test('returns null when user not found', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'User not found' })
      });
      
      const ride = await userService.addRideToHistory('999', 'Times Square');
      
      expect(ride).toBeNull();
    });

    test('handles empty destination', async () => {
      const mockRideResponse = {
        ride_id: 'ride-123',
        status: 'pending'
      };
      
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockRideResponse)
      });
      
      const ride = await userService.addRideToHistory('1', '');
      
      expect(ride?.destination).toBe('');
    });

    test('handles special characters in destination', async () => {
      const mockRideResponse = {
        ride_id: 'ride-123',
        status: 'pending'
      };
      
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockRideResponse)
      });
      
      const destination = 'Times Square & Broadway';
      const ride = await userService.addRideToHistory('1', destination);
      
      expect(ride?.destination).toBe(destination);
    });
  });

  describe('getUserRideHistory', () => {
    test('returns user ride history', async () => {
      const mockRides = [
        {
          id: 'ride-1',
          destination: 'Times Square',
          status: 'completed',
          createdAt: '2023-01-01T00:00:00Z'
        }
      ];
      
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockRides)
      });
      
      const history = await userService.getUserRideHistory('2');
      
      expect(Array.isArray(history)).toBe(true);
      expect(history).toHaveLength(1);
      expect(history[0].destination).toBe('Times Square');
    });

    test('returns empty array when user not found', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'User not found' })
      });
      
      const history = await userService.getUserRideHistory('999');
      
      expect(history).toEqual([]);
    });

    test('returns empty array for user with no rides', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue([])
      });
      
      const history = await userService.getUserRideHistory('1');
      
      expect(history).toEqual([]);
    });
  });

  describe('updateUserPreferences', () => {
    test('updates user preferences successfully', async () => {
      const updatedUser = { ...mockUser, preferences: { ...mockUser.preferences, notifications: false, language: 'es' } };
      
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(updatedUser)
      });
      
      const newPreferences: Partial<UserPreferences> = {
        notifications: false,
        language: 'es'
      };

      const result = await userService.updateUserPreferences('1', newPreferences);
      
      expect(result).toBe(true);
    });

    test('returns false when user not found', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: false,
        json: jest.fn().mockResolvedValue({ detail: 'User not found' })
      });
      
      const newPreferences: Partial<UserPreferences> = {
        notifications: false
      };

      const result = await userService.updateUserPreferences('999', newPreferences);
      
      expect(result).toBe(false);
    });

    test('updates partial preferences', async () => {
      const updatedUser = { ...mockUser, preferences: { ...mockUser.preferences, notifications: false } };
      
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(updatedUser)
      });
      
      const newPreferences: Partial<UserPreferences> = {
        notifications: false
      };

      const result = await userService.updateUserPreferences('1', newPreferences);
      
      expect(result).toBe(true);
    });

    test('updates all preference fields', async () => {
      const newPreferences: UserPreferences = {
        defaultPaymentMethod: 'paypal',
        notifications: false,
        language: 'fr'
      };
      
      const updatedUser = { ...mockUser, preferences: newPreferences };
      
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(updatedUser)
      });

      const result = await userService.updateUserPreferences('1', newPreferences);
      
      expect(result).toBe(true);
    });

    test('handles empty preferences object', async () => {
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(mockUser)
      });
      
      const result = await userService.updateUserPreferences('1', {});
      
      expect(result).toBe(true);
    });
  });

  describe('getAllUsers', () => {
    test('returns all users without passwords', async () => {
      const usersWithoutPasswords = [
        { ...mockUser, password: undefined },
        { ...mockUser2, password: undefined }
      ];
      
      (fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: jest.fn().mockResolvedValue(usersWithoutPasswords)
      });
      
      const users = await userService.getAllUsers();
      
      expect(users).toHaveLength(2);
      // Password should be removed from user objects
      expect(users[0]).not.toHaveProperty('password');
      expect(users[1]).not.toHaveProperty('password');
    });

    test('returns empty array when no users loaded', async () => {
      const users = await userService.getAllUsers();
      
      expect(users).toEqual([]);
    });

    test('handles API error gracefully', async () => {
      (fetch as jest.Mock).mockRejectedValue(new Error('Network error'));
      
      const users = await userService.getAllUsers();
      
      expect(users).toEqual([]);
    });
  });
}); 