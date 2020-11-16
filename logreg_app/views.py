from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, PostMessage, Comment

def index(request):
    return render(request, 'index.html')

def success(request):
    if "user_id" not in request.session:
        return redirect('/')
    context={
        'all_messages':PostMessage.objects.all()
    }
    return render(request, 'success.html', context)

def register(request):
    if request.method =="POST":
        errors=User.objects.validate_user(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        # encypt password
        # store plain text pw in variable
        user_pw=request.POST['password']
        # hash password
        hash_pw=bcrypt.hashpw(user_pw.encode(),bcrypt.gensalt()).decode()
        # test
        print(hash_pw)
        new_user=User.objects.create(
            f_name=request.POST['f_name'],
            l_name=request.POST['l_name'],
            email=request.POST['email'],
            password=hash_pw,
        )

        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.f_name} {new_user.l_name}"
        return redirect('/success')
        # return redirect('/success/{new_user.id}')
    return redirect('/')

def login (request):
    if request.method=='POST':
        log_user=User.objects.filter(email=request.POST['email'])
        if log_user:
            log_user=log_user[0]
            # if log_user.password == request.POST['password']:
            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['user_id']=log_user.id
                request.session['user_name']=f"{log_user.f_name} {log_user.l_name}"
                return redirect('/success')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

# Dashboard 

# CREATE

def create_message(request):
    if request.method=="POST":
        error=PostMessage.objects.empty_valadator(request.POST)
        if error:
            messages.error(request, error)
            return redirect('/success')
        PostMessage.objects.create(content=request.POST['message'], poster=User.objects.get(id=request.session["user_id"]))
        return redirect('/success')
    return redirect('/')

def create_comment(request):
    if request.method=='POST':
        Comment.objects.create(content=request.POST['comment'], poster=User.objects.get(id=request.session["user_id"]), message=PostMessage.objects.get(id=request.POST['message']))
        return redirect('/success')
    return redirect('/')



# READ

def profile(request, user_id):
    context={
        'user':User.objects.get(id=user_id)
    }
    return render(request, "profile.html", context)

# DESTROY

def delete_wallpost(request, message_id):
    PostMessage.objects.get(id=message_id).delete()
    return redirect('/success')

def delete_comm(request, comment_id):
    Comment.objects.get(id=comment_id).delete()
    return redirect('/success')


