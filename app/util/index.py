import bcrypt
from datetime import datetime

def verify_password(plain_password, hashed_password):
  return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def hash_password(password):
  return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def get_current_datetime():
  return datetime.now()