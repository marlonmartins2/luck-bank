from pydantic import BaseModel, EmailStr, constr


class LoginUserRequest(BaseModel):
    """
    Model for user login from request
    Args:
        BaseModel (Pydantic): the Pydantic base model.
    """
    class Config:
        """
        Config for address
        Args:
            Config (Config): The global config for this model.
        """
        anystr_strip_whitespace = True
        anystr_lower = True

    email: EmailStr
    password: constr(min_length=8)
