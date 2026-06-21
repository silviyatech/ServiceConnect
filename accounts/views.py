import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
from django.db.models import Avg
from .models import UserRole


# Create your views here.
@csrf_exempt

def create_user_role(request):
    
    if request.method=='POST':
        request_body = json.loads(request.body)
        role_name=request_body.get('role_name')
        role_description=request_body.get('role_description','')

        user_role =UserRole.objects.create(
            role_name=role_name,
            role_description=role_description

        )

        return JsonResponse({
            'message': 'user role created successfully',
                             
        },status =201)
    
    else:
        return JsonResponse({'error': 'Invalid request method. only POST is allowed.'},status =400)
@csrf_exempt    
def get_all_user_roles(request):

        if request.method =='GET':
            user_roles= UserRole.objects.all()
            user_role_data=list(user_roles.values('role_id','role_name','role_description'))
                
            return JsonResponse({'user_roles': user_role_data },status =200)
        else:
            return JsonResponse({'error': 'Invalid request method. only GET is allowed.'},status =400)

@csrf_exempt 
def get_single_user_role(request):
    if request.method == 'GET':

        request_body = json.loads(request.body)
        role_id = request_body.get('role_id')

        user_role = UserRole.objects.filter(role_id=role_id)

        if user_role.exists():
            user_role_data = {
                'role_id': user_role[0].role_id,
                'role_name': user_role[0].role_name,
                'role_description': user_role[0].role_description,
            }
            return JsonResponse({'user_roles': user_role_data}, status=200)

        else:
            return JsonResponse({'error': 'User is not found'}, status=404)

    else:
        return JsonResponse({'error': 'Invalid request method. Only GET is allowed.'}, status=400)  

@csrf_exempt

def get_user_role_by_id(request, role_id):

        if request.method == 'GET':
            user_role = UserRole.objects.filter(role_id=role_id).first()

            return JsonResponse({'user_role': {
                'role_id': user_role.role_id,
                'role_name': user_role.role_name,
                'role_description': user_role.role_description
            }}, status=200) if user_role else JsonResponse({'error':'user role not found'}, status=404)  
        else:
            return JsonResponse({'error':'Invalid request method. only GET is allowed'}, status=200)  

@csrf_exempt    
def update_user_role(request):

    if request.method == 'PUT':
        request_body = json.loads(request.body)
        role_id = request_body.get('role_id')
        role_name= request_body.get('role_name')
        role_description= request_body.get('role_description')

        user_role = UserRole.objects.filter(role_id=role_id,is_deleted=False)

        if user_role.exists():
            user_role.update(
                role_name=role_name,
                role_description=role_description
            )





            return JsonResponse({
                'message':'User role updatwed successfully',
                'user_role':{
                    'role_id':user_role[0].role_id,
                    'role_name':user_role[0].role_name,
                    'role_description':user_role[0].role_description

                }

            },  status=200)
        else:
            return JsonResponse({'error': 'User role not found'}, status=404)
    else:
        return JsonResponse({'error':'Invalid request method. only PUT is allowed.'}, status=400)

    
@csrf_exempt    
def delete_user_role(request):

    if request.method == 'DELETE':
        request_body = json.loads(request.body)
        role_id = request_body.get('role_id')

        user_role = UserRole.objects.filter( role_id= role_id)
        user_role.delete()


        return JsonResponse({'message': ' User role deleted successfully. '}, status=200)
    else:
        return JsonResponse({'error': ' Invalid request method. only DELETE is allowed.'}, status=400) 

@csrf_exempt
def delete_user_role_update(request):
    if request.method == 'DELETE':
        request_body = json.loads(request.body)
        role_id = request_body.get('role_id')

        user_role = UserRole.objects.filter(role_id=role_id, is_deleted=False)
        if not user_role.exists():
            return JsonResponse({'error': 'User not found'}, status=404)

        user_role.update(is_deleted=True)
        return JsonResponse({'message': 'User role deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': ' Invalid request method. only DELETE is allowed.'}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .models import User, UserRole
import json
import random


@csrf_exempt
def send_email_otp(request):
    """
    Send OTP to user's email address
    """

    if request.method == "POST":

        request_data = json.loads(request.body)

        email_address = request_data.get("email_address")

        if not email_address:
            return JsonResponse({
                "error": "Email Address Required"
            }, status=400)

        otp = str(random.randint(100000, 999999))

        message = f"""
Welcome to Service Connect!

Thank you for registering with our application. Service Connect is designed to connect customers with trusted service providers and make accessing services simple, convenient, and reliable.

To complete your registration and verify your email address, please use the One-Time Password (OTP) provided below:

OTP: {otp}

This OTP is valid for a limited time. Please do not share it with anyone for security reasons.

If you did not request this registration, please ignore this email.

Thank you for choosing Service Connect.

Best Regards,

Silviya
Service Connect Team
"""

        send_mail(
            subject="Welcome to Service Connect - Email Verification OTP",
            message=message,
            from_email="yourgmail@gmail.com",
            recipient_list=[email_address],
            fail_silently=False
        )

        return JsonResponse({
            "message": "OTP Sent Successfully",
            "otp": otp
        }, status=200)

    return JsonResponse({
        "error": "Invalid Request Method. Only POST is allowed."
    }, status=400)


@csrf_exempt
def create_user(request):

    if request.method == 'POST':

        request_body = json.loads(request.body)

        full_name = request_body.get('full_name')
        email = request_body.get('email')
        phone_number = request_body.get('phone_number')
        password = request_body.get('password')
        confirm_password = request_body.get('confirm_password')
        role_id = request_body.get('role_id')

        if password != confirm_password:
            return JsonResponse({
                'error': 'Passwords do not match'
            }, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'error': 'Email already exists'
            }, status=400)

        if User.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({
                'error': 'Phone number already exists'
            }, status=400)

        user_role = UserRole.objects.filter(
            role_id=role_id
        ).first()

        if not user_role:
            return JsonResponse({
                'error': 'User role not found'
            }, status=404)

        otp = str(random.randint(100000, 999999))

        user = User.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,
            confirm_password=confirm_password,
            user_role=user_role,
            email_otp=otp
        )

        message = f"""
Welcome to Service Connect!

Thank you for registering with our application.

Your Email Verification OTP is:

OTP: {otp}

Please do not share this OTP with anyone.

Best Regards,

Silviya
Service Connect Team
"""

        send_mail(
            subject="Service Connect Email Verification OTP",
            message=message,
            from_email="yourgmail@gmail.com",
            recipient_list=[email],
            fail_silently=False
        )

        return JsonResponse({

            'message': 'User created successfully and OTP sent to email',

            'user': {
                'user_id': user.user_id,
                'full_name': user.full_name,
                'email': user.email,
                'phone_number': user.phone_number,

                'user_role': {
                    'role_id': user.user_role.role_id,
                    'role_name': user.user_role.role_name
                }
            }

        }, status=201)

    return JsonResponse({
        'error': 'Invalid request method. Only POST is allowed.'
    }, status=400)


@csrf_exempt
def verification_email(request):

    if request.method == 'POST':

        request_data = json.loads(request.body)

        email = request_data.get('email')
        otp = request_data.get('otp')

        user = User.objects.filter(email=email).first()

        if not user:
            return JsonResponse({
                'error': 'User not found'
            }, status=404)

        if user.email_otp == otp:

            user.email_otp = None
            user.save()

            return JsonResponse({
                'message': 'Email verified successfully'
            }, status=200)

        return JsonResponse({
            'error': 'Invalid OTP'
        }, status=400)

    return JsonResponse({
        'error': 'Invalid request method. Only POST is allowed.'
    }, status=400)

@csrf_exempt
def get_active_user_role(request):
    if request.method =='GET':
        active_user_roles = UserRole.objects.filter(is_deleted = False)
        """
         select * from user_role where is_deleted = false;

        """
        active_user_roles_data = list(active_user_roles.values('role_name'))
        return JsonResponse({'active_user_roles':active_user_roles_data}, status=200)
    
    else:
        return JsonResponse({'error': 'Invalid request method .only GET is allowed.'}, status=400)
    
@csrf_exempt
def get_inactive_user_role(request):
    if request.method =='GET':
        inactive_user_roles = UserRole.objects.exclude(is_deleted = False)
        """
         select * from user_role where is_deleted = false;

        """
        inactive_user_roles_data = list(inactive_user_roles.values('role_name'))
        return JsonResponse({'inactive_user_roles':inactive_user_roles_data}, status=200)
    
    else:
        return JsonResponse({'error': 'Invalid request method .only GET is allowed.'}, status=400)
    
@csrf_exempt
def get_active_user_roles_order_by_asc(request):
    if request.method == "GET":
        active_user_roles= UserRole.objects.order_by('role_id')

        """
            select * from user role order by user role id asc;

        """

        active_user_roles_data = list(active_user_roles.values())
        return JsonResponse({'active user_roles': active_user_roles_data}, status=200)



    else:
        return JsonResponse({"error: Invalid request method. Only Get is allowed."}, status=400)
    

@csrf_exempt
def get_active_user_roles_order_by_desc(request):
    if request.method == "GET":
        active_user_roles= UserRole.objects.order_by('-role_id')

        """
            select * from user role order by user role id asc;

        """

        active_user_roles_data = list(active_user_roles.values())
        return JsonResponse({'active user_roles': active_user_roles_data}, status=200)



    else:
        return JsonResponse({"error: Invalid request method. Only Get is allowed."}, status=400)
    

@csrf_exempt
def get_user_count(request):

    if request.method == 'GET':

        total_users = User.objects.count()

        return JsonResponse({
            "total_users": total_users
        }, status=200)

    return JsonResponse({
        "error": "Only GET method is allowed"
    }, status=400) 

@csrf_exempt 
def get_user_values(request):

    users = User.objects.values(
        'user_id',
        'full_name',
        'email'
    )

    return JsonResponse(
        list(users),
        safe=False
    )  


@csrf_exempt 
def get_user_values_list(request):

    users = User.objects.values_list(
        'user_id',
        'full_name'
    )

    return JsonResponse(
        list(users),
        safe=False
    )


@csrf_exempt 
def get_user_names(request):

    users = User.objects.values_list(
        'full_name',
        flat=True
    )

    return JsonResponse(
        list(users),
        safe=False
    )
    

def get_user_aggregate_count(request):

    total_users = User.objects.aggregate(
        total_count=Count('user_id')
    )

    return JsonResponse(total_users) 

def get_user_max_id(request):

    max_id = User.objects.aggregate(
        max_user_id=Max('user_id')
    )

    return JsonResponse(max_id)   

def get_user_min_id(request):

    min_id = User.objects.aggregate(
        min_user_id=Min('user_id')
    )

    return JsonResponse(min_id)

def get_user_avg_id(request):

    avg_id = User.objects.aggregate(
        avg_user_id=Avg('user_id')
    )

    return JsonResponse(avg_id)


    
        



