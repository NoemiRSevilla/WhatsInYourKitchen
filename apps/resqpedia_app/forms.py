from .models import User
from django import forms
from django.contrib.auth.hashers import check_password
import datetime

# def get_image_path(instance, filename):
#     return os.path.join('recipe_picture', str(instance.id), filename)

class RegisterUserForm(forms.Form):
    # user_picture = forms.ImageField(upload_to='images/')
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    birthdate = forms.DateField(initial=datetime.date.today)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=150,widget=forms.PasswordInput)

    def clean_password(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']
            if password == confirm_password:
                return confirm_password
        raise forms.ValidationError('Passwords do not match.')


class LoginUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)

class EditUserForm(forms.Form):
    # user_picture = forms.ImageField(upload_to='images/')
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=150,widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        passwordrepeat = cleaned_data.get("passwordrepeat")
        if password != passwordrepeat:
            raise forms.ValidationError("Passwords must match.")
        return cleaned_data


class AddRecipeForm(forms.Form):
    # recipe_picture = models.ImageField(upload_to='images/')
    prep_time = forms.IntegerField()
    cook_time = forms.IntegerField()
    number_of_servings = forms.IntegerField()
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget = forms.Textarea)
    ingredients = forms.CharField(widget = forms.Textarea)
    directions = forms.CharField(widget = forms.Textarea)
    categories = forms.CharField(widget = forms.Textarea)

class EditRecipeForm(forms.Form):
    # recipe_picture = models.ImageField(upload_to='images/')
    prep_time = forms.IntegerField()
    cook_time = forms.IntegerField()
    number_of_servings = forms.IntegerField()
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget = forms.Textarea)
    ingredients = forms.CharField(widget = forms.Textarea)
    directions = forms.CharField(widget = forms.Textarea)
    categories = forms.CharField(widget = forms.Textarea)


class AddMessageForm(forms.Form):
    # message_picture = models.ImageField(upload_to='images/')
    message = forms.CharField(widget = forms.Textarea)


class EditMessageForm(forms.Form):
    # message_picture = models.ImageField(upload_to='images/')
    message = forms.CharField(widget = forms.Textarea)

class AddCommentForm(forms.Form):
    # comment_picture = models.ImageField(upload_to='images/')
    comment = forms.CharField(widget = forms.Textarea)

class EditCommentForm(forms.Form):
    # comment_picture = models.ImageField(upload_to='images/')
    comment = forms.CharField(widget = forms.Textarea)