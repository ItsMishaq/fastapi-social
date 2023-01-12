#for hashing password


from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)



# The purpose of this function is to verify the hashed pwd and user tried pwd.
def verify(plain_password, hashed_password):         
    return pwd_context.verify(plain_password, hashed_password)