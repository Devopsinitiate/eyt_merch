from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, TournamentRegistration


class UserSignupForm(UserCreationForm):
    """Registration form for new users"""
    full_name = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm placeholder:opacity-30',
            'placeholder': 'John Doe'
        })
    )
    
    gamer_tag = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 pl-8 rounded text-sm placeholder:opacity-30 uppercase font-bold tracking-tight',
            'placeholder': 'EYT_LEGEND'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm placeholder:opacity-30',
            'placeholder': 'you@example.com'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm placeholder:opacity-30',
            'placeholder': '+1 234 567 8900'
        })
    )
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm placeholder:opacity-30',
            'placeholder': 'Enter password'
        })
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm placeholder:opacity-30',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['full_name', 'gamer_tag', 'email', 'phone', 'password1', 'password2']
    
    def clean_gamer_tag(self):
        gamer_tag = self.cleaned_data.get('gamer_tag')
        if gamer_tag:
            gamer_tag = gamer_tag.upper().strip()
            if CustomUser.objects.filter(gamer_tag=gamer_tag).exists():
                raise forms.ValidationError("This gamer tag is already taken. Choose another one.")
        return gamer_tag
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Use email as username
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Login form"""
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm placeholder:opacity-30',
            'placeholder': 'you@example.com',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm placeholder:opacity-30',
            'placeholder': 'Enter your password'
        })
    )


class UserProfileForm(forms.ModelForm):
    """Profile edit form"""
    class Meta:
        model = CustomUser
        fields = ['full_name', 'gamer_tag', 'email', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm'
            }),
            'gamer_tag': forms.TextInput(attrs={
                'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm uppercase font-bold',
                'readonly': True  # Don't allow gamer tag changes
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm'
            }),
        }


class TournamentRegistrationForm(forms.ModelForm):
    """Registration form for the EYT gaming tournament (QR-based)"""
    class Meta:
        model = TournamentRegistration
        fields = ['full_name', 'gender', 'gamer_tag', 'email', 'payment_reference']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm placeholder:opacity-30',
                'placeholder': 'John Doe',
                'autofocus': True
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm'
            }),
            'gamer_tag': forms.TextInput(attrs={
                'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 pl-8 rounded text-sm placeholder:opacity-30 uppercase font-bold tracking-tight',
                'placeholder': 'EYT_LEGEND'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm placeholder:opacity-30',
                'placeholder': 'you@example.com'
            }),
            'payment_reference': forms.TextInput(attrs={
                'class': 'w-full bg-slate-50 dark:bg-black border border-slate-200 dark:border-white/10 p-3 rounded text-sm placeholder:opacity-30',
                'placeholder': 'Optional — bank transfer reference / receipt number'
            }),
        }

    def clean_gamer_tag(self):
        gamer_tag = self.cleaned_data.get('gamer_tag')
        if gamer_tag:
            gamer_tag = gamer_tag.upper().strip()
            if TournamentRegistration.objects.filter(gamer_tag=gamer_tag).exists():
                raise forms.ValidationError(
                    'This gamer tag has already been registered. Choose another one.'
                )
        return gamer_tag

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if TournamentRegistration.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email has already been registered for the tournament.'
            )
        return email
