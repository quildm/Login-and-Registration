from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
	return render(request, 'login_reg_app/index.html')
def success(request):
	return render(request, 'login_reg_app/success.html')

def register(request):
	errors = User.objects.validate_reg(request.POST)
	if errors:
		for tag, error in errors.iteritems():
		    messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		found_users = User.objects.filter(email=request.POST['email'])
		if found_users.count() > 0:
			# we can't register
			messages.error(request, "email already taken", extra_tags="email")
			return redirect('/')
		else:
			hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			created_user = User.objects.create(name=request.POST['name'], email=request.POST['email'], password=hashed_pw)
			request.session['user_id'] = created_user.id
			request.session['user_name'] = created_user.name
			print created_user
			return redirect('/success')
		# register the user
	return redirect('/')

def login(request):
	# check user for that email
	# then check password
	found_users = User.objects.filter(email=request.POST['email'])
	if found_users.count() > 0:
		# check passwords
		found_user = found_users.first()
		if bcrypt.checkpw(request.POST['password'].encode(), found_user.password.encode()) == True:
			# we are logged in
			request.session['user_id'] = found_user.id
			request.session['user_name'] = found_user.name
			print found_user
			return redirect('/success')
		else:
			messages.error(request, "Login Failed", extra_tags="email")
			return redirect('/')
	else:
		messages.error(request, "Login Failed", extra_tags="email")
		return redirect('/')