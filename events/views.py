from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now,localtime
from django.db.models import Q, Count
from django.contrib import messages
from .models import Event, Participant, Category
from .forms import EventModelForm, CategoryModelForm, ParticipantModelForm


def home(request):
    query = request.GET.get('q', '')
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    
    if query:
        events = events.filter(Q(name__icontains=query) | Q(location__icontains=query))

    participants = Participant.objects.annotate(event_count=Count('events')).order_by('-event_count')

    context = {
        "events": events,
        "participants": participants
    }
    return render(request, 'events/home.html', context)


def dashboard(request):
    today = now().date() 
    event_type = request.GET.get("type", "today")  

    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    participants = Participant.objects.annotate(event_count=Count('events'))
    events = Event.objects.none()

    if event_type == "today":
        events = Event.objects.filter(date=today)
    elif event_type == "total":
        events = Event.objects.all()
    elif event_type == "upcoming":
        events = Event.objects.filter(date__gte=today)
    elif event_type == "past":
        events = Event.objects.filter(date__lt=today)
    elif event_type == "participants":
        events = None 
    else:
        events = Event.objects.none()  

    context = {
        "total_participants": total_participants,
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "events": events,
        "participants": participants if event_type == "participants" else None,
        "selected_type": event_type,
    }

    return render(request, 'events/dashboard.html', context)
def event_detail(request, id):
    event = get_object_or_404(Event.objects.prefetch_related('participants'), id=id)
    context = {"event": event}  
    return render(request, 'events/event_detail.html', context)

def add_event(request):
    event_form = EventModelForm()
    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event added successfully!')
            return redirect('add_event')
    return render(request, "events/add_event.html", {"event_form": event_form})


def update_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('dashboard_o')
    else:
        event_form = EventModelForm(instance=event)
    return render(request, "events/update_event.html", {"event_form": event_form})


def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('dashboard_o')
    else:
        messages.error(request,"Something went worng")
        return redirect('dashboard_o')
    


def add_category(request):
    category_form = CategoryModelForm()
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('add_category')
    return render(request, "events/add_category.html", {"category_form": category_form})


def add_participant(request):
    participant_form = ParticipantModelForm()
    if request.method == "POST":
        participant_form = ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, 'Participant added successfully!')
            return redirect('add_participant')
    return render(request, "events/add_participant.html", {"participant_form": participant_form})
