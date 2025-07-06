import React, { useEffect, useRef, useState } from 'react';
import './MapSelector.css';

interface MapSelectorProps {
  operationAreaType: 'circle' | 'polygon';
  centerLat?: number;
  centerLng?: number;
  radiusKm?: number;
  polygonCoordinates?: Array<{ lat: number; lng: number }>;
  onAreaChange: (area: {
    type: 'circle' | 'polygon';
    centerLat?: number;
    centerLng?: number;
    radiusKm?: number;
    polygonCoordinates?: Array<{ lat: number; lng: number }>;
  }) => void;
}

declare global {
  interface Window {
    google: any;
  }
}

const MapSelector: React.FC<MapSelectorProps> = ({
  operationAreaType,
  centerLat = 40.7128,
  centerLng = -74.0060,
  radiusKm = 10,
  polygonCoordinates = [],
  onAreaChange
}) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const circleRef = useRef<any>(null);
  const polygonRef = useRef<any>(null);
  const drawingManagerRef = useRef<any>(null);
  const [isMapLoaded, setIsMapLoaded] = useState(false);

  useEffect(() => {
    // Load Google Maps API
    const loadGoogleMaps = () => {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.VITE_GOOGLE_MAPS_API_KEY}&libraries=drawing`;
      script.async = true;
      script.defer = true;
      script.onload = () => {
        setIsMapLoaded(true);
        initializeMap();
      };
      document.head.appendChild(script);
    };

    if (!window.google) {
      loadGoogleMaps();
    } else {
      setIsMapLoaded(true);
      initializeMap();
    }

    return () => {
      // Cleanup
      if (mapInstanceRef.current) {
        // Google Maps doesn't need explicit cleanup
      }
    };
  }, []);

  const initializeMap = () => {
    if (!mapRef.current || !window.google) return;

    const mapOptions = {
      center: { lat: centerLat, lng: centerLng },
      zoom: 12,
      mapTypeId: window.google.maps.MapTypeId.ROADMAP
    };

    const map = new window.google.maps.Map(mapRef.current, mapOptions);
    mapInstanceRef.current = map;

    // Initialize drawing manager
    const drawingManager = new window.google.maps.drawing.DrawingManager({
      drawingMode: null,
      drawingControl: true,
      drawingControlOptions: {
        position: window.google.maps.ControlPosition.TOP_CENTER,
        drawingModes: [
          window.google.maps.drawing.OverlayType.CIRCLE,
          window.google.maps.drawing.OverlayType.POLYGON
        ]
      }
    });

    drawingManager.setMap(map);
    drawingManagerRef.current = drawingManager;

    // Add event listeners for drawing
    window.google.maps.event.addListener(drawingManager, 'circlecomplete', (circle: any) => {
      clearExistingShapes();
      circleRef.current = circle;
      
      const center = circle.getCenter();
      const radius = circle.getRadius() / 1000; // Convert to km
      
      onAreaChange({
        type: 'circle',
        centerLat: center.lat(),
        centerLng: center.lng(),
        radiusKm: radius
      });
    });

    window.google.maps.event.addListener(drawingManager, 'polygoncomplete', (polygon: any) => {
      clearExistingShapes();
      polygonRef.current = polygon;
      
      const path = polygon.getPath();
      const coordinates = path.getArray().map((latLng: any) => ({
        lat: latLng.lat(),
        lng: latLng.lng()
      }));
      
      onAreaChange({
        type: 'polygon',
        polygonCoordinates: coordinates
      });
    });

    // Draw existing area if provided
    drawExistingArea();
  };

  const clearExistingShapes = () => {
    if (circleRef.current) {
      circleRef.current.setMap(null);
      circleRef.current = null;
    }
    if (polygonRef.current) {
      polygonRef.current.setMap(null);
      polygonRef.current = null;
    }
  };

  const drawExistingArea = () => {
    if (!mapInstanceRef.current) return;

    clearExistingShapes();

    if (operationAreaType === 'circle' && centerLat && centerLng && radiusKm) {
      const circle = new window.google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: mapInstanceRef.current,
        center: { lat: centerLat, lng: centerLng },
        radius: radiusKm * 1000 // Convert km to meters
      });
      circleRef.current = circle;
    } else if (operationAreaType === 'polygon' && polygonCoordinates.length > 0) {
      const polygon = new window.google.maps.Polygon({
        paths: polygonCoordinates,
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: mapInstanceRef.current
      });
      polygonRef.current = polygon;
    }
  };

  useEffect(() => {
    if (isMapLoaded) {
      drawExistingArea();
    }
  }, [operationAreaType, centerLat, centerLng, radiusKm, polygonCoordinates, isMapLoaded]);

  const handleTypeChange = (type: 'circle' | 'polygon') => {
    clearExistingShapes();
    onAreaChange({
      type,
      centerLat: type === 'circle' ? centerLat : undefined,
      centerLng: type === 'circle' ? centerLng : undefined,
      radiusKm: type === 'circle' ? radiusKm : undefined,
      polygonCoordinates: type === 'polygon' ? polygonCoordinates : undefined
    });
  };

  if (!isMapLoaded) {
    return (
      <div className="map-selector">
        <div className="map-loading">
          <div className="spinner"></div>
          <p>Loading map...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="map-selector">
      <div className="map-controls">
        <div className="area-type-selector">
          <label>Operation Area Type:</label>
          <div className="radio-group">
            <label>
              <input
                type="radio"
                name="areaType"
                value="circle"
                checked={operationAreaType === 'circle'}
                onChange={() => handleTypeChange('circle')}
              />
              Circle
            </label>
            <label>
              <input
                type="radio"
                name="areaType"
                value="polygon"
                checked={operationAreaType === 'polygon'}
                onChange={() => handleTypeChange('polygon')}
              />
              Polygon
            </label>
          </div>
        </div>
        
        {operationAreaType === 'circle' && (
          <div className="circle-controls">
            <label>
              Radius (km):
              <input
                type="number"
                min="0.1"
                max="100"
                step="0.1"
                value={radiusKm || 10}
                onChange={(e) => onAreaChange({
                  type: 'circle',
                  centerLat,
                  centerLng,
                  radiusKm: parseFloat(e.target.value)
                })}
              />
            </label>
          </div>
        )}
      </div>
      
      <div className="map-instructions">
        <p>
          {operationAreaType === 'circle' 
            ? 'Click and drag to draw a circle, or use the radius input above.'
            : 'Click on the map to draw a polygon. Double-click to finish.'
          }
        </p>
      </div>
      
      <div ref={mapRef} className="map-container" />
    </div>
  );
};

export default MapSelector; 