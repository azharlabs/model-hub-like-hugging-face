
# Import Python
import re
import random
from datetime import datetime

# Import Django

from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Team, Invitation

from .utils import send_invitation, send_invitation_accepted

@login_required()
def team_home(request):
    team_list = Team.objects.filter(members__in=[request.user]).order_by('-created_at')
    
    context = {
        'team_list':team_list,
        
    }
    return render(request, 'scheme/teams/teams_home.html', context)


@login_required()
def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        team_title = Team.objects.filter(title=title, created_by=request.user)
        team_title_len = []
        for i in team_title:
            team_title_len.append(i.title)
        print("team_title_len======", len(team_title_len))

        if title and len(team_title_len) == 0:
            team = Team.objects.create(title=title, created_by=request.user, description=description)
            
            team.members.add(request.user)
            team.save()

            return HttpResponse('Team added')
        return HttpResponse('Team title must be unique')
    
    return HttpResponse('Something went wrong')


@login_required()
def team_detail(request, pk):
    # user = Profile.user
    team=get_object_or_404(Team, pk=pk)
    invitations = team.invitations.filter(status=Invitation.INVITED)

    context = {
        'team':team,
        'invitations':invitations,

    }

    return render(request, 'scheme/teams/team_detail.html', context)


@login_required()
def invite(request):
    

    if request.method == 'POST':
        print("post true", request.POST)
        email = request.POST.get('invite_email')
        team_pk = request.POST.get('team_pk')
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(pat,email):
            print('email true ')
            team = get_object_or_404(Team, pk=team_pk)

            if email:
                print('email true 2')
                invitations = Invitation.objects.filter(team=team,invited_by=request.user, email=email)

                print('invitations', invitations)

                if not invitations:
                    print("invitation check 4")
                    code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz123456789') for i in range(4))
                    invitation = Invitation.objects.create(team=team, email=email, invited_by=request.user,code=code)

                    messages.info(request, 'The user was invited')

                    send_invitation(email, code, team)

                    return HttpResponse('User invited Successfully')
                else:
                    return HttpResponse('The users has already been invited')
        else:
            return HttpResponse('Please Check the email')

    return HttpResponse('Oops! something went wrong')


@login_required()
def accept_invitation(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        invitations = Invitation.objects.filter(code=code, email=request.user.email)

        if invitations:
            invitation = invitations[0]
            invitation.status = Invitation.ACCEPTED
            invitation.save()

            team = invitation.team
            team.members.add(request.user)
            team.save()

            messages.info(request, 'Invitation accepted')

            send_invitation_accepted(team, invitation)

            return redirect('dashboard:teams:team_detail', pk=team.id)
        else:
            messages.info(request, 'Invitation was not found')
    else:
        return render(request, 'scheme/teams/accept_invitation.html', {})



@login_required()
def delete(request):
    context ={}
    if request.method =="POST":
        print("dict", dict(request.POST), request.POST.getlist('id'))
        for i in request.POST.getlist('id'):
            print("i=============", i)
            obj = get_object_or_404(Team, id = i)
            # delete object
            obj.delete()
        return redirect('dashboard:teams:team_home')
 
    return HttpResponse("Something went wrong")
