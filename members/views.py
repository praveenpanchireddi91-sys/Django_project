from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Teacher, Attendance
from django.contrib import messages
from members.utils import generate_otp
from django.core.mail import send_mail
from .forms import OTPForm
from django.contrib.auth.hashers import make_password, check_password
from .models import Student, Attendance
from datetime import date


def homes(request):
    return render(request, 'home.html')


def student_signup(request):
    return render(request, 'student_signup.html')


def student_dashboard(request):
    return render(request, 'student_dashboard.html')


def teacher_signup(request):
    return render(request, 'teacher_signup.html')


def student_login(request):
    return render(request, 'student_login.html')


def teacher_login(request):
    return render(request, 'teacher_login.html')


def signup(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        year = request.POST.get('year')

        if password != confirm_password:
            return HttpResponse("Passwords do not match.")

        if Student.objects.filter(email=email).exists():

            messages.info(request, "Email already exists...")

            return redirect('student_signup')

        otp = generate_otp()

        request.session['otp'] = str(otp)
        request.session['name'] = name
        request.session['email'] = email
        request.session['password'] = make_password(password)
        request.session['year'] = year

        send_mail(
            'Your OTP',
            f'Your OTP is : {otp}',
            'praveenpanchireddi91@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect('verify_otp')

    return render(request, 'student_signup.html')


def verify_otp(request):

    if request.method == 'POST':

        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if str(stored_otp) == str(entered_otp):

            student = Student(
                name=request.session.get('name'),
                email=request.session.get('email'),
                password=request.session.get('password'),
                year=request.session.get('year')
            )

            student.save()

            request.session.pop('otp', None)

            return HttpResponse("""
                <script>
                    alert('Registration Successful');
                    window.location.href='/student_login/';
                </script>
            """)

        else:

            return HttpResponse("""
                <script>
                    alert('Invalid OTP');
                    window.location.href='/verify_otp/';
                </script>
            """)

    return render(request, 'verify_otp.html')


def teachersignup(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if password != confirm_password:
            return HttpResponse("Passwords do not match.")

        if Teacher.objects.filter(email=email).exists():

            messages.info(request, "Email already exists...")

            return redirect('teacher_signup')

        otp = generate_otp()

        request.session['otp'] = str(otp)
        request.session['name'] = name
        request.session['email'] = email
        request.session['password'] = make_password(password)

        send_mail(
            'Your OTP',
            f'Your OTP is : {otp}',
            'praveenpanchireddi91@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect('verifyotp')

    return render(request, 'teacher_signup.html')


def verifyotp(request):

    if request.method == 'POST':

        form = OTPForm(request.POST)

        if form.is_valid():

            entered_otp = form.cleaned_data['otp']
            stored_otp = request.session.get('otp')

            if str(stored_otp) == str(entered_otp):

                user = Teacher(
                    name=request.session.get('name'),
                    email=request.session.get('email'),
                    password=request.session.get('password')
                )

                user.save()

                request.session.pop('otp', None)

                return HttpResponse("""
                    <script>
                        alert('Teacher Registration Successful');
                        window.location.href='/teacher_login/';
                    </script>
                """)

            else:

                return HttpResponse("""
                    <script>
                        alert('Invalid OTP');
                        window.location.href='/verifyotp/';
                    </script>
                """)

    else:

        form = OTPForm()

    return render(request, 'verifyotp.html', {'form': form})


def teacherlogin(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:

            return HttpResponse("""
                <script>
                    alert('All fields are required');
                    window.location.href='/teacher_login/';
                </script>
            """)

        if Teacher.objects.filter(email=email).exists():

            teacher = Teacher.objects.get(email=email)

            if check_password(password, teacher.password):

                return redirect('teacher_dashboard')

            else:

                return HttpResponse("""
                    <script>
                        alert('Wrong Password');
                        window.location.href='/teacher_login/';
                    </script>
                """)

        else:

            return HttpResponse("""
                <script>
                    alert('Wrong Email');
                    window.location.href='/teacher_login/';
                </script>
            """)

    return render(request, 'teacher_login.html')


def studentlogin(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not name or not email or not password:

            return HttpResponse("""
                <script>
                    alert('All fields are required');
                    window.location.href='/student_login/';
                </script>
            """)

        if Student.objects.filter(email=email, name=name).exists():

            student = Student.objects.get(email=email, name=name)

            if check_password(password, student.password):

                attendance = Attendance.objects.filter(student=student).order_by('-date')

                context = {
                    'student': student,
                    'attendance': attendance
                }

                return render(request, 'student_dashboard.html', context)

            else:

                return HttpResponse("""
                    <script>
                        alert('Wrong Password');
                        window.location.href='/student_login/';
                    </script>
                """)

        else:

            return HttpResponse("""
                <script>
                    alert('Wrong Name or Email');
                    window.location.href='/student_login/';
                </script>
            """)

    return render(request, 'student_login.html')


def teacher_dashboard(request):

    students = []

    selected_year = None

    if request.method == 'POST':

        if 'load_students' in request.POST:

            selected_year = request.POST.get('year')

            students = Student.objects.filter(
                year=selected_year
            ).order_by('name')

            context = {
                'students': students,
                'selected_year': selected_year
            }

            return render(request, 'teacher_dashboard.html', context)

        elif 'save_attendance' in request.POST:

            year = request.POST.get('selected_year')

            attendance_date = request.POST.get('attendance_date')

            students = Student.objects.filter(
                year=year
            ).order_by('name')

            for student in students:

                status = request.POST.get(f'attendance_{student.id}')

                Attendance.objects.filter(
                    student=student,
                    date=attendance_date
                ).delete()

                Attendance.objects.create(
                    student=student,
                    date=attendance_date,
                    status=status
                )

            return HttpResponse("""
                <script>
                    alert('Attendance Saved Successfully');
                    window.location.href='/teacher_dashboard/';
                </script>
            """)

    context = {
        'students': students,
        'selected_year': selected_year
    }

    return render(request, 'teacher_dashboard.html', context)

def student_list(request):

    students = Student.objects.all()

    context = {
        'students': students
    }

    return render(request, 'teacher_dashboard.html', context)