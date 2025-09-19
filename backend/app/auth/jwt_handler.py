from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.employee_department import EmployeeDepartment
from app.schemas.auth import TokenData
from app.models import Employee, EmployeeDepartment
from app.models.router_access import RouterAccess

SECRET_KEY = "eemw-secret@-@backend@-@key@20sdajkfljsdalpfh;dsajkl;fasdjklfds4815153333333333333348461asd8f46sdaf1dsa6f51sd561fds250"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/employees/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="employees/login/swagger")



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Employee:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Employee).filter(Employee.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Employee:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials from get admin",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("Token:", token)  # Debug 1
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload:", payload)  # Debug 2
        user_id = payload.get("sub")
        if user_id is None:
            print("sub is missing")
            raise credentials_exception
        user_id = int(user_id)
        print("Decoded user_id:", user_id)  
    except JWTError as e:
        print("JWT Decode Error:", e)
        raise credentials_exception

    user = db.query(Employee).filter(Employee.id == user_id).first()
    print("User from DB:", user)  # Debug 4
    if user is None or user.role != "admin":
        print("Not admin or not found")
        raise credentials_exception

    return user


# def get_current_manager(current_user: Employee = Depends(get_current_user)) -> Employee:
#     if current_user.role != "manager":
#         raise HTTPException(status_code=403, detail="Only Assigned Managers Can Access")
#     return current_user

def get_admin_or_authorized_manager(
    db: Session = Depends(get_db),
    current_user: Employee = Depends(get_current_user),
    department_id: int = Path(...)
) -> Employee:
    if current_user.role == "admin":
        return current_user

    if current_user.role == "manager":
        authorized = db.query(EmployeeDepartment).filter_by(
            employee_id=current_user.id,
            department_id=department_id
        ).first()

        if authorized:
            return current_user

    raise HTTPException(status_code=403, detail="Not authorized for this department")

def authorize_by_department(
    allowed_department_ids: list[int]
):
    def _authorize(
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
    ) -> Employee:
        if current_user.role == "admin":
            return current_user

        if current_user.role == "manager":
            authorized = db.query(EmployeeDepartment).filter(
                EmployeeDepartment.employee_id == current_user.id,
                EmployeeDepartment.department_id.in_(allowed_department_ids)
            ).first()

            if authorized:
                return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this resource"
        )

    return _authorize

def check_resource_permission(resource_name: str):
    def permission_checker(
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user),
    ):
        if current_user.role == 'admin':
            return  
        dept_ids = db.query(EmployeeDepartment.department_id).filter(
            EmployeeDepartment.employee_id == current_user.id
        ).all()
        dept_ids = [id for (id,) in dept_ids]

        allowed = db.query(RouterAccess.resource_name).filter(
            RouterAccess.department_id.in_(dept_ids)
        ).all()
        allowed_resources = [r[0] for r in allowed]

        if resource_name not in allowed_resources:
            raise HTTPException(status_code=403, detail="Access denied")
    return permission_checker

