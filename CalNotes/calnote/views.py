from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
from calendar import monthrange, month_abbr
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from markdown2 import Markdown
from math import ceil

from .models import Task, Event, Note		# Imports class Task from models.py
# Imports forms from forms.p
from .forms import TaskForm, EventForm, NoteForm

markdowner = Markdown()

def index(request):
    """Main view: shows the task listing by default."""

    # Parse date URL query
    date_query = request.GET.get('date')
    if date_query is None:
        selected_date = datetime.today()
    else:
        selected_date = datetime.strptime(date_query, "%Y-%m-%d")

    date_start = selected_date.replace(hour=0, minute=0, second=0)
    date_end = selected_date.replace(hour=23, minute=59, second=59)

    calendar_month_str = selected_date.strftime("%B")
    calendar_year_str = selected_date.strftime("%Y")
    calendar_prev_month_idx = (selected_date.month-2) % 12 + 1
    calendar_next_month_idx = (selected_date.month) % 12 + 1
    calendar_prev_month = month_abbr[calendar_prev_month_idx]
    calendar_next_month = month_abbr[calendar_next_month_idx]

    _, calendar_days = monthrange(selected_date.year, selected_date.month)
    offset = datetime.strptime(
        "%d-%d-1" % (selected_date.year, selected_date.month),
        "%Y-%m-%d"
    ).weekday()

    month_events = Event.objects.filter(
        date__gte=date_start.replace(day=1),
        date__lte=date_end.replace(day=calendar_days)).order_by('eventID')
    has_event = {}
    for event in month_events:
        has_event[event.date.day-1] = True

    calendar_month_range = [
        [
            (week*7+day-offset+1, has_event.get(week*7+day-offset, False))
            for day in range(7)
        ]
        for week in range(ceil((offset+calendar_days)/7))
    ]

    task_list = Task.objects.order_by('taskID')
    event_list = Event.objects.filter(
        date__gte=date_start, date__lte=date_end).order_by('eventID')

    context = {
        'task_list': task_list,
        'empty_task_list': len(task_list) == 0,
        'len_incomplete_task_list': len([task for task in task_list if not task.isComplete]),
        'len_complete_task_list': len([task for task in task_list if task.isComplete]),

        # Calendar contexts
        'calendar_month_str': calendar_month_str,
        'calendar_month': selected_date.month,
        'calendar_year': selected_date.year,
        'calendar_year_str': calendar_year_str,
        'calendar_month_range': calendar_month_range,
        'calendar_days': calendar_days,
        'calendar_selected': selected_date.day,
        'calendar_today': datetime.today().strftime("%Y-%m-%d"),
        'calendar_prev_month': calendar_prev_month,
        'calendar_next_month': calendar_next_month,
        'event_list': event_list,
        'calendar_prev_month_idx': calendar_prev_month_idx,
        'calendar_next_month_idx': calendar_next_month_idx,
        'has_event': has_event
    }
    return render(request, "calnote/index.html", context)

def viewNotes(request):
    """Notes View"""

    # Parse date URL query
    date_query = request.GET.get('date')
    if date_query is None:
        selected_date = datetime.today()
    else:
        selected_date = datetime.strptime(date_query, "%Y-%m-%d")

    date_start = selected_date.replace(hour=0, minute=0, second=0)
    date_end = selected_date.replace(hour=23, minute=59, second=59)

    calendar_month_str = selected_date.strftime("%B")
    calendar_year_str = selected_date.strftime("%Y")
    calendar_prev_month_idx = (selected_date.month-2) % 12 + 1
    calendar_next_month_idx = (selected_date.month) % 12 + 1
    calendar_prev_month = month_abbr[calendar_prev_month_idx]
    calendar_next_month = month_abbr[calendar_next_month_idx]

    _, calendar_days = monthrange(selected_date.year, selected_date.month)
    offset = datetime.strptime(
        "%d-%d-1" % (selected_date.year, selected_date.month),
        "%Y-%m-%d"
    ).weekday()

    month_events = Event.objects.filter(
        date__gte=date_start.replace(day=1),
        date__lte=date_end.replace(day=calendar_days)).order_by('eventID')
    has_event = {}
    for event in month_events:
        has_event[event.date.day-1] = True

    calendar_month_range = [
        [
            (week*7+day-offset+1, has_event.get(week*7+day-offset, False))
            for day in range(7)
        ]
        for week in range(ceil((offset+calendar_days)/7))
    ]

    note_list = Note.objects.order_by('noteID')
    event_list = Event.objects.filter(
        date__gte=date_start, date__lte=date_end).order_by('eventID')
    context = {
        'note_list': note_list,
        'empty_note_list': len(note_list) == 0,

       # Calendar contexts
        'calendar_month_str': calendar_month_str,
        'calendar_month': selected_date.month,
        'calendar_year': selected_date.year,
        'calendar_year_str': calendar_year_str,
        'calendar_month_range': calendar_month_range,
        'calendar_days': calendar_days,
        'calendar_selected': selected_date.day,
        'calendar_today': datetime.today().strftime("%Y-%m-%d"),
        'calendar_prev_month': calendar_prev_month,
        'calendar_next_month': calendar_next_month,
        'event_list': event_list,
        'calendar_prev_month_idx': calendar_prev_month_idx,
        'calendar_next_month_idx': calendar_next_month_idx,
        'has_event': has_event
    }
    return render(request, "calnote/notesview.html", context)

def addNewTask(request):
    """View to add a new task"""

    # Save task inputs; adds a task to the database
    if request.method == "POST":
        addTaskForm = TaskForm(request.POST)
        if addTaskForm.is_valid():
            addTaskForm.save()		# New addtask object
        return redirect(index)

    # Display task input form
    elif request.method == "GET":
        addTaskForm = TaskForm(instance=Task())
        context = {
            'taskform': addTaskForm,
            'action': 'Add a New Task'
        }
        return render(request, "calnote/taskform.html", context)

def deleteTask(request, task_id):
    """View to remove an existing task"""

    task = Task.objects.get(taskID=task_id)
    task.delete()									# Remove Task from database
    return redirect(index)

def toggleTask(request, task_id):
    """View to mark or unmark task as complete"""

    task = Task.objects.get(taskID=task_id)
    if not task.isComplete:
        task.isComplete = True
    else:
        task.isComplete = False
    task.save()
    return redirect(index)

def editTask(request, task_id):
    """View to edit a task"""

    task = Task.objects.get(taskID=task_id)
    if request.method == "POST":
        editTaskForm = TaskForm(request.POST or None, instance=task)
        if editTaskForm.is_valid():
            editTaskForm.save()
        return redirect(index)

    elif request.method == "GET":
        context = {
            'taskform': TaskForm(instance=task),
            'action': 'Edit Existing Task'
        }
        return render(request, "calnote/taskform.html", context)

def addNewEvent(request):
    """View to add a new event"""

    # Save event inputs; adds an event to the database
    if request.method == "POST":
        addEventForm = EventForm(request.POST)
        if addEventForm.is_valid():
            addEventForm.save()		            # New addEvent object
        return redirect(index)

        # Display task input form
    elif request.method == "GET":
        addEventForm = EventForm(instance=Event())
        context = {
            'eventform': addEventForm,
            'action': 'Add Event'
        }
        return render(request, "calnote/eventform.html", context)

def deleteEvent(request, event_id):
    """View to remove an existing event"""

    event = Event.objects.get(eventID=event_id)
    event.delete()									# Remove Event from database
    return redirect(index)

def editEvent(request, event_id):
    """View to edit an event"""

    event = Event.objects.get(eventID=event_id)
    if request.method == "POST":
        editEventForm = EventForm(request.POST or None, instance=event)
        if editEventForm.is_valid():
            editEventForm.save()
        return redirect(index)

    elif request.method == "GET":
        context = {
            'eventform': EventForm(instance=event),
            'action': 'Edit Event'
        }
        return render(request, "calnote/eventform.html", context)

def addNewNote(request):
    """View to add a new note"""

    # Save note inputs; adds a note to the database
    if request.method == "POST":
        addNoteForm = AddNoteForm(request.POST)
        if addNoteForm.is_valid():
            new_addNote = addNoteForm.save()		# New addnote object
        return redirect(viewNotes)

        # Display note input form
    elif request.method == "GET":
        addNoteForm = AddNoteForm(instance=Note())
        context = {
            'noteform': addNoteForm
        }
        return render(request, "calnote/noteform.html", context)

def deleteNote(request, note_id):
    """View to remove an existing event"""
    note = Note.objects.get(noteID=note_id)
    note.delete()									# Remove Event from database
    return redirect(viewNotes)
  
def openNote(request, note_id):
    """View to display a single note"""

    # Parse date URL query
    date_query = request.GET.get('date')
    if date_query is None:
        selected_date = datetime.today()
    else:
        selected_date = datetime.strptime(date_query, "%Y-%m-%d")

    date_start = selected_date.replace(hour=0, minute=0, second=0)
    date_end = selected_date.replace(hour=23, minute=59, second=59)

    calendar_month_str = selected_date.strftime("%B")
    calendar_year_str = selected_date.strftime("%Y")
    calendar_prev_month_idx = (selected_date.month-2) % 12 + 1
    calendar_next_month_idx = (selected_date.month) % 12 + 1
    calendar_prev_month = month_abbr[calendar_prev_month_idx]
    calendar_next_month = month_abbr[calendar_next_month_idx]

    _, calendar_days = monthrange(selected_date.year, selected_date.month)
    offset = datetime.strptime(
        "%d-%d-1" % (selected_date.year, selected_date.month),
        "%Y-%m-%d"
    ).weekday()

    month_events = Event.objects.filter(
        date__gte=date_start.replace(day=1), date__lte=date_end.replace(day=calendar_days)).order_by('eventID')
    has_event = {}
    for event in month_events:
        has_event[event.date.day-1] = True

    calendar_month_range = [
        [
            (week*7+day-offset+1, has_event.get(week*7+day-offset, False))
            for day in range(7)
        ]
        for week in range(ceil((offset+calendar_days)/7))
    ]

    # task_list = Task.objects.order_by('taskID')
    event_list = Event.objects.filter(
        date__gte=date_start, date__lte=date_end).order_by('eventID')


    note = Note.objects.get(pk=note_id)             # Retrieve note

    if request.method == "GET":

        converted_note = markdowner.convert(note.note)

        context = {
            'title': note.noteTitle,
            'content': converted_note,

            # Calendar contexts
            'calendar_month_str': calendar_month_str,
            'calendar_month': selected_date.month,
            'calendar_year': selected_date.year,
            'calendar_year_str': calendar_year_str,
            'calendar_month_range': calendar_month_range,
            'calendar_days': calendar_days,
            'calendar_selected': selected_date.day,
            'calendar_today': datetime.today().strftime("%Y-%m-%d"),
            'calendar_prev_month': calendar_prev_month,
            'calendar_next_month': calendar_next_month,
            'event_list': event_list,
            'calendar_prev_month_idx': calendar_prev_month_idx,
            'calendar_next_month_idx': calendar_next_month_idx,
            'has_event': has_event
        }
        return render(request, "calnote/note.html", context)



def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index") #change this to what page you want after register
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    return render(request=request,
                template_name="calnote/register.html",
                context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index") #change this to what page you want after login
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
            template_name="calnote/login.html",
            context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index") #change this to what page you want after logout