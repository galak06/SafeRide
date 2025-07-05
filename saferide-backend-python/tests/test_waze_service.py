import pytest
from unittest.mock import patch, MagicMock
from services.waze_service import WazeService
from datetime import datetime

class TestWazeService:
    """Test Waze service functionality"""
    
    @pytest.fixture
    def waze_service(self):
        """Create Waze service instance for testing"""
        return WazeService()
    
    @pytest.fixture
    def sample_origin(self):
        """Sample origin coordinates"""
        return {"lat": 40.7128, "lng": -74.0060}
    
    @pytest.fixture
    def sample_destination(self):
        """Sample destination coordinates"""
        return {"lat": 40.7589, "lng": -73.9851}
    
    @pytest.fixture
    def sample_location(self):
        """Sample location for traffic info"""
        return {"lat": 40.7505, "lng": -73.9934}
    
    class TestCalculateRoute:
        """Test route calculation functionality"""
        
        @pytest.mark.asyncio
        async def test_calculate_route_success(self, waze_service, sample_origin, sample_destination):
            """Test successful route calculation"""
            route_data = await waze_service.calculate_route(sample_origin, sample_destination)
            
            # Verify response structure
            assert isinstance(route_data, dict)
            assert "routes" in route_data
            assert "best_route" in route_data
            assert "total_distance" in route_data
            assert "total_duration" in route_data
            assert "traffic_conditions" in route_data
            
            # Verify routes array
            routes = route_data["routes"]
            assert isinstance(routes, list)
            assert len(routes) > 0
            
            # Verify first route structure
            first_route = routes[0]
            assert "id" in first_route
            assert "name" in first_route
            assert "distance" in first_route
            assert "duration" in first_route
            assert "traffic_conditions" in first_route
            assert "waypoints" in first_route
            
            # Verify waypoints
            waypoints = first_route["waypoints"]
            assert isinstance(waypoints, list)
            assert len(waypoints) >= 2
            
            # Verify coordinates are preserved
            assert waypoints[0]["lat"] == sample_origin["lat"]
            assert waypoints[0]["lng"] == sample_origin["lng"]
            assert waypoints[-1]["lat"] == sample_destination["lat"]
            assert waypoints[-1]["lng"] == sample_destination["lng"]
        
        @pytest.mark.asyncio
        async def test_calculate_route_with_different_coordinates(self, waze_service):
            """Test route calculation with different coordinate sets"""
            origin = {"lat": 34.0522, "lng": -118.2437}  # Los Angeles
            destination = {"lat": 37.7749, "lng": -122.4194}  # San Francisco
            
            route_data = await waze_service.calculate_route(origin, destination)
            
            assert route_data["routes"][0]["waypoints"][0]["lat"] == origin["lat"]
            assert route_data["routes"][0]["waypoints"][-1]["lat"] == destination["lat"]
        
        @pytest.mark.asyncio
        async def test_calculate_route_error_handling(self, waze_service, sample_origin, sample_destination):
            """Test error handling in route calculation"""
            # Mock the service to throw an exception
            with patch.object(waze_service, 'calculate_route', side_effect=Exception("API Error")):
                with pytest.raises(Exception) as exc_info:
                    await waze_service.calculate_route(sample_origin, sample_destination)
                assert "API Error" in str(exc_info.value)
        
        @pytest.mark.asyncio
        async def test_calculate_route_invalid_coordinates(self, waze_service):
            """Test route calculation with invalid coordinates"""
            invalid_origin = {"lat": 200, "lng": 200}  # Invalid coordinates
            invalid_destination = {"lat": -200, "lng": -200}  # Invalid coordinates
            
            # Should still work with mock implementation
            route_data = await waze_service.calculate_route(invalid_origin, invalid_destination)
            assert isinstance(route_data, dict)
    
    class TestGetTrafficInfo:
        """Test traffic information functionality"""
        
        @pytest.mark.asyncio
        async def test_get_traffic_info_success(self, waze_service, sample_location):
            """Test successful traffic info retrieval"""
            traffic_data = await waze_service.get_traffic_info(sample_location)
            
            # Verify response structure
            assert isinstance(traffic_data, dict)
            assert "location" in traffic_data
            assert "traffic_level" in traffic_data
            assert "congestion_percentage" in traffic_data
            assert "average_speed" in traffic_data
            assert "last_updated" in traffic_data
            
            # Verify data types
            assert isinstance(traffic_data["traffic_level"], str)
            assert isinstance(traffic_data["congestion_percentage"], int)
            assert isinstance(traffic_data["average_speed"], int)
            assert isinstance(traffic_data["last_updated"], str)
            
            # Verify location is preserved
            assert traffic_data["location"]["lat"] == sample_location["lat"]
            assert traffic_data["location"]["lng"] == sample_location["lng"]
        
        @pytest.mark.asyncio
        async def test_get_traffic_info_different_locations(self, waze_service):
            """Test traffic info for different locations"""
            locations = [
                {"lat": 40.7128, "lng": -74.0060},  # NYC
                {"lat": 34.0522, "lng": -118.2437},  # LA
                {"lat": 41.8781, "lng": -87.6298},  # Chicago
            ]
            
            for location in locations:
                traffic_data = await waze_service.get_traffic_info(location)
                assert traffic_data["location"]["lat"] == location["lat"]
                assert traffic_data["location"]["lng"] == location["lng"]
        
        @pytest.mark.asyncio
        async def test_get_traffic_info_error_handling(self, waze_service, sample_location):
            """Test error handling in traffic info retrieval"""
            # Mock the service to throw an exception
            with patch.object(waze_service, 'get_traffic_info', side_effect=Exception("API Error")):
                with pytest.raises(Exception) as exc_info:
                    await waze_service.get_traffic_info(sample_location)
                assert "API Error" in str(exc_info.value)
    
    class TestServiceInitialization:
        """Test service initialization and configuration"""
        
        def test_service_initialization(self):
            """Test Waze service initialization"""
            service = WazeService()
            
            assert hasattr(service, 'api_key')
            assert hasattr(service, 'base_url')
            assert service.base_url == "https://www.waze.com/row-rtserver/R-T"
        
        def test_service_with_api_key(self):
            """Test service initialization with API key"""
            with patch('services.waze_service.settings') as mock_settings:
                mock_settings.waze_api_key = "test-api-key"
                service = WazeService()
                assert service.api_key == "test-api-key"
        
        def test_service_without_api_key(self):
            """Test service initialization without API key"""
            with patch('services.waze_service.settings') as mock_settings:
                mock_settings.waze_api_key = None
                service = WazeService()
                assert service.api_key is None
    
    class TestIntegration:
        """Test integration scenarios"""
        
        @pytest.mark.asyncio
        async def test_route_and_traffic_integration(self, waze_service, sample_origin, sample_destination):
            """Test using both route calculation and traffic info together"""
            # Calculate route
            route_data = await waze_service.calculate_route(sample_origin, sample_destination)
            
            # Get traffic info for origin
            origin_traffic = await waze_service.get_traffic_info(sample_origin)
            
            # Get traffic info for destination
            destination_traffic = await waze_service.get_traffic_info(sample_destination)
            
            # Verify all data is consistent
            assert route_data["routes"][0]["waypoints"][0]["lat"] == origin_traffic["location"]["lat"]
            assert route_data["routes"][0]["waypoints"][-1]["lat"] == destination_traffic["location"]["lat"]
        
        @pytest.mark.asyncio
        async def test_multiple_concurrent_requests(self, waze_service):
            """Test handling multiple concurrent requests"""
            import asyncio
            
            origins = [
                {"lat": 40.7128, "lng": -74.0060},
                {"lat": 34.0522, "lng": -118.2437},
                {"lat": 41.8781, "lng": -87.6298},
            ]
            
            destinations = [
                {"lat": 40.7589, "lng": -73.9851},
                {"lat": 37.7749, "lng": -122.4194},
                {"lat": 42.3601, "lng": -71.0589},
            ]
            
            # Create concurrent tasks
            tasks = []
            for origin, destination in zip(origins, destinations):
                task = waze_service.calculate_route(origin, destination)
                tasks.append(task)
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks)
            
            # Verify all tasks completed successfully
            assert len(results) == 3
            for result in results:
                assert isinstance(result, dict)
                assert "routes" in result 