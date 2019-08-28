from django.db import models
from datetime import datetime
import re
import bcrypt
import os

class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        bcrypt.hashpw('test'.encode(), bcrypt.gensalt())
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "<div class='ohno'>First name should at least be 2 characters</div>"
        else:
            if not NAME_REGEX.match(postData['first_name']):
                errors["first_name"] = "<div class='ohno'>First name must contain only letters</div>"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "<div class='ohno'>Last name should at least be 2 characters</div>"
        else:
            if not NAME_REGEX.match(postData['last_name']):
                errors["last_name"] = "<div class='ohno'>Last name must contain only letters</div>"
        if len(postData['email']) < 1:
            errors["email"] = "<div class='ohno'>Email required</div>"
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors["email"] = "<div class='ohno'>Must enter valid email</div>"
        if len(postData['birthdate']) < 1:
            errors["birthdate"] = "<div class='ohno'>Birthdate required</div>"
        else:
            birthdate = datetime.strptime(postData['birthdate'], "%Y-%m-%d")
            present = datetime.now()
            if ((present - birthdate).days/365 < 13):
                errors['birthdate'] = "<div class='ohno'>You have to at least be 13 years old to register</div>"
        try:
            User.objects.get(email=postData['email'])
            errors['email'] = "<div class='ohno'>Email already registered</div>"
        except:
            pass
        if len(postData['password']) < 1:
            errors['password'] = "<div class='ohno'>Password required</div>"
        else:
            if len(postData['password']) < 8:
                errors['password'] = "<div class='ohno'>Password has to be at least 8 characters</div>"
        if postData['confirmpassword'] != postData['password']:
            errors['confirmpassword'] = "<div class='ohno'>Password has to match</div>"
        return errors
    def login_validator(self, postData):
        errors = {}
        try:
            user = User.objects.get(email=postData['email'])
        except:
            errors['password'] = "<div class='ohno'>You could not be logged in</div>"
            return errors
        if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            return errors
        else:
            errors['password'] = "<div class='ohno'>You could not be logged in</div>"
            return errors

    def edit_user_validator(self, postData, request):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 1:
            errors["first_name"] = "<div class='ohno'>First name required</div>"
        else:
            if not NAME_REGEX.match(postData['first_name']):
                errors["first_name"] = "<div class='ohno'>First name must contain only letters</div>"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "<div class='ohno'>Last name required</div>"
        else:
            if not NAME_REGEX.match(postData['last_name']):
                errors["last_name"] = "<div class='ohno'>Last name must contain only letters</div>"
        if len(postData['email']) < 1:
            errors["email"] = "<div class='ohno'>Email required</div>"
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors["email"] = "<div class='ohno'>Must enter valid email</div>"
        if request.session['username'] == postData['email']:
            pass
        else:
            try:
                User.objects.get(email=postData['email'])
                errors['email'] = "<div class='ohno'>Email already registered</div>"
            except:
                pass
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    birthdate = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __repr__(self):
        return f"ID: {self.id}, First Name: {self.first_name}, Last Name: {self.last_name}, Email: {self.email}"

def get_image_path(instance, filename):
    return os.path.join('recipe_picture', str(instance.id), filename)

class RecipeManager(models.Manager):
    def add_recipe_validate (self, postData):
        RECIPE_REGEX = re.compile(r'^[a-zA-Z0-9.?!-]+$')
        if len(postData['preptime']) < 1:
            errors["preptime"] = "<div class='ohno'>Prep time required</div>"
        if len(postData['cook_time']) < 1:
            errors["preptime"] = "<div class='ohno'>Cook time required</div>"
        if len(postData['number_of_servings']) < 1:
            errors["number_of_servings"] = "<div class='ohno'>Cook time required</div>"
        if len(postData['title']) < 1:
            errors["title"] = "<div class='ohno'>Title required</div>"
        else:
            if not RECIPE_REGEX.match(postData['title']):
                errors["title"] = "<div class='ohno'>Title contains symbols that are not allowed. Allowed symbols are [.?!-]</div>"
        if len(postData['description']) < 1:
            errors["description"] = "<div class='ohno'>Description required</div>"
        else:
            if not RECIPE_REGEX.match(postData['description']):
                errors["description"] = "<div class='ohno'>Description contains symbols that are not allowed. Allowed symbols are [.?!-]</div>"
        if len(postData['ingredients']) < 1:
            errors["ingredients"] = "<div class='ohno'>Ingredients required</div>"
        else:
            if not RECIPE_REGEX.match(postData['ingredients']):
                errors["ingredients"] = "<div class='ohno'>Ingredients contains symbols that are not allowed. Allowed symbols are [.?!-]</div>"
        if len(postData['directions']) < 50:
            errors["directions"] = "<div class='ohno'>Please enter more detailed directions</div>"
        else:
            if not RECIPE_REGEX.match(postData['directions']):
                errors["directions"] = "<div class='ohno'>Directions contains symbols that are not allowed. Allowed symbols are [.?!-]</div>"
        return errors

class Recipe(models.Model): 
    recipe_picture = models.ImageField(upload_to='images/')
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    number_of_servings = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    directions = models.TextField()
    objects = RecipeManager()

# class category(models.Model):
#     world_cuisine = "WC"
#     cooking_style = "CS"
#     diet = "DI"
#     season = "SS"

# class world_cuisine(models.Model):
#     north_american = "NA"
#     south_american = "SA"
#     australian = "AU"
#     asian = "AS"
#     european = "EU"

# class cooking_style(models.Model):
#     vegan = "vegan"
#     vegetarian = "vegetarian"
#     slow_cooker = "slow_cooker"
#     quick_and_easy = "quick_and_easy"

# class diet(models.Model):
#     diabetic = "diabetic"
#     gluten free = "gluten free"
    

#     YEAR_IN_SCHOOL_CHOICES = [
#     ('FR', 'Freshman'),
#     ('SO', 'Sophomore'),
#     ('JR', 'Junior'),
#     ('SR', 'Senior'),
# ]