from models.User import User
from fastapi import APIRouter, HTTPException
from schema.user import UserCreate, UserResult,  UserActivationCreate
import secrets
from passlib.hash import bcrypt
import os
from dotenv import load_dotenv
load_dotenv('.env')
from datetime import datetime, timedelta
from services.email_engine import SystemMailer
import socket
import random
from fastapi import status
from fastapi.responses import JSONResponse

system_mailer = SystemMailer()
router = APIRouter(
    prefix= os.getenv('API_BASE_URL')
)


def get_nxt_datetime(next_min:int | None = None):
    """
    next_min can be any minute(s) of type int or None
    """
    dt = datetime.now()
    if next_min:
        next_min_dt = dt + timedelta(minutes=next_min)
        return next_min_dt
    else:
        return dt

def generate_code(n: int):
    rand_code = str(random.getrandbits(36))
    if len(rand_code) >= n:
        return rand_code[0:n]
        


def get_user_ip_addr():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    return ip_addr

@router.put('/user/create', response_model=UserResult)
async def create_user(req: UserCreate):
    email_code = generate_code(8)

    if req.re_password != req.password:
        raise HTTPException(detail="Password do not match, try again", status_code=status.HTTP_406_NOT_ACCEPTABLE)

    elif User.where('email', req.email.lower()).where("is_verified", True).where("is_active", True).get():
        raise HTTPException(
            status_code=status.HTTP_421_MISDIRECTED_REQUEST, 
            detail=f"User email - {req.email.lower()} already exist, try login"
        )

    elif User.where("email", req.email.lower()).where("activation_time_expires", "<=", get_nxt_datetime()).where("is_verified", False).where("is_active", True).get():
        """
        Activation time expires is greater than 1 min, so
        we regenerate, update our only needed attributes using
        force_update method.
        """
        act_time_expires = get_nxt_datetime(1)
        user_obj = User.where("email", req.email.lower()).update({
            "email_code":  email_code,
            "activation_time_expires": act_time_expires,
        })

        if user_obj:
            await system_mailer.send_mail(
                subject="Account Activation Code",
                email_to=req.email.lower(),
                body= {
                    "msg": email_code,
                    "email": req.email
                }
            )
        raise HTTPException(
            status_code=status.HTTP_206_PARTIAL_CONTENT, 
            detail=f"Account ID Exist, please verify, we've resent new code to {req.email}"
        )
    
    elif User.where("email", req.email.lower()).where("activation_time_expires", ">=", get_nxt_datetime()).where("is_verified", False).where("is_active", True).get():
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Please, we've to wait for the elapse time")
        
    
    elif User.where("email", req.email.lower()).where("is_verified", True).where("is_active", False).get():
        raise HTTPException(
            detail="Account Blocked!, Contact Us", 
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    else:
        user_ip_address = get_user_ip_addr()
        user = User.create({
        "username": "user-"+secrets.token_urlsafe(6),
        "email": req.email.lower(),
        "password": bcrypt.hash(req.password),
        "is_staff": False,
        "is_superuser": False,
        "activation_time_expires": get_nxt_datetime(1),
        "is_verified": False,
        "is_active": True,
        "ip_addr": user_ip_address,
        "email_code": email_code
    }).fresh()
        if user:
            await system_mailer.send_mail(
                subject="Account Activation Code",
                email_to=req.email.lower(),
                body= {
                    "msg": email_code,
                    "email": req.email
                },
            )
            return user



@router.post('/user/activation')
def account_activation(req: UserActivationCreate) -> JSONResponse:
    if not req:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No activation code found")
    
    if User.where("email", req.email.lower()).where("email_code", req.activation_code).where("activation_time_expires", ">=", get_nxt_datetime(4)).get():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Token expired...request for new code"
        )
    elif User.where("email","!=" ,req.email.lower()).or_where("email_code", "!=", req.activation_code).where("activation_time_expires", "<=", get_nxt_datetime(4)).get():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Invalid Credential, try again"
        )
    
    else:
        #verify the user's account dtails
        user = User.where("email", req.email).update({
            "is_verified": True,
            "is_active": True,
        })
        
        if user:
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                content= {
                    "message": "Your account was successfully activated",
                }
            )
        
