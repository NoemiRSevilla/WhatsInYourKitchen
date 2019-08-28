from django.shortcuts import render, redirect
from . import models
from .models import User
from django.contrib import messages
import bcrypt
from datetime import datetime


def index(request):
    if "username" in request.session:
        return redirect("/resqpedia/addrecipe")
    else:
        return render(request, "index.html")


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if errors:
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                            email=request.POST['email'], birthdate=datetime.strptime(request.POST['birthdate'], '%Y-%m-%d'), password=hash)
        request.session['username'] = request.POST['email']
        return redirect("/resqpedia/addrecipe")


def checklogin(request):
    errors = {}
    if "username" not in request.session:
        errors['email'] = "<div class='ohno'>Please log in</div>"
        return False
    return True


def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        request.session['username'] = request.POST['email']
        return redirect("/resqpedia/addrecipe")


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


def addrecipe(request):
    if request.method == "GET":
        context = {
            "user_info": User.objects.get(email=request.session['username'])
        }
        return render(request, "addrecipe.html")
    if request.method == "POST":
        errors = Recipe.objects.add_recipe_validate(request.POST)
        if errors:
            request.session['title'] = request.POST['title']
            request.session['description'] = request.POST['description']
            request.session['ingredients'] = request.POST['ingredients']
            request.session['directions'] = request.POST['directions']
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/resqpedia/addrecipe")
        else:
            uploaded_by = User.objects.get(id=int(request.POST['uploaded_by']))
            new_recipe = Recipe.objects.create(prep_time=request.POST['prep_time'], cook_time=request.POST['cook_time'], number_of_servings=request.POST[
                                               'number_of_servings'], title=request.POST['title'], ingredients=request.POST['ingredients'], directions=request.POST['directions'])
            new_recipe.users_who_like.add(uploaded_by)
            return redirect("/resqpedia/addrecipe")