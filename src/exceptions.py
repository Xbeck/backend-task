from fastapi import HTTPException, status




#####################################? 88 probels ######################################
########################################################################################

class BookingException(HTTPException):
    status = "error"
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# ################################
#? Error Exceptions
# ################################

class UserNotAdminException(BookingException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="Вы не являетесь администратором"
    
class PermissionErrorException(BookingException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="Недостаточно прав для выполнения операции"

class UserNotFoundException(BookingException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Пользователь отсутствует"

class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"
        
class IncorrectEmailOrPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"
        
class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Срок действия токена истек"
        
class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"
        
class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"


#################### Stadium Exceptions ####################
class BadRequestException(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Данные были введены неверно."

class StadiumNotFoundException(BookingException):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Такого стадиона не найдено."

class StadiumAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Такой стадион уже существует."

#################### Booking Exceptions ####################
class BookingAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="В это время стадион занят."




#################### Email Exceptions ####################
class CannotSendPasswordException(BookingException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Не удалось отправить пароль."


class IncorrectPasswordOrExpiredException(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Неверный или истекший пароль."


class UserDataUpdateFailedException(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Не удалось обновить данные пользователя"
        

class CannotAddDataToDatabase(BookingException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Не удалось добавить запись"


class CannotProcessCSV(BookingException):
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    detail="Не удалось обработать CSV файл"





