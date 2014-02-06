# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from forms import UserNameEditForm, AccountEditForm, OtherInfoEditForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import auth
import MySQLdb
from votune.models import Account


@login_required
def index(request):
    return render_to_response('establishment/index.html', 
                              {'user': request.user},
                              context_instance=RequestContext(request))


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/establishment')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        nextTo = request.GET.get('next', '')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(nextTo)
        else:
            error = "Please sign in"
            messages.add_message(request, messages.ERROR, 'Login failed, try again!')
            return render_to_response('establishment/login.html', {'error': error},
                                      context_instance=RequestContext(request))

    return render_to_response('establishment/login.html', {}, context_instance=RequestContext(request))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/establishment')


@login_required
def editUserName(request):
    form = UserNameEditForm(instance=request.user)
    if 'ok' in request.POST:
        form = UserNameEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form = UserNameEditForm(request.POST, instance=request.user)
            form.username = MySQLdb.escape_string(request.POST['username'])
            form.save()
            return HttpResponse(status=201)

    return render_to_response("establishment/accounts/change_username.html",
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required
def editOther(request):
    usrAccount = Account.getByID(request.user)
    form = OtherInfoEditForm(instance=usrAccount)

    if 'ok' in request.POST:
        print("Submitted")
        form = OtherInfoEditForm(request.POST, instance=usrAccount)
        if form.is_valid():
            form.company = MySQLdb.escape_string(request.POST['company'])
            form.address = MySQLdb.escape_string(request.POST['address'])
            form.postal_code = MySQLdb.escape_string(request.POST['postal_code'])
            form.phone = MySQLdb.escape_string(request.POST['phone'])
            form.save()
            return HttpResponse(status=201)
    return render_to_response("establishment/accounts/edit_other.html",
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required
def editAccountInfo(request):
    form = AccountEditForm(instance=request.user)

    if 'ok' in request.POST:
        form = AccountEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.firstName = MySQLdb.escape_string(request.POST['first_name'])
            form.last_name = MySQLdb.escape_string(request.POST['last_name'])
            form.email = MySQLdb.escape_string(request.POST['email'])
            form.save()
            return HttpResponse(status=201)

    return render_to_response("establishment/accounts/edit_account.html",
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required
def changePassword(request):
    form = PasswordChangeForm()
    if 'ok' in request.POST:
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            u = User.objects.get(username=request.user)
            password1 = request.POST.get('confirm_password', '')
            u.set_password(password1)
            u.save()
            return HttpResponse(status=201)

    return render_to_response("establishment/accounts/change_password.html",
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required
def editAccount(request):
    accountEditForm = AccountEditForm(instance=request.user)
    usernameEditForm = UserNameEditForm(instance=request.user)
    usrAccount = Account.getByID(request.user)
    otherInfoEditForm = OtherInfoEditForm(instance=usrAccount)
    passwordChangeForm = PasswordChangeForm()

    if request.method == 'POST' and 'account_update' in request.POST:
        accountEditForm = AccountEditForm(request.POST, instance=request.user)
        if accountEditForm.is_valid():
            accountEditForm.firstName = MySQLdb.escape_string(request.POST['first_name'])
            accountEditForm.last_name = MySQLdb.escape_string(request.POST['last_name'])
            accountEditForm.email = MySQLdb.escape_string(request.POST['email'])
            accountEditForm.save()
            messages.add_message(request, messages.INFO, 'Account was successfully updated.')
            return HttpResponseRedirect('')

    elif request.method == 'POST' and 'username_update' in request.POST:
        usernameEditForm = UserNameEditForm(request.POST, instance=request.user)
        if usernameEditForm.is_valid():
            usernameEditForm.username = MySQLdb.escape_string(request.POST['username'])
            usernameEditForm.save()
            messages.add_message(request, messages.INFO, 'Username was successfully updated.')
            return HttpResponseRedirect('/establishment')

    elif request.method == 'POST' and 'other_info_update' in request.POST:
        otherInfoEditForm = OtherInfoEditForm(request.POST, instance=usrAccount)
        if otherInfoEditForm.is_valid():
            otherInfoEditForm.company = MySQLdb.escape_string(request.POST['company'])
            otherInfoEditForm.address = MySQLdb.escape_string(request.POST['address'])
            otherInfoEditForm.postal_code = MySQLdb.escape_string(request.POST['postal_code'])
            otherInfoEditForm.phone = MySQLdb.escape_string(request.POST['phone'])
            otherInfoEditForm.save()
            messages.add_message(request, messages.INFO, 'Username was successfully updated.')
            return HttpResponseRedirect('/establishment')

    elif request.method == 'POST' and 'password_update' in request.POST:
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('confirm_password', '')

        if password1 != password2:
            messages.add_message(request, messages.ERROR, 'Password did not match.')
            return HttpResponseRedirect('')
        elif len(password1) < 4:
            messages.add_message(request, messages.ERROR, 'Password too short.')
            return HttpResponseRedirect('')
        else:
            u = User.objects.get(username=request.user)
            u.set_password(password1)
            u.save()
            messages.add_message(request, messages.INFO, 'Password successfully updated')
            return HttpResponseRedirect('/establishment')

    return render_to_response('establishment/edit_account.html',
                              {
                                  'accountEditForm': accountEditForm,
                                  'usernameEditForm': usernameEditForm,
                                  'otherInfoEditForm': otherInfoEditForm,
                                  'passwordChangeForm': passwordChangeForm},
                              context_instance=RequestContext(request))
