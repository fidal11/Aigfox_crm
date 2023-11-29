from django.shortcuts import render
from .models import ClockInClockOut,Break
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone
import datetime

# Create your views here.


 
    
    
 



from datetime import datetime, date


def index(request):
    msg = ''
    if request.method == 'POST':
        email = request.POST['email']
        action = request.POST['action']
        current_datetime = datetime.now()
        current_date = date.today()

        # Check if there are existing entries for clock in or clock out for the given email on the current day
        existing_clock_in = ClockInClockOut.objects.filter(email=email, clock_type='in', timestamp__date=current_date).exists()
        existing_clock_out = ClockInClockOut.objects.filter(email=email, clock_type='out', timestamp__date=current_date).exists()

        if action == 'clock_in' and not existing_clock_in:
            # Record clock in timestamp for the given email
            ClockInClockOut.objects.create(timestamp=current_datetime, clock_type='in', email=email)
             
            msg='Clock in recorded successfully.'
        elif action == 'clock_out' and not existing_clock_out and existing_clock_in:
            # Record clock out timestamp for the given email only if a clock in exists for the same day
            ClockInClockOut.objects.create(timestamp=current_datetime, clock_type='out', email=email)
            
            msg = 'Clock out recorded successfully.'
        elif action == 'start_break':
            # Record break start timestamp for the given email
            Break.objects.create(timestamp_start=current_datetime, timestamp_end=None, email=email)
             
            msg = 'Break started.'

        elif action == 'end_break':
            # Record break end timestamp for the given email
            Break.objects.create(timestamp_end=current_datetime, timestamp_start=None, email=email)
             
            msg='Break Ended'
        else:
            msg='Action Already Performed !'
    else:
        msg = ""
    return render(request, 'common/index.html' ,{'message':msg})


 

# Calculate total work time for each employee

def worktime(request):
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
                if (
                    b.timestamp_start
                    and clock_in.timestamp <= b.timestamp_start
                    and (clock_out is None or (b.timestamp_end and b.timestamp_end < clock_out.timestamp))
                ):
                    break_end = (
                        b.timestamp_end
                        if b.timestamp_end and (clock_out is None or b.timestamp_end < clock_out.timestamp)
                        else (clock_out.timestamp if clock_out else None)
                    )
                    if break_end:
                        break_time += min(break_end, clock_out.timestamp) - max(b.timestamp_start, clock_in.timestamp)

            # Calculate work time after deducting break time
            work_time = (clock_out.timestamp - clock_in.timestamp - break_time) if (clock_out and clock_out.timestamp) else timedelta()

            worktime_entries.append({
                'clock_in_time': clock_in.timestamp.time(),
                'clock_out_time': clock_out.timestamp.time() if clock_out and clock_out.timestamp else None,
                'total_work_time': work_time
            })

        worktime_data.append({
            'email': email,
            'date': clock_in.timestamp.date().isoformat(),
            'worktime_entries': worktime_entries
        })

    return render(request, 'common/worktime.html', {'worktime_data': worktime_data})



  