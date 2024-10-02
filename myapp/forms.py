from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Category, UserProfile, Product, Cart, Supplier

# Form for Product
class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.filter(parent__isnull=True), required=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'is_active', 'quantity', 'reorderlevel', 'category']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        return quantity

    def clean_reorderlevel(self):
        reorderlevel = self.cleaned_data.get('reorderlevel')
        if reorderlevel < 0:
            raise forms.ValidationError('Reorder level cannot be negative.')
        return reorderlevel

# Form for User Profile Registration
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = UserProfile  # Ensure you're using your custom UserProfile model
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

# Form for Updating User Profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']

# Form for User Profile Creation with additional fields
class UserProfileCreationForm(UserCreationForm):
    age = forms.IntegerField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'password1', 'password2', 'age', 'email', 'profile_picture')

# Form for Cart management
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity']

# Custom Password Change Form
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Old Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm Password'

# Form for Supplier management
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

# from django import forms
# from .models import Category, UserProfile, Product, Cart, Supplier  # Ensure Product is imported correctly
# from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
# from django.contrib.auth.models import User



# class ProductForm(forms.ModelForm):
#     category = forms.ModelChoiceField(queryset=Category.objects.filter(parent__isnull=True), required=True)

#     class Meta:
#         model = Product
#         fields = ['name', 'description', 'price', 'image', 'is_active', 'quantity', 'reorderlevel', 'category']
        

#     # other fields like user, address, etc.

#     # other fields like user, address, etc.


# from django import forms
# from .models import UserProfile  # Ensure UserProfile is imported

# class CustomUserCreationForm(forms.ModelForm):
#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = UserProfile  # Use UserProfile here
#         fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')
        
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords do not match.")
        
#         return cleaned_data


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']

# # forms.py
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import UserProfile

# class UserProfileCreationForm(UserCreationForm):
#     age = forms.IntegerField(required=False)

#     class Meta:
#         model = UserProfile
#         fields = ('username', 'password1', 'password2', 'age', 'email', 'profile_picture')


# class CartForm(forms.ModelForm):
#     class Meta:
#         model = Cart
#         fields = ['user', 'product', 'quantity']

# class CustomPasswordChangeForm(PasswordChangeForm): 
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['old_password'].label = 'Old Password'
#         self.fields['new_password1'].label = 'New Password'
#         self.fields['new_password2'].label = 'Confirm Password'

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=30)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

# class SupplierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = '__all__'
