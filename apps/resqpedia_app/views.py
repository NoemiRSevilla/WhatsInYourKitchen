from django.shortcuts import render, redirect
from . import models
from .models import User
from django.contrib import messages
import bcrypt
from datetime import datetime

from .forms import RegisterUser, EditUser, AddRecipe, EditRecipe, AddMessage, EditMessage, AddComment, EditComment


def index(request):
    if "username" in request.session:
        return redirect("/resqpedia")
    else:
        context = {
            "RegisterUser": RegisterUser()
        }
        return render(request, "index.html", context)


def register(request):
    if request.method == "POST":
        bound_form = RegisterUser(request.POST)
        # Now test that bound_form using built-in methods!
        # *************************
        # True or False, based on the validations that were set!
        print(bound_form.is_valid())
        print(bound_form.errors)
        hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                            email=request.POST['email'], birthdate=datetime.strptime(request.POST['birthdate'], '%Y-%m-%d'), password=hash)
        request.session['username'] = request.POST['email']
        return redirect("/resqpedia")


def checklogin(request):
    errors = {}
    if "username" not in request.session:
        errors['email'] = "<div class='ohno'>Please log in</div>"
        return False
    return True


def login(request):
    bound_form = LoginUser(request.POST)
    request.session['username'] = request.POST['email']
    return redirect("/resqpedia")


def logout(request):
    if "username" in request.session:
        del request.session["username"]
    if "email" in request.session:
        del request.session["email"]
    if "first_name" in request.session:
        del request.session["first_name"]
    if "last_name" in request.session:
        del request.session["last_name"]
    return redirect("/")


def all_recipes(request):
    context = {
        "EditUser": EditUser(),
        "all_recipes": Recipe.objects.all
    }
    return render(request, "allrecipes.html", context)

def show_user_info(request):
    return render (request, 'show_user_info.html')

def edit_user(request):
    if request.method == "GET":
        context = {
            "EditUser": EditUser()
        }
        return render("edituser.html")
    if request.method == 'POST':
        bound_form = EditUser(request.POST)
        # Now test that bound_form using built-in methods!
        # *************************
        # True or False, based on the validations that were set!
        print(bound_form.is_valid())
        print(bound_form.errors)
        user = User.objects.get(email=request.session['username'])
        if request.method == "POST":
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                if len(request.POST['first_name']) > 0:
                    user.first_name = request.POST['first_name']
                    request.session['first_name'] = user.first_name
                else:
                    pass
                if len(request.POST['last_name']) > 0:
                    user.first_name = request.POST['last_name']
                    user.last_name = request.POST['last_name']
                else:
                    pass
                if len(request.POST['email']) > 0:
                    user.email = request.POST['email']
                    user = User.objects.get(email=request.session['username'])
                else:
                    pass
                if len(request.POST['password']) >= 1:
                    if (request.POST['password'] == request.POST['confirm_password']):
                        hash1=bcrypt.hashpw(
                            request.POST["newpassword"].encode(), bcrypt.gensalt())
                        user.password=hash1
                    else: pass
                    user.save()
                else:
                    messages.error(request, "Previous password is incorrect")
                return redirect(f'/resqpedia/myaccount/{user_id}/edit')


def add_recipe(request, recipe_id):
    if request.method == "GET":
        context={
            "user_info": User.objects.get(email=request.session['username']),
            "AddRecipe": AddRecipe(),
        }
        return render(request, "addrecipe.html")
    if request.method == "POST":
        errors=Recipe.objects.add_recipe_validate(request.POST)
        if errors:
            request.session['title']=request.POST['title']
            request.session['description']=request.POST['description']
            request.session['ingredients']=request.POST['ingredients']
            request.session['directions']=request.POST['directions']
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/resqpedia/addrecipe")
        else:
            uploaded_by=User.objects.get(id=int(request.POST['uploaded_by']))
            new_recipe=Recipe.objects.create(prep_time=request.POST['prep_time'], cook_time=request.POST['cook_time'], number_of_servings=request.POST[
                                               'number_of_servings'], title=request.POST['title'], ingredients=request.POST['ingredients'], directions=request.POST['directions'])
            new_recipe.users_who_like.add(uploaded_by)
            return redirect(f"resqpedia/recipe/{recipe_id}")

def show_individual_recipe(request, recipe_id):
    if request.method == "GET":
        context={
            "current_recipe": Recipe.objects.get(id=recipe_id),
        }
        return render("show_individual_recipe.html")

def edit_recipe(request, recipe_id):
    if request.method == "GET":
        context={
            "current_recipe": Recipe.objects.get(id=recipe_id),
            "EditRecipe": EditRecipe()
        }
        return render("updatepageofuser.html")
    if request.method == 'POST':
        # current_recipe.recipe_picture = request.POST['pic']
        current_recipe.prep_time=request.POST['prep_time']
        current_recipe.cook_time=request.POST['cook_time']
        current_recipe.number_of_servings=request.POST['number_of_servings']
        current_recipe.directions=request.POST['directions']
        current_recipe.ingredients - request.POST['ingredients']
        current_recipe.save()
        return redirect('/homepage')  # redirect to show user info

def add_message(request, message_id):
    if request.method == "GET":
        context={
            "user_info": User.objects.get(email=request.session['username']),
            "recipe_info": User.objects.get(id=recipe_id),
            "AddMessage": AddMessage()
        }
        return render(request, "addmessage.html", context)
    if request.method == "POST":
        errors=Message.objects.add_message(request.POST)
        if errors:
            request.session['message']=request.POST['message']
            request.session['message_picture']=request.POST['message_picture']
            for key, value in errors.items():
                message.error(request, value)
            return redirect(f"resqpedia/recipe/{recipe_id}")
        else:
            uploaded_by=User.objects.get(id=int(request.POST['uploaded_by']))
            recipe_id=User.objects.get(id=int(request.POST[recipe_id]))
            new_message=Message.objects.create()
            new_recipe.users_who_like.add(uploaded_by)
            return redirect(f"/resqpedia/recipe/{recipe_id}")

def edit_message(request, message_id):
    if request.method == 'POST':
        edit_message = Message.objects.get(id=message_id)
        if edit_message.uploaded_message_by.email == request.session['username']:
            edit_message.message = request.POST['newmessage']
            edit_message.save()
    return redirect(f'/resqpedia/recipe/edit_message/{message_id}')

def add_comment(request, recipe_id):
    if request.method == "GET":
        context={
            "user_info": User.objects.get(email=request.session['username']),
            "recipe_info": User.objects.get(id=recipe_id),
            "AddMessage": AddMessage()
        }
        return render(request, "addmessage.html", context)
    if request.method == "POST":
        errors=Message.objects.add_message(request.POST)
        if errors:
            request.session['message']=request.POST['message']
            request.session['message_picture']=request.POST['message_picture']
            for key, value in errors.items():
                message.error(request, value)
            return redirect(f"resqpedia/recipe/{recipe_id}")
        else:
            uploaded_by=User.objects.get(id=int(request.POST['uploaded_by']))
            recipe_id=User.objects.get(id=int(request.POST[recipe_id]))
            new_message=Message.objects.create()
            new_recipe.users_who_like.add(uploaded_by)
            return redirect(f"/resqpedia/recipe/{recipe_id}")

def update_comment(request, comment_id):
    if request.method == 'POST':
        edit_comment = Comment.objects.get(id=comment_id)
        if edit_comment.uploaded_comment_by.email == request.session['username']:
            edit_comment.comment = request.POST['newcomment']
            edit_comment.save()
        return redirect('/resqpedia/recipe/edit_comment/<comment_id>')
    
def delete_message(request, message_id):
    delete_message = Message.objects.get(id=message_id)
    delete_message.uploaded_message_by.email == request.session['username']
    delete_message.delete()
    return redirect('/')

def delete_comment(request, comment_id):
    delete_comment = Comment.objects.get(id=comment_id)
    delete_comment.uploaded_comment_by.email == request.session['username']
    delete_comment.delete()
    return redirect('/')
# def addmessage(request):
#     if request.method == "GET":
#         context = {
#             "user_info": User.objects.get(email=request.session['username'])
#         }
#         return render(request, "showpageofrecipe.html")
#     if request.method == "POST":

def delete_recipe(request, recipe_id):
    delete_recipe=Recipe.objects.get(id=recipe_id)
    delete_recipe.delete()
    return redirect('/homepage')


def delete_user(request):
    user=User.objects.get(email=request.session['username'])
    user.delete()
    return redirect('/')  # return to loginpage
