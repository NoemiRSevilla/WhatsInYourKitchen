from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
import re
import bcrypt
import os


def LengthGreaterThanOne(value):
    if len(value) < 1:
        raise ValidationError(
            '{} required'.format(value)
        )

def LengthGreaterThanEight(value):
    if len(value) < 8:
        raise ValidationError(
            '{} must be longer than: 8'.format(value)
        )

def LengthGreaterThanTen(value):
    if len(value) < 10:
        raise ValidationError(
            '{} must be longer than: 10'.format(value)
        )

def NameMatchforRegex(value):
    NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
    if not NAME_REGEX.match(value):
        raise ValidationError(
            '{} must contain only letters'.format(value)
        )

def OlderThanThirteen(value):
    birthdate = datetime.strptime(value, "%Y-%m-%d")
    present = datetime.now()
    if ((present - birthdate).days/365 < 13):
        raise ValidationError(
            '{} must be 13 years of age to register'.format(value)
        )

def EmailRegexMatch(value):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(value):
        raise ValidationError(
            '{} must contain valid email'.format(value)
        )

def StringAndCertainSymbols(value):
    STRING_REGEX = re.compile(r'^[a-zA-Z0-9.?!-]+$')
    if not STRING_REGEX.match(value):
        raise ValidationError(
            '{} can only contain letters and [.?!-]'.format(value)
        )

def GreaterThanEight(value):
    if len(value) < 8:
        raise ValidationError(
            '{} must be longer than: 8'.format(value)
        )

def AlreadyReadyRegistered(value):
    try:
        User.objects.get(email=postData['email'])
        raise ValidationError(
            '{} already registered'.format(value)
        )
    except:
        pass

def ConfirmPassword(value):
    if postData['confirmpassword'] != postData['password']:
        raise ValidationError(
            '{} must match'.format(value)
        )
def UserExists(value):
    try:
        user = User.objects.get(email=postData['email'])
    except:
        raise ValidationError(
            '{} could not be logged in'.format(value)
        )

def PasswordMatch(value):
    if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
        pass
    else:
        raise ValidationError(
            '{} could not be logged in'.format(value)
        )

def NoNegatives(value):
    if value < 0:
        raise ValidationError(
            '{} no negatives'.format(value)
        )

# def basic_validator(self, postData):
#     EMAIL_REGEX = re.compile(
#         r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#     NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
#     bcrypt.hashpw('test'.encode(), bcrypt.gensalt())
#         if not NAME_REGEX.match(postData['first_name']):
#             raise ValidationError(
#                 '{} must contain only letters'.format(value)
#         )
#     if len(postData['last_name']) < 2:
#         raise ValidationError(
#             '{} must be longer than: 2'.format(value)
#         )
#     else:
#         if not NAME_REGEX.match(postData['last_name']):
#             raise ValidationError(
#                 '{} must contain only letters'.format(value)
#             )
#     if len(postData['email']) < 1:
#         raise ValidationError(
#             '{} must be longer than: 2'.format(value)
#         )
#     else:
#         if not EMAIL_REGEX.match(postData['email']):
#             raise ValidationError(
#                 '{} must contain valid email'.format(value)
#             )
#     if len(postData['birthdate']) < 1:
#         raise ValidationError(
#             '{} required'.format(value)
#         )
#     else:
#         birthdate = datetime.strptime(postData['birthdate'], "%Y-%m-%d")
#         present = datetime.now()
#         if ((present - birthdate).days/365 < 13):
#             raise ValidationError(
#                 '{} must be 13 years of age to register'.format(value)
#             )
#     try:
#         User.objects.get(email=postData['email'])
#         raise ValidationError(
#             '{} already registered'.format(value)
#         )
#     except:
#         pass
#     if len(postData['password']) < 1:
#         raise ValidationError(
#             '{} required'.format(value)
#         )
#     else:
#         if len(postData['password']) < 8:
#             raise ValidationError(
#                 '{} must be longer than: 8'.format(value)
#             )
#     if postData['confirmpassword'] != postData['password']:
#         raise ValidationError(
#             '{} must match'.format(value)
#         )
#     return errors
# def login_validator(self, postData):
#     errors = {}
#     try:
#         user = User.objects.get(email=postData['email'])
#     except:
#         raise ValidationError(
#             '{} could not be logged in'.format(value)
#         )
#     if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
#         return errors
#     else:
#         raise ValidationError(
#             '{} could not be logged in'.format(value)
#         )
#         return errors

# def edit_user_validator(self, postData, request):
#     EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#     NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
#     errors = {}
#     if len(postData['first_name']) < 1:
#         raise ValidationError(
#             '{} must be longer than: 1'.format(value)
#         )
#     else:
#         if not NAME_REGEX.match(postData['first_name']):
#             raise ValidationError(
#                 '{} must contain only letters'.format(value)
#             )
#     if len(postData['last_name']) < 1:
#         raise ValidationError(
#             '{} required'.format(value)
#         )
#     else:
#         if not NAME_REGEX.match(postData['last_name']):
#             raise ValidationError(
#                 '{} must contain only letters'.format(value)
#             )
#     if len(postData['email']) < 1:
#         raise ValidationError(
#             '{} required'.format(value)
#         )
#     else:
#         if not EMAIL_REGEX.match(postData['email']):
#             raise ValidationError(
#                 '{} must contain valid email'.format(value)
#             )
#     if request.session['username'] == postData['email']:
#         pass
#     else:
#         try:
#             User.objects.get(email=postData['email'])
#             raise ValidationError(
#                 '{} already registered'.format(value)
#             )
#         except:
#             pass
#     return errors

# class CommentManager(models.Manager):
#     def message_validation(self, postData):
#         errors = {}
#         if len(postData['comment']) < 1:
#             errors["comment"] = "<div class='ohno'>Comment required</div>"
#             return errors
#         if len(request.FILES)!= 0:
#             data = request.FILES

    
class User(models.Model):
    first_name = models.CharField(max_length=100, validators = [LengthGreaterThanOne, NameMatchforRegex])
    last_name = models.CharField(max_length=100, validators = [LengthGreaterThanOne, NameMatchforRegex])
    email = models.CharField(max_length=100, validators = [LengthGreaterThanOne, EmailRegexMatch, AlreadyReadyRegistered])
    birthdate = models.DateField(validators = [LengthGreaterThanOne, OlderThanThirteen])
    password = models.CharField(max_length=255, validators =[LengthGreaterThanOne, LengthGreaterThanEight, ConfirmPassword])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # objects = UserManager()

    def __repr__(self):
        return f"ID: {self.id}, First Name: {self.first_name}, Last Name: {self.last_name}, Email: {self.email}"

class Comment(models.Model):
    # comment_picture = models.ImageField(upload_to = 'images/')
    uploaded_by = models.ForeignKey(User, related_name ="comment_uploaded")
    comment = models.TextField(validators = [LengthGreaterThanOne, LengthGreaterThanTen, StringAndCertainSymbols])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    users_who_like = models.ManyToManyField(User, related_name="liked_comments")

class Message(models.Model):
    # message_picture = models.ImageField(upload_to = 'images/')
    uploaded_message_by = models.ForeignKey(User, related_name ="message_uploaded")
    users_who_like = models.ManyToManyField(User, related_name="liked_message")
    comments_for_message = models.ForeignKey(Comment, related_name ="message_to_comment")
    message = models.TextField(validators = [LengthGreaterThanOne, LengthGreaterThanTen, StringAndCertainSymbols])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # objects = MessageManager()


def get_image_path(instance, filename):
    return os.path.join('recipe_picture', str(instance.id), filename)

class Recipe(models.Model): 
    recipe_picture = models.ImageField(upload_to='images/')
    uploaded_by = models.ForeignKey(User, related_name ="recipe_uploaded")
    users_who_like = models.ManyToManyField(User, related_name="liked_recipe")
    prep_time = models.IntegerField(validators = [LengthGreaterThanOne, NoNegatives])
    cook_time = models.IntegerField(validators = [LengthGreaterThanOne, NoNegatives])
    number_of_servings = models.IntegerField(validators = [LengthGreaterThanOne, NoNegatives])
    title = models.CharField(max_length=100, validators = [LengthGreaterThanOne, StringAndCertainSymbols])
    description = models.TextField(validators = [LengthGreaterThanOne, LengthGreaterThanTen, StringAndCertainSymbols])
    ingredients = models.TextField(validators = [LengthGreaterThanOne, StringAndCertainSymbols])
    directions = models.TextField(validators = [LengthGreaterThanOne, LengthGreaterThanTen, StringAndCertainSymbols])
    categories = models.TextField(validators = [LengthGreaterThanOne, StringAndCertainSymbols])
    messages_for_recipe = models.ForeignKey(Message, related_name ="recipe_with_messages")
    comments_for_recipe = models.ForeignKey(Comment, related_name ="recipe_with_comments")
    # objects = RecipeManager()


# class RecipeManager(models.Manager):
#     def add_recipe_validate (self, postData):
#         RECIPE_REGEX = re.compile(r'^[a-zA-Z0-9.?!-]+$')
#         errors = {}
#         if len(postData['preptime']) < 1:
#             raise ValidationError(
#                 '{} required'.format(value)
#             )
#         if len(postData['cook_time']) < 1:
#             raise ValidationError(
#                 '{} required'.format(value)
#             )
#         if len(postData['number_of_servings']) < 1:
#             raise ValidationError(
#                 '{} required'.format(value)
#             )
#         if len(postData['title']) < 1:
#             raise ValidationError(
#                 '{} required'.format(value)
#             )
#         else:
#             if not RECIPE_REGEX.match(postData['title']):
#                 raise ValidationError(
#                     '{} only allowed symbols can be accepted [.?!-]'.format(value)
#                 )
#         if len(postData['description']) < 1:
#             raise ValidationError(
#                 '{} required'.format(value)
#             )
#         else:
#             if not RECIPE_REGEX.match(postData['description']):
#                 raise ValidationError(
#                     '{} only allowed symbols can be accepted [.?!-]'.format(value)
#                 )
#         if len(postData['ingredients']) < 1:
#             raise ValidationError(
#                 '{} required'.format(value)
#             )
#         else:
#             if not RECIPE_REGEX.match(postData['ingredients']):
#                 raise ValidationError(
#                     '{} only allowed symbols can be accepted [.?!-]'.format(value)
#                 )
#         if len(postData['directions']) < 50:
#             raise ValidationError(
#                 '{} must be longer than : 50[.?!-]'.format(value)
#             )
#         else:
#             if not RECIPE_REGEX.match(postData['directions']):
#                 errors["directions"] = "<div class='ohno'>Directions contains symbols that are not allowed. Allowed symbols are [.?!-]</div>"
#         return errors
# class MessageManager(models.Manager):
#     def message_validation(self, postData):
#         errors = {}
#         if len(postData['message']) < 1:
#             errors["message"] = "<div class='ohno'>Message required</div>"

# class Message(models.Model):
#     message_picture = models.ImageField(upload_to = 'images/')
#     uploaded_message_by = models.ForeignKey(User, related_name ="message_uploaded")
#     users_who_like = models.ManyToManyField(User, related_name="liked_message")
#     comments_for_message = models.ForeignKey(Comment, related_name ="message_to_comment")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
    # objects = MessageManager()




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