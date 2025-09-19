from django.db import models
from django.core.validators import EmailValidator, RegexValidator

# Create your models here.

class Contact(models.Model):
    """
    Model to store contact information
    """
    
    # Basic Information
    fullname = models.CharField(max_length=200, help_text="Contact's full name")
    
    # Contact Details
    email = models.EmailField(
        unique=True, 
        blank=True,
        null=True,
        validators=[EmailValidator()],
        help_text="Contact's email address"
    )
    phone_number = models.CharField(
        max_length=20,
        # validators=[RegexValidator(
        #     regex=r'^\+?1?\d{9,15}$',
        #     message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        # )],
        help_text="Contact's phone number"
    )
    
    # Additional Information
    address = models.TextField(blank=True, null=True, help_text="Contact's address")
    country = models.CharField(max_length=100, blank=True, null=True, help_text="Contact's country")
    
    # Notes
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the contact")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the contact was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the contact was last updated")
    is_active = models.BooleanField(default=True, help_text="Whether the contact is active")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['fullname']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        email_display = self.email if self.email else "No email"
        return f"{self.fullname} ({email_display})"
