from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Group
from .forms import GroupForm


@login_required(login_url='/login/')
def group_list(request):
    # Groups the user owns or is a member of
    groups_owned = Group.objects.filter(owner=request.user)
    groups_member = Group.objects.filter(
        members=request.user).exclude(owner=request.user)

    context = {
        'groups_owned': groups_owned,
        'groups_member': groups_member,
    }
    return render(request, 'groups/group_list.html', context)


@login_required(login_url='/login/')
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            form.save_m2m()  # save members
            return redirect('group_list')
    else:
        form = GroupForm()

    return render(request, 'groups/group_form.html', {'form': form})


@login_required(login_url='/login/')
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # to restrict visibility:
    # if request.user != group.owner and request.user not in group.members.all():
    #     return redirect('group_list')

    return render(request, 'groups/group_detail.html', {'group': group})
