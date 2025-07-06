import React, { useEffect, useRef, useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
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
  const { t } = useLanguage();
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const circleRef = useRef<any>(null);
  const polygonRef = useRef<any>(null);
  const drawingManagerRef = useRef<any>(null);
  const [isMapLoaded, setIsMapLoaded] = useState(false);
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);
  const markerRef = useRef<any>(null);
  const [drawingMode, setDrawingMode] = useState<'circle' | 'polygon' | null>(operationAreaType);
  const [instructions, setInstructions] = useState('');

  // Try to get user's current location on mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        () => {
          setUserLocation(null); // Use default if denied
        }
      );
    }
  }, []);

  useEffect(() => {
    // Load Google Maps API only once
    const loadGoogleMaps = () => {
      // Check if script already exists
      if (document.querySelector('script[data-google-maps]')) {
        // If already loaded, just initialize
        if (window.google && window.google.maps) {
          setIsMapLoaded(true);
          initializeMap();
        }
        return;
      }
      const script = document.createElement('script');
      // Get API key - use environment variable or fallback
      const apiKey = process.env.NODE_ENV === 'test' ? 'test-key' : 
                    import.meta.env.VITE_GOOGLE_MAPS_API_KEY || 
                    (window as any).__GOOGLE_MAPS_API_KEY__ || 
                    'test-key';
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=drawing`;
      script.async = true;
      script.defer = true;
      script.setAttribute('data-google-maps', 'true');
      script.onload = () => {
        setIsMapLoaded(true);
        initializeMap();
      };
      script.onerror = () => {
        console.warn('Failed to load Google Maps API. Map functionality will be disabled.');
        setIsMapLoaded(false);
      };
      document.head.appendChild(script);
    };

    if (!window.google || !window.google.maps) {
      loadGoogleMaps();
    } else {
      setIsMapLoaded(true);
      initializeMap();
    }

    return () => {
      // Cleanup (no-op for Google Maps)
    };
  }, [userLocation]);

  // Update instructions and drawing mode on type change
  useEffect(() => {
    if (operationAreaType === 'circle') {
      setInstructions(t('companies.operationAreaInstructions.circle'));
      setDrawingMode('circle');
    } else {
      setInstructions(t('companies.operationAreaInstructions.polygon'));
      setDrawingMode('polygon');
    }
    // Auto-select drawing tool if map/drawingManager is ready
    if (drawingManagerRef.current) {
      drawingManagerRef.current.setDrawingMode(
        operationAreaType === 'circle'
          ? window.google.maps.drawing.OverlayType.CIRCLE
          : window.google.maps.drawing.OverlayType.POLYGON
      );
    }
    // Remove any marker if switching to polygon
    if (operationAreaType === 'polygon' && markerRef.current) {
      markerRef.current.setMap(null);
      markerRef.current = null;
    }
  }, [operationAreaType, isMapLoaded, t]);

  const initializeMap = () => {
    if (!mapRef.current || !window.google || !window.google.maps) return;

    // Use user location if available
    const initialCenter = userLocation || { lat: centerLat, lng: centerLng };
    const mapOptions = {
      center: initialCenter,
      zoom: 12,
      mapTypeId: window.google.maps.MapTypeId.ROADMAP
    };

    const map = new window.google.maps.Map(mapRef.current, mapOptions);
    mapInstanceRef.current = map;

    // Add click listener for setting a marker and updating form
    map.addListener('click', (e: any) => {
      if (operationAreaType === 'circle') {
        // Place or move marker
        if (markerRef.current) {
          markerRef.current.setMap(null);
        }
        markerRef.current = new window.google.maps.Marker({
          position: e.latLng,
          map: mapInstanceRef.current,
        });
        // Update form
        onAreaChange({
          type: 'circle',
          centerLat: e.latLng.lat(),
          centerLng: e.latLng.lng(),
          radiusKm: radiusKm
        });
      }
      // For polygon, let drawing manager handle
    });

    // Initialize drawing manager
    const drawingManager = new window.google.maps.drawing.DrawingManager({
      drawingMode: operationAreaType === 'circle'
        ? window.google.maps.drawing.OverlayType.CIRCLE
        : window.google.maps.drawing.OverlayType.POLYGON,
      drawingControl: true,
      drawingControlOptions: {
        position: window.google.maps.ControlPosition.TOP_CENTER,
        drawingModes: [
          window.google.maps.drawing.OverlayType.CIRCLE,
          window.google.maps.drawing.OverlayType.POLYGON
        ]
      },
      circleOptions: {
        editable: true,
        draggable: true
      },
      polygonOptions: {
        editable: true,
        draggable: true
      }
    });

    drawingManager.setMap(map);
    drawingManagerRef.current = drawingManager;

    // Add event listeners for drawing
    window.google.maps.event.addListener(drawingManager, 'circlecomplete', (circle: any) => {
      clearExistingShapes();
      circleRef.current = circle;
      if (markerRef.current) markerRef.current.setMap(null);
      // Show marker at center
      const center = circle.getCenter();
      markerRef.current = new window.google.maps.Marker({
        position: center,
        map: mapInstanceRef.current,
      });
      // Allow editing/deleting
      circle.setEditable(true);
      circle.setDraggable(true);
      // Update on edit
      window.google.maps.event.addListener(circle, 'center_changed', () => {
        const c = circle.getCenter();
        markerRef.current.setPosition(c);
        onAreaChange({
          type: 'circle',
          centerLat: c.lat(),
          centerLng: c.lng(),
          radiusKm: circle.getRadius() / 1000
        });
      });
      window.google.maps.event.addListener(circle, 'radius_changed', () => {
        const c = circle.getCenter();
        onAreaChange({
          type: 'circle',
          centerLat: c.lat(),
          centerLng: c.lng(),
          radiusKm: circle.getRadius() / 1000
        });
      });
      // Delete on right-click
      window.google.maps.event.addListener(circle, 'rightclick', () => {
        clearExistingShapes();
        onAreaChange({ type: 'circle' });
      });
      onAreaChange({
        type: 'circle',
        centerLat: center.lat(),
        centerLng: center.lng(),
        radiusKm: circle.getRadius() / 1000
      });
    });

    window.google.maps.event.addListener(drawingManager, 'polygoncomplete', (polygon: any) => {
      clearExistingShapes();
      polygonRef.current = polygon;
      if (markerRef.current) markerRef.current.setMap(null);
      polygon.setEditable(true);
      polygon.setDraggable(true);
      // Update on edit
      window.google.maps.event.addListener(polygon.getPath(), 'set_at', () => {
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
      window.google.maps.event.addListener(polygon.getPath(), 'insert_at', () => {
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
      // Delete on right-click
      window.google.maps.event.addListener(polygon, 'rightclick', () => {
        clearExistingShapes();
        onAreaChange({ type: 'polygon' });
      });
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
    if (markerRef.current) {
      markerRef.current.setMap(null);
      markerRef.current = null;
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
          <p>{t('common.loading')}</p>
          <p className="map-error">
            <small>Note: Google Maps API key may be required for full functionality</small>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="map-selector">
      <div className="map-controls">
        <div className="area-type-selector">
          <label>{t('companies.operationAreaType')}:</label>
          <div className="radio-group">
            <label>
              <input
                type="radio"
                name="areaType"
                value="circle"
                checked={operationAreaType === 'circle'}
                onChange={() => handleTypeChange('circle')}
              />
              {t('companies.circle')}
            </label>
            <label>
              <input
                type="radio"
                name="areaType"
                value="polygon"
                checked={operationAreaType === 'polygon'}
                onChange={() => handleTypeChange('polygon')}
              />
              {t('companies.polygon')}
            </label>
          </div>
        </div>
        {operationAreaType === 'circle' && (
          <div className="circle-controls">
            <label>
              {t('companies.radius')}:
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
        <p>{instructions}</p>
        <p><em>{t('companies.operationAreaInstructions.tip')}</em></p>
      </div>
      <div ref={mapRef} className="map-container" />
    </div>
  );
};

export default MapSelector; 