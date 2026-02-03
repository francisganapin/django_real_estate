import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate.settings')
django.setup()

from agent_page.models import Property, Agent, PropertyFeatures, NearbyLocation
from datetime import date
from decimal import Decimal
import random





dsadsadsadsadsadsadsa
sadsadsa
d
# Create agents first
agents_data = [
    {"name": "Sarah Johnson", "title": "Senior Real Estate Agent", "phone": "(555) 123-4567", "email": "sarah.johnson@dreamhome.com", "rating": 4.9, "review_count": 127},
    {"name": "Michael Chen", "title": "Luxury Property Specialist", "phone": "(555) 234-5678", "email": "michael.chen@dreamhome.com", "rating": 4.8, "review_count": 98},
    {"name": "Emily Rodriguez", "title": "Buyer's Agent", "phone": "(555) 345-6789", "email": "emily.rodriguez@dreamhome.com", "rating": 4.7, "review_count": 85},
    {"name": "David Williams", "title": "Commercial Real Estate Agent", "phone": "(555) 456-7890", "email": "david.williams@dreamhome.com", "rating": 4.9, "review_count": 156},
    {"name": "Jessica Thompson", "title": "First-Time Buyer Specialist", "phone": "(555) 567-8901", "email": "jessica.thompson@dreamhome.com", "rating": 4.6, "review_count": 72},
    {"name": "Robert Martinez", "title": "Investment Property Expert", "phone": "(555) 678-9012", "email": "robert.martinez@dreamhome.com", "rating": 4.8, "review_count": 110},
    {"name": "Amanda Lee", "title": "Relocation Specialist", "phone": "(555) 789-0123", "email": "amanda.lee@dreamhome.com", "rating": 4.7, "review_count": 64},
    {"name": "James Brown", "title": "Rental Property Agent", "phone": "(555) 890-1234", "email": "james.brown@dreamhome.com", "rating": 4.5, "review_count": 89},
]

print("Creating agents...")
for agent_data in agents_data:
    agent, created = Agent.objects.get_or_create(
        email=agent_data["email"],
        defaults={
            "name": agent_data["name"],
            "title": agent_data["title"],
            "phone": agent_data["phone"],
            "photo": "agent_images/placeholder.jpg",
            "rating": Decimal(str(agent_data["rating"])),
            "review_count": agent_data["review_count"],
        }
    )
    if created:
        print(f"  Created: {agent.name}")
    else:
        print(f"  Exists: {agent.name}")

print(f"Total agents: {Agent.objects.count()}\n")

# Refresh agents list
agents = list(Agent.objects.all())

properties_data = [
    # Houses
    {"title": "Modern Family Home", "property_type": "House", "status": "For Sale", "price": 750000, "bedrooms": 4, "bathrooms": 3, "square_feet": 2800, "city": "Los Angeles", "state": "CA"},
    {"title": "Cozy Suburban House", "property_type": "House", "status": "For Sale", "price": 485000, "bedrooms": 3, "bathrooms": 2, "square_feet": 1850, "city": "San Diego", "state": "CA"},
    {"title": "Luxury Estate", "property_type": "House", "status": "For Sale", "price": 2500000, "bedrooms": 6, "bathrooms": 5, "square_feet": 5500, "city": "Beverly Hills", "state": "CA"},
    {"title": "Charming Cottage", "property_type": "House", "status": "For Rent", "price": 3200, "bedrooms": 2, "bathrooms": 1, "square_feet": 1200, "city": "Santa Monica", "state": "CA"},
    {"title": "Spacious Ranch Home", "property_type": "House", "status": "For Sale", "price": 620000, "bedrooms": 4, "bathrooms": 2, "square_feet": 2400, "city": "Phoenix", "state": "AZ"},
    
    # Apartments
    {"title": "Downtown Loft", "property_type": "Apartment", "status": "For Rent", "price": 2800, "bedrooms": 1, "bathrooms": 1, "square_feet": 850, "city": "New York", "state": "NY"},
    {"title": "Skyline View Apartment", "property_type": "Apartment", "status": "For Rent", "price": 3500, "bedrooms": 2, "bathrooms": 2, "square_feet": 1100, "city": "Chicago", "state": "IL"},
    {"title": "Urban Studio Plus", "property_type": "Apartment", "status": "For Sale", "price": 320000, "bedrooms": 1, "bathrooms": 1, "square_feet": 650, "city": "Seattle", "state": "WA"},
    {"title": "Riverside Apartment", "property_type": "Apartment", "status": "For Rent", "price": 2200, "bedrooms": 2, "bathrooms": 1, "square_feet": 950, "city": "Portland", "state": "OR"},
    {"title": "Penthouse Suite", "property_type": "Apartment", "status": "For Sale", "price": 1850000, "bedrooms": 3, "bathrooms": 3, "square_feet": 2200, "city": "Miami", "state": "FL"},
    
    # Condos
    {"title": "Beachfront Condo", "property_type": "Condo", "status": "For Sale", "price": 890000, "bedrooms": 2, "bathrooms": 2, "square_feet": 1400, "city": "San Diego", "state": "CA"},
    {"title": "Golf Course Condo", "property_type": "Condo", "status": "For Sale", "price": 425000, "bedrooms": 2, "bathrooms": 2, "square_feet": 1200, "city": "Scottsdale", "state": "AZ"},
    {"title": "City Center Condo", "property_type": "Condo", "status": "For Rent", "price": 2600, "bedrooms": 1, "bathrooms": 1, "square_feet": 800, "city": "Denver", "state": "CO"},
    {"title": "Lakeside Condo", "property_type": "Condo", "status": "For Sale", "price": 550000, "bedrooms": 3, "bathrooms": 2, "square_feet": 1600, "city": "Austin", "state": "TX"},
    
    # Townhouses
    {"title": "Modern Townhouse", "property_type": "Townhouse", "status": "For Sale", "price": 680000, "bedrooms": 3, "bathrooms": 3, "square_feet": 2000, "city": "San Francisco", "state": "CA"},
    {"title": "Historic Townhouse", "property_type": "Townhouse", "status": "For Sale", "price": 1200000, "bedrooms": 4, "bathrooms": 3, "square_feet": 2800, "city": "Boston", "state": "MA"},
    {"title": "Family Townhouse", "property_type": "Townhouse", "status": "For Rent", "price": 3800, "bedrooms": 3, "bathrooms": 2, "square_feet": 1800, "city": "Atlanta", "state": "GA"},
    {"title": "Luxury Townhouse", "property_type": "Townhouse", "status": "For Sale", "price": 950000, "bedrooms": 4, "bathrooms": 4, "square_feet": 2500, "city": "Dallas", "state": "TX"},
    
    # More variety
    {"title": "Mountain View Retreat", "property_type": "House", "status": "For Sale", "price": 875000, "bedrooms": 5, "bathrooms": 4, "square_feet": 3200, "city": "Denver", "state": "CO"},
    {"title": "Urban Micro Apartment", "property_type": "Apartment", "status": "For Rent", "price": 1800, "bedrooms": 1, "bathrooms": 1, "square_feet": 450, "city": "New York", "state": "NY"},
]

streets = ["Oak Street", "Maple Avenue", "Pine Road", "Cedar Lane", "Elm Drive", "Birch Boulevard", "Willow Way", "Cherry Court", "Aspen Circle", "Walnut Place"]
zip_codes = {"CA": ["90210", "92101", "90401", "94102"], "NY": ["10001", "10019"], "AZ": ["85001", "85251"], "IL": ["60601"], "WA": ["98101"], "OR": ["97201"], "FL": ["33101"], "CO": ["80202"], "TX": ["78701", "75201"], "MA": ["02101"], "GA": ["30301"]}

print(f"Creating {len(properties_data)} properties...")

for i, data in enumerate(properties_data):
    state = data["state"]
    prop = Property.objects.create(
        title=data["title"],
        description=f"Beautiful {data['property_type'].lower()} located in {data['city']}, {state}. Features {data['bedrooms']} bedrooms and {data['bathrooms']} bathrooms with {data['square_feet']} sq ft of living space. Perfect for families or professionals looking for a great home.",
        property_type=data["property_type"],
        status=data["status"],
        price=Decimal(str(data["price"])),
        price_per_sqft=Decimal(str(round(data["price"] / data["square_feet"], 2))),
        bedrooms=data["bedrooms"],
        bathrooms=data["bathrooms"],
        square_feet=data["square_feet"],
        year_built=date(random.randint(1990, 2023), 1, 1),
        address=f"{random.randint(100, 9999)} {random.choice(streets)}",
        city=data["city"],
        state=state,
        zip_code=random.choice(zip_codes.get(state, ["00000"])),
        main_image="property_images/main_image/placeholder.jpg",
        image_2="property_images/image_2/placeholder.jpg",
        image_3="property_images/image_3/placeholder.jpg",
        agent=random.choice(agents)
    )
    
    # Add some features
    features = [
        ("Swimming Pool", "Heated outdoor swimming pool"),
        ("Garage", "2-car attached garage"),
        ("Central AC", "Central air conditioning"),
        ("Hardwood Floors", "Beautiful hardwood flooring throughout"),
        ("Modern Kitchen", "Updated kitchen with stainless steel appliances"),
    ]
    for name, desc in random.sample(features, random.randint(2, 4)):
        PropertyFeatures.objects.create(property=prop, name=name, description=desc)
    
    # Add nearby locations
    nearby = [
        ("school", "Local Elementary School", random.uniform(0.3, 1.5)),
        ("hospital", "City Hospital", random.uniform(1.0, 5.0)),
        ("mall", "Shopping Center", random.uniform(0.5, 3.0)),
        ("park", "Community Park", random.uniform(0.2, 1.0)),
        ("transport", "Metro Station", random.uniform(0.3, 2.0)),
    ]
    for loc_type, name, distance in random.sample(nearby, random.randint(2, 4)):
        NearbyLocation.objects.create(
            property=prop,
            location_type=loc_type,
            name=name,
            distance=Decimal(str(round(distance, 2))),
            distance_unit="miles"
        )
    
    print(f"  Created: {prop.title}")

print(f"\nDone! Total properties: {Property.objects.count()}")