from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplica el valor por el argumento usando Decimal para evitar errores de precisión."""
    try:
        value = Decimal(str(value).replace(',', '.'))
        arg = Decimal(str(arg).replace(',', '.'))
        
        return value * arg
    except (ValueError, TypeError, InvalidOperation) as e:
        print(f"Error al multiplicar: {e}")
        return 0
