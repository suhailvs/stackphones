from django.db import models

class PhoneSpec(models.Model):
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=200, blank=True)
    image = models.URLField(max_length=500, blank=True)
    # Network
    network_technology = models.CharField(max_length=100, blank=True)
    network_2g_bands = models.CharField(max_length=200, blank=True)
    network_3g_bands = models.CharField(max_length=200, blank=True)
    network_4g_bands = models.CharField(max_length=500, blank=True)
    network_5g_bands = models.CharField(max_length=500, blank=True)
    network_speed = models.CharField(max_length=100, blank=True)

    # Launch
    announced = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=100, blank=True)

    # Body
    dimensions = models.CharField(max_length=100, blank=True)
    weight = models.CharField(max_length=50, blank=True)
    sim = models.CharField(max_length=100, blank=True)
    body_other = models.TextField(blank=True)

    # Display
    display_type = models.CharField(max_length=100, blank=True)
    display_size = models.CharField(max_length=100, blank=True)
    display_resolution = models.CharField(max_length=100, blank=True)
    display_protection = models.CharField(max_length=100, blank=True)

    # Platform
    os = models.CharField(max_length=100, blank=True)
    chipset = models.CharField(max_length=100, blank=True)
    cpu = models.CharField(max_length=200, blank=True)
    gpu = models.CharField(max_length=100, blank=True)

    # Memory
    card_slot = models.CharField(max_length=100, blank=True)
    internal_memory = models.CharField(max_length=100, blank=True)
    memory_type = models.CharField(max_length=50, blank=True)

    # Main Camera
    main_camera_modules = models.TextField(blank=True)
    main_camera_features = models.CharField(max_length=200, blank=True)
    main_camera_video = models.CharField(max_length=200, blank=True)

    # Selfie Camera
    selfie_camera_modules = models.CharField(max_length=200, blank=True)
    selfie_camera_video = models.CharField(max_length=100, blank=True)

    # Sound
    loudspeaker = models.BooleanField(default=False)
    headphone_jack = models.BooleanField(default=False)

    # Comms
    wlan = models.CharField(max_length=100, blank=True)
    bluetooth = models.CharField(max_length=100, blank=True)
    positioning = models.CharField(max_length=200, blank=True)
    nfc = models.BooleanField(default=False)
    infrared_port = models.BooleanField(default=False)
    radio = models.CharField(max_length=100, blank=True)
    usb = models.CharField(max_length=100, blank=True)

    # Features
    sensors = models.CharField(max_length=300, blank=True)

    # Battery
    battery_type = models.CharField(max_length=100, blank=True)
    charging = models.TextField(blank=True)

    # Misc
    colors = models.CharField(max_length=100, blank=True)
    price = models.CharField(max_length=100, blank=True)

    # EU Label
    eu_energy_class = models.CharField(max_length=20, blank=True)
    eu_battery_endurance = models.CharField(max_length=100, blank=True)
    eu_free_fall_class = models.CharField(max_length=100, blank=True)
    eu_repairability_class = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.chipset} - {self.announced}"

class NoPhone(models.Model):
    number = models.IntegerField(unique=True)
    error = models.TextField()
    def __str__(self):
        return self.number