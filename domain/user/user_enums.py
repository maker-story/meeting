from enum import Enum

class Role(str, Enum):
    Admin = "Admin"
    Customer = "Customer"
    Freelancer = "Freelancer"
    Supervisor = "Supervisor"

class UserStatus(str, Enum):
    Pending = "Pending"
    Active = "Active"
    Blocked = "Blocked"