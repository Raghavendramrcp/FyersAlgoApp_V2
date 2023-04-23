from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# Create your models here.


class Fyers_Auth_Inputs(models.Model):
    # one user may have many apps
    user_ass = models.ForeignKey(User, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=50, null=True, blank=True)
    secret_id = models.CharField(max_length=50, null=True, blank=True)
    redirect_url = models.CharField(
        max_length=100, default="https://trade.fyers.in/api-login/redirect-uri/index.html")

    def __str__(self):
        return self.client_id


class Fyers_Access_Token(models.Model):
    app_ass = models.OneToOneField(Fyers_Auth_Inputs, on_delete=models.CASCADE)
    auth_code = models.CharField(max_length=1500, null=True, blank=True)

    def __str__(self):
        return f"Access Token-{self.app_ass}"


class CurrencySymbol(models.Model):
    fytoken = models.CharField(max_length=255, unique=True)
    symbol_details = models.CharField(max_length=255)
    exchange_instrument_type = models.IntegerField()
    minimum_lot_size = models.IntegerField()
    tick_size = models.FloatField()
    isin = models.CharField(max_length=255, null=True, blank=True)
    trading_session = models.CharField(max_length=255)
    last_update_date = models.DateField()
    expiry_date = models.CharField(max_length=255)
    symbol_ticker = models.CharField(max_length=255)
    exchange = models.IntegerField()
    segment = models.IntegerField()
    scrip_code = models.IntegerField()
    underlying_scrip_code = models.CharField(max_length=200)
    modifed_script_code = models.IntegerField()
    strike_price = models.FloatField()
    option_type = models.CharField(max_length=255)
    exchange_token = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.underlying_scrip_code}-{self.symbol_details}"


class MCXSymbol(models.Model):
    fytoken = models.CharField(max_length=255, unique=True)
    symbol_details = models.CharField(max_length=255)
    exchange_instrument_type = models.IntegerField()
    minimum_lot_size = models.IntegerField()
    tick_size = models.FloatField()
    isin = models.CharField(max_length=255, null=True, blank=True)
    trading_session = models.CharField(max_length=255)
    last_update_date = models.DateField()
    expiry_date = models.CharField(max_length=255)
    symbol_ticker = models.CharField(max_length=255)
    exchange = models.IntegerField()
    segment = models.IntegerField()
    scrip_code = models.IntegerField()
    underlying_scrip_code = models.CharField(max_length=200)
    modifed_script_code = models.IntegerField()
    strike_price = models.FloatField()
    option_type = models.CharField(max_length=255)
    exchange_token = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.underlying_scrip_code}-{self.symbol_details}"


class EquitySymbol(models.Model):
    fytoken = models.CharField(max_length=255, unique=True)
    symbol_details = models.CharField(max_length=255)
    exchange_instrument_type = models.IntegerField()
    minimum_lot_size = models.IntegerField()
    tick_size = models.FloatField()
    isin = models.CharField(max_length=255, null=True, blank=True)
    trading_session = models.CharField(max_length=255)
    last_update_date = models.CharField(max_length=100, null=True, blank=True)
    expiry_date = models.CharField(max_length=255)
    symbol_ticker = models.CharField(max_length=255)
    exchange = models.IntegerField()
    segment = models.IntegerField()
    scrip_code = models.IntegerField()
    underlying_scrip_code = models.CharField(max_length=200)
    modifed_script_code = models.IntegerField()
    strike_price = models.FloatField()
    option_type = models.CharField(max_length=255)
    exchange_token = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.underlying_scrip_code}-{self.symbol_details}"
