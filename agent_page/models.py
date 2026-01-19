from django.db import models

# Create your models here.
class Property(models.Model):

    STATUS_CHOICES = [
        ('for_sale','For Sale'),
        ('for_rent','For Rent'),
        ('sold','Sold'),
        ('pending','Pending')
    ]

    TYPE_CHOICES = [
        ('house','House'),
        ('apartment','Apartment'),
        ('condo','Condo'),
        ('townhouse','Townhouse'),
    ]

    #information 
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=100,choices=TYPE_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    #PRICING
    price = models.DecimalField(max_digits=12,decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    square_feet = models.PositiveIntegerField()
    year_built = models.DateField()

    #location
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    #photo
    main_image = models.ImageField(upload_to='property_images/main_image/')
    image_2 = models.ImageField(upload_to='property_images/image_2/')
    image_3 = models.ImageField(upload_to='property_images/image_3/')

    #timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    agent = models.ForeignKey('Agent', on_delete=models.SET_NULL, null=True, related_name='properties')


    map_image = models.ImageField(upload_to='property_images/map_image/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
 

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Properties'

class PropertyFeatures(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.property.title} - {self.name}'

class Agent(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True)  # e.g., "Senior Real Estate Agent"
    photo = models.ImageField(upload_to='agent_images/')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    review_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class PropertyInquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Inquiry From {self.full_name} for {self.property.title}'
    
    class Meta:
        verbose_name_plural = 'Property Inquiries'

class NearbyLocation(models.Model):
    LOCATION_TYPE_CHOICES = [
        ('school', 'School'),
        ('hospital', 'Hospital'),
        ('bank', 'Bank'),
        ('mall', 'Mall'),
        ('transport', 'Transportation'),
        ('city', 'City'),
        ('airport', 'Airport'),
        ('park', 'Park'),
        ('beach', 'Beach'),
        ('museum', 'Museum'),
        ('zoo', 'Zoo'),
        ('gym', 'Gym'),
        ('supermarket', 'Supermarket'),
        ('restaurant', 'Restaurant'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='nearby_locations')
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPE_CHOICES)
    name = models.CharField(max_length=200)  # "Beverly Hills High"
    distance = models.DecimalField(max_digits=5, decimal_places=2)  # 0.8
    distance_unit = models.CharField(max_length=10, default='miles')  # "miles" or "km"
    
    def __str__(self):
        return f"{self.name} - {self.distance} {self.distance_unit}"


class PropertyViews(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"View for {self.property.title} from {self.ip_address}"