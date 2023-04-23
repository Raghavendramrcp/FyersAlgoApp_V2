from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView


from .models import Fyers_Access_Token, Fyers_Auth_Inputs, MCXSymbol, CurrencySymbol, EquitySymbol
from .forms import Fyers_Access_TokenForm
# Create your views here.

import pandas as pd

from fyers_api import fyersModel
from fyers_api import accessToken


class HomePageView(TemplateView):
    template_name = 'home/homepage.html'


class AccessTokenView(View):

    """ Generate Access Toke with class based view  """

    form_class = Fyers_Access_TokenForm
    template_name = 'home/accesstoken.html'

    def get_queryset(self):
        self.app_inputs = get_object_or_404(
            Fyers_Auth_Inputs, user_ass_id=self.kwargs['pk'])
        return self.app_inputs

    def get(self, request, pk):
        client_id = self.get_queryset().client_id
        secret_key = self.get_queryset().secret_id
        redirect_url = self.get_queryset().redirect_url

        session = accessToken.SessionModel(client_id=client_id, secret_key=secret_key,
                                           redirect_uri=redirect_url, response_type="code", grant_type="authorization_code")

        response = session.generate_authcode()

        form = self.form_class

        return render(request, self.template_name, {'access_form': form, 'response': response})

    def post(self, request, pk):

        if request.method == 'POST':
            client_id = self.get_queryset().client_id
            secret_key = self.get_queryset().secret_id
            redirect_url = self.get_queryset().redirect_url

            session = accessToken.SessionModel(client_id=client_id, secret_key=secret_key,
                                               redirect_uri=redirect_url, response_type="code", grant_type="authorization_code")
            access_form = Fyers_Access_TokenForm(request.POST)

            if access_form.is_valid():
                user_ass = access_form.cleaned_data.get('app_ass')
                auth_code = access_form.cleaned_data.get('auth_code')

                session.set_token(auth_code)
                access_token = session.generate_token()["access_token"]

                object = Fyers_Access_Token(
                    app_ass=user_ass, auth_code=access_token)
                object.save()

                return redirect('homepage')

        form = Fyers_Access_TokenForm()
        return render(request, self.template_name, {'access_token': form})

# Deleting Access Token


def delete_auth_code(request, pk):
    """ Delete the Access Token with this function """

    if request.method == 'POST':
        accesstoken = Fyers_Access_Token.objects.filter(app_ass_id=pk)
        accesstoken.delete()
        return redirect('homepage')


# TODO: 1) generate a function to upload the symbol list of Currency, MCX and Equity
#       2) Create a MCX app

class SymbolUploadView(TemplateView):
    template_name = 'home/symbolupload.html'


# View for Currency Symbol

def currency_symbol_upload(request):

    if request.method == 'POST':

        currency_symbols_url = "https://public.fyers.in/sym_details/NSE_CD.csv"
        read_csv = pd.read_csv(currency_symbols_url, header=None)

        usdinr_data = read_csv[(read_csv[16] == 'XX') & ((read_csv[13] == 'USDINR') | (
            read_csv[13] == 'GBPINR') | (read_csv[13] == 'EURINR') | (read_csv[13] == 'JPYINR'))]

        for index, row in usdinr_data.iterrows():
            new_currency_symbol = CurrencySymbol(
                fytoken=row[0],
                symbol_details=row[1],
                exchange_instrument_type=row[2],
                minimum_lot_size=row[3],
                tick_size=row[4],
                isin=row[5],
                trading_session=row[6],
                last_update_date=row[7],
                expiry_date=row[8],
                symbol_ticker=row[9],
                exchange=row[10],
                segment=row[11],
                scrip_code=row[12],
                underlying_scrip_code=row[13],
                modifed_script_code=row[14],
                strike_price=row[15],
                option_type=row[16],
                exchange_token=row[17],
            )
            new_currency_symbol.save()

        return redirect('symbol_update')


# Delete CUrrency Symbols

def delete_currency_symbols(request):
    if request.method == 'POST':

        currency_symbol = CurrencySymbol.objects.filter(option_type='XX')
        currency_symbol.delete()
        return redirect('symbol_update')

# Upload View for MCX Symbols


def mcx_symbols_upload(request):
    if request.method == "POST":
        mcx_url = "https://public.fyers.in/sym_details/MCX_COM.csv"
        read_csv = pd.read_csv(mcx_url, header=None)

        mcx_data = read_csv[read_csv[16] == "XX"]

        for index, row in mcx_data.iterrows():
            new_mcx_symbol = MCXSymbol(
                fytoken=row[0],
                symbol_details=row[1],
                exchange_instrument_type=row[2],
                minimum_lot_size=row[3],
                tick_size=row[4],
                isin=row[5],
                trading_session=row[6],
                last_update_date=row[7],
                expiry_date=row[8],
                symbol_ticker=row[9],
                exchange=row[10],
                segment=row[11],
                scrip_code=row[12],
                underlying_scrip_code=row[13],
                modifed_script_code=row[14],
                strike_price=row[15],
                option_type=row[16],
                exchange_token=row[17]
            )
            new_mcx_symbol.save()
        return redirect('symbol_update')


def delete_mcx_symbols(request):
    if request.method == 'POST':
        mcx_symbols = MCXSymbol.objects.filter(option_type='XX')
        mcx_symbols.delete()
        return redirect('symbol_update')


def equity_symbols_upload(request):
    if request.method == "POST":
        equity_url = "https://public.fyers.in/sym_details/NSE_CM.csv"
        read_csv = pd.read_csv(equity_url, header=None)
        for index, row in read_csv.iterrows():
            new_equity_symbol = EquitySymbol(
                fytoken=row[0],
                symbol_details=row[1],
                exchange_instrument_type=row[2],
                minimum_lot_size=row[3],
                tick_size=row[4],
                isin=row[5],
                trading_session=row[6],
                last_update_date=row[7],
                expiry_date=row[8],
                symbol_ticker=row[9],
                exchange=row[10],
                segment=row[11],
                scrip_code=row[12],
                underlying_scrip_code=row[13],
                modifed_script_code=row[14],
                strike_price=row[15],
                option_type=row[16],
                exchange_token=row[17]
            )
            new_equity_symbol.save()
        return redirect('symbol_update')


def delete_equity_symbols(request):
    if request.method == 'POST':
        equity_symbols = EquitySymbol.objects.filter(option_type='XX')
        equity_symbols.delete()
        return redirect('symbol_update')
