from importlib.resources import contents
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm, EventForm
import csv
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator

###########################################################################################
# Home
###########################################################################################
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "John"
    month = month.capitalize() # allow lower/upper case
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)
    # Get current year
    now = datetime.now()
    current_year = now.year

    # Get current time
    time = now.strftime('%I:%M %p')

    return render(request, 'events/home.html',{
        "name":name,
        "year":year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
        "current_year":current_year,
        "time":time,
})

###########################################################################################
# Venue
###########################################################################################
def add_venue(request):
    submitted = False
    if request.method == "POST":
        form =  VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request,'events/add_venue.html',{
        'form':form,
        'submitted':submitted
    })

def list_venues(request):
    venue_list = Venue.objects.all().order_by('name') # grab information from models.py
    paginator = Paginator(venue_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render (request, 'events/venue.html', {'venue_list':page_obj})

def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request,'events/search_venues.html',{  
            'searched':searched,
            'venues':venues
        })
    else:
        return render(request,'events/search_venues.html',{  
        })

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request,'events/show_venue.html',{
        'venue':venue
    })

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')

    return render(request,'events/update_venue.html',{
        'venue':venue,
        'form':form
    })

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

# Generate CSV files from Venue List
def venue_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=venues.csv'
	# Create a csv writer
	writer = csv.writer(response)
	# Designate The Model
	venues = Venue.objects.all()
	# Add column headings to the csv file
	writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email'])
	# Loop Thu and output
	for venue in venues:
		writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])
	return response

# Generate a PDF File Venue List
def venue_pdf(request):
    	# Create Bytestream buffer
	buf = io.BytesIO()
	# Create a canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	# Create a text object
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica", 14)
	
	# Designate The Model
	venues = Venue.objects.all()
	# Create blank list
	lines = []
	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.zip_code)
		lines.append(venue.phone)
		lines.append(venue.web)
		lines.append(venue.email_address)
		lines.append(" ")
	# Loop
	for line in lines:
		textob.textLine(line)
	# Finish Up
	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)
	# Return 
	return FileResponse(buf, as_attachment=True, filename='venue.pdf')
###########################################################################################
# Events
###########################################################################################
def all_events(request):
    event_list = Event.objects.all().order_by('event_date','name') # grab all information from models.py
    return render(request,'events/event_list.html',{
        'event_list':event_list
    })

def add_event(request):
    submitted = False
    if request.method == "POST":
        form =  EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request,'events/add_event.html',{
        'form':form,
        'submitted':submitted
    })

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request,'events/update_event.html',{
        'event':event,
        'form':form
    })

# Delete an Event
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')