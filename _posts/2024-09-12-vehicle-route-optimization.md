---
layout: post
title: Vehicle Route Optimization with Fuel Constraints
date: 2024-09-12 11:59:00-0400
description: A practical guide to implementing a vehicle routing system with fuel constraints using Python and PostGIS
categories: vehicle-routing optimization route-planning
mermaid: true
giscus_comments: true
---

In this post, we examine the strategies that delivery companies use to optimize their routes by integrating fuel constraints. This post provides a professional guide to developing an optimal routing strategy for vehicles navigating the United States, balancing fuel efficiency and cost effectiveness.

### Problem Definition

To address this challenge, our solution must satisfy the following requirements:
• A vehicle must be capable of traveling up to 1000 miles on a single tank of fuel.
• There is access to approximately 6000 fuel stations with known geographic coordinates and fuel prices.
• The objective is to minimize the overall fuel expenditure.

Here's a visual representation of our problem:

<div class="mermaid">
graph LR
    A[Start Location] --> B[Route Planning]
    B --> C[Find Nearby Stations]
    C --> D[Calculate Costs]
    D --> E[Choose Next Stop]
    E --> F[Destination Reached?]
    F -->|No| C
    F -->|Yes| G[End Location]
    
    style A fill:#f96,stroke:#333,stroke-width:2px
    style G fill:#f96,stroke:#333,stroke-width:2px
    style B fill:#9cf,stroke:#333,stroke-width:2px
    style C fill:#9f9,stroke:#333,stroke-width:2px
    style D fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#ff9,stroke:#333,stroke-width:2px
    style F fill:#fcc,stroke:#333,stroke-width:2px
</div>

### Proposed Approach

Our solution comprises three core components:
1. Location Services – Integrating the Google Maps API to accurately convert addresses into geographic coordinates.
2. Data Storage – Utilizing PostGIS for efficient storage and querying of fuel station data.
3. Route Optimization – Employing a greedy algorithm to determine the optimal route while considering fuel constraints and cost minimization.

### 1. Location Services

We begin by integrating the Google Maps API for precise geocoding and route planning. The service converts addresses into coordinates and retrieves route information as demonstrated below:

```python
from googlemaps import Client
from typing import Tuple

class LocationService:
    def __init__(self, api_key: str):
        self.gmaps = Client(key=api_key)
    
    def geocode(self, address: str) -> Tuple[float, float]:
        """Convert address to coordinates"""
        result = self.gmaps.geocode(address)
        if not result:
            raise ValueError(f"Could not geocode address: {address}")
        
        location = result[0]['geometry']['location']
        return location['lat'], location['lng']
    
    def get_route(self, origin: Tuple[float, float], 
                 destination: Tuple[float, float]) -> list:
        """Get route points between two locations"""
        route = self.gmaps.directions(
            origin,
            destination,
            mode="driving"
        )
        
        if not route:
            raise ValueError("No route found")
        
        # Extract route points
        points = []
        for step in route[0]['legs'][0]['steps']:
            points.append((
                step['start_location']['lat'],
                step['start_location']['lng']
            ))
        
        # Add destination
        points.append((
            route[0]['legs'][0]['end_location']['lat'],
            route[0]['legs'][0]['end_location']['lng']
        ))
        
        return points
```

### 2. Data Storage

We'll use PostGIS to efficiently store and query fuel stations. Here's our Django model:

```python
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class FuelStation(models.Model):
    name = models.CharField(max_length=200)
    location = models.PointField(srid=4326)  # SRID for GPS coordinates
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    retail_price = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        indexes = [
            models.Index(fields=['retail_price']),
            # PostGIS will automatically create spatial index
        ]
```

### 3. Route Optimization

Now for the core logic. We'll use a greedy algorithm that:
1. Follows the route points
2. Checks fuel level at each point
3. Finds the cheapest reachable station when needed
If the vehicle can reach the destination without refueling, it will do so. Otherwise, it will find the cheapest reachable station.

Here's the main optimizer class, broken down into manageable pieces:

```python
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
import math
import logging

logger = logging.getLogger(__name__)

class GreedyRouteOptimizer:
    def __init__(self, max_range_miles=1000, mpg=10):
        self.max_range_miles = max_range_miles
        self.mpg = mpg
        self.max_tank_gallons = max_range_miles / mpg
```

#### Distance Calculation

```python
def calculate_distance(self, point1: tuple[float, float], 
                      point2: tuple[float, float]) -> float:
    """Calculate haversine distance between two points"""
    lat1, lon1 = point1
    lat2, lon2 = point2
    R = 3958.8  # Earth radius in miles
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
```

#### Finding Optimal Fuel Stops

The core optimization logic:

```python
def find_optimal_stops(self, route_points: list[tuple[float, float]], 
                      total_distance: float) -> dict:
    """Find optimal fuel stops along the route"""
    current_fuel_range = self.max_range_miles
    total_cost = 0.0
    stops = []
    current_position = route_points[0]
    distance_remaining = total_distance
    new_route = []
    
    # Short route optimization
    if total_distance <= self.max_range_miles:
        logger.info("Direct route possible - no fuel stops needed")
        return {
            'route': route_points,
            'stops': [],
            'total_cost': 0.0
        }
    
    # Process each route segment
    for next_point in route_points[1:]:
        segment_distance = self.calculate_distance(
            current_position, next_point)
        
        if segment_distance <= current_fuel_range:
            # Can reach next point with current fuel
            self._process_direct_segment(
                current_position, next_point, 
                segment_distance, new_route)
            current_fuel_range -= segment_distance
            current_position = next_point
            
        else:
            # Need to find a fuel stop
            station = self._find_fuel_stop(
                current_position, current_fuel_range)
            
            if not station:
                raise Exception("No reachable fuel stations found")
                
            stop_info = self._process_fuel_stop(
                station, current_position, 
                current_fuel_range, total_cost)
                
            stops.append(stop_info['station'])
            total_cost += stop_info['cost']
            current_position = (station.location.y, station.location.x)
            current_fuel_range = self.max_range_miles
            new_route.append(stop_info['location'])
    
    return {
        'route': new_route,
        'stops': stops,
        'total_cost': total_cost
    }
```

#### Finding the Next Fuel Station

```python
def _find_fuel_stop(self, current_point: Point, 
                    max_range: float) -> FuelStation:
    """Find the cheapest reachable fuel station"""
    nearby_stations = (FuelStation.objects
        .annotate(distance=Distance('location', current_point))
        .filter(distance__lte=D(mi=max_range))
        .order_by('retail_price', 'distance'))
    
    if not nearby_stations.exists():
        return None
        
    return nearby_stations.first()
```

### Route Visualization

The diagram below illustrates a sample optimized route with designated fuel stops:

<div class="mermaid">
graph LR
    A[Los Angeles] -->|350mi| B[Station 1]
    B -->|400mi| C[Station 2]
    C -->|300mi| D[Station 3]
    D -->|450mi| E[New York]
    
    style A fill:#f96,stroke:#333,stroke-width:2px
    style E fill:#f96,stroke:#333,stroke-width:2px
    style B fill:#9f9,stroke:#333,stroke-width:2px
    style C fill:#9f9,stroke:#333,stroke-width:2px
    style D fill:#9f9,stroke:#333,stroke-width:2px
</div>

### Usage Example
```python
# Initialize services
location_service = LocationService(GOOGLE_MAPS_API_KEY)
optimizer = GreedyRouteOptimizer()

# Get coordinates
start = location_service.geocode("Los Angeles, CA")
end = location_service.geocode("New York, NY")

# Get route points
route_points = location_service.get_route(start, end)

# Find optimal stops
result = optimizer.find_optimal_stops(
    route_points,
    optimizer.calculate_distance(start, end)
)

print(f"Total fuel cost: ${result['total_cost']:.2f}")
for stop in result['stops']:
    print(f"Fuel stop: {stop.city}, {stop.state} - ${stop.retail_price}/gal")
```

### Performance Considerations

Our implementation is designed with efficiency in mind:   
• **Spatial Indexing**: Leveraging PostGIS's built-in spatial indexes for rapid data retrieval.  
• **Distance Calculations**: Utilizing the Haversine formula for fast and accurate distance approximations.  
• **Greedy Approach**: A pragmatic algorithm that, while not globally optimal, effectively addresses real-world constraints.  

### Future Improvements

Potential enhancements include:
• Integrating real-time fuel pricing data.
• Incorporating live traffic and road condition updates.
• Supporting simultaneous routing for multiple vehicles.
• Implementing time-window constraints for fuel station operations.

### Conclusion

In summary, this implementation offers a robust approach to optimizing vehicle routes under stringent fuel constraints. Although the current solution employs a greedy strategy, it establishes a solid foundation for further enhancements and real-world applications. The complete code is available on [GitHub](https://github.com/dipespandey/spotter-solution), and contributions are welcome to adapt and extend this solution for diverse operational needs.

---
