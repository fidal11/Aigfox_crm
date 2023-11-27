from django.shortcuts import render
from .models import ClockInClockOut,Break
from django.http import HttpResponse
from datetime import datetime, date,timedelta
from django.utils import timezone
import datetime

# Create your views here.


 
    
    

def can_clock_in(email):
    today = date.today()
    clock_ins_today = ClockInClockOut.objects.filter(email=email, clock_type='in', timestamp__date=today)
    return not clock_ins_today.exists()

def can_clock_out(email):
    today = date.today()
    clock_outs_today = ClockInClockOut.objects.filter(email=email, clock_type='out', timestamp__date=today)
    return not clock_outs_today.exists()





def index(request):
    msg=''
    if request.method == 'POST':
        email = request.POST['email']
        action = request.POST['action']

        # Record timestamps based on the action clicked
        if action == 'clock_in':
            # Record clock in timestamp for the given email
            ClockInClockOut.objects.create(timestamp=datetime.datetime.now(), clock_type='in', email=email)
            
        elif action == 'clock_out':
            # Record clock out timestamp for the given email
            ClockInClockOut.objects.create(timestamp=datetime.datetime.now(), clock_type='out', email=email)
        elif action == 'start_break':
            # Record break start timestamp for the given email
            Break.objects.create(timestamp_start=datetime.datetime.now(), timestamp_end=None, email=email)
        elif action == 'end_break':
            # Record break end timestamp for the given email
            Break.objects.create(timestamp_end=datetime.datetime.now(), timestamp_start=None, email=email)

        return HttpResponse("Action recorded successfully.")
    else:
        msg="Error"
    return render(request,'common/index.html')


 



def worktime(request):
    
# Calculate total work time for each employee
    employees = ClockInClockOut.objects.values('email').distinct()
    worktime_data = []

    for employee in employees:
        email = employee['email']
        clock_ins = ClockInClockOut.objects.filter(email=email, clock_type='in').order_by('timestamp')
        clock_outs = ClockInClockOut.objects.filter(email=email, clock_type='out').order_by('timestamp')
        breaks = Break.objects.filter(email=email).order_by('timestamp_start')

        worktime_entries = []
        for i in range(len(clock_ins)):
            clock_in = clock_ins[i]
            clock_out = clock_outs[i] if i < len(clock_outs) else None

            # Calculate break time between clock-in and clock-out
            break_time = timedelta()
            for b in breaks:
                if b.timestamp_start and clock_in.timestamp <= b.timestamp_start and (clock_out is None or b.timestamp_start < clock_out.timestamp):
                    break_end = b.timestamp_end if b.timestamp_end and (clock_out is None or b.timestamp_end < clock_out.timestamp) else clock_out.timestamp
                    break_time += min(break_end, clock_out.timestamp) - max(b.timestamp_start, clock_in.timestamp)

            # Calculate work time after deducting break time
            work_time = (clock_out.timestamp - clock_in.timestamp - break_time) if clock_out else timedelta()

            worktime_entries.append({
                'clock_in_time': clock_in.timestamp.time(),
                'clock_out_time': clock_out.timestamp.time() if clock_out else None,
                'total_work_time': work_time
            })

        worktime_data.append({
            'email': email,
            'date': clock_in.timestamp.date().isoformat(),
            'worktime_entries': worktime_entries
        })

    return render(request, 'common/worktime.html', {'worktime_data': worktime_data})

  