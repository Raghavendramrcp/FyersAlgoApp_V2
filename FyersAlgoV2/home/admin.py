from django.contrib import admin

from .models import (
    Fyers_Access_Token,
    Fyers_Auth_Inputs,
    CurrencySymbol,
    MCXSymbol,
    EquitySymbol,
    
)

# Register your models here.


admin.site.register(Fyers_Access_Token)
admin.site.register(Fyers_Auth_Inputs)
admin.site.register(CurrencySymbol)
admin.site.register(MCXSymbol)
admin.site.register(EquitySymbol)

