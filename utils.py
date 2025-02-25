from functools import wraps
from services.colorizer import Colorizer
from models.exceptions import PhoneValueError, BirthdayValueError

def input_error(errors_config: dict = {}):
	errors = {
		ValueError: "Contact name and phone are required",
		IndexError: "Contact name is required"
	}

	errors.update(errors_config or {})

	def wrapper(func):
		@wraps(func)
		def inner(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except KeyError as e:
				return Colorizer.error(f"Contact {e} not found")
			except PhoneValueError as e:
				return Colorizer.error(e)
			except BirthdayValueError as e:
				return Colorizer.error(e)
			except ValueError as e:
				return Colorizer.error(errors[ValueError])
			except IndexError as e:
				return Colorizer.error(errors[IndexError])
		return inner
	return wrapper