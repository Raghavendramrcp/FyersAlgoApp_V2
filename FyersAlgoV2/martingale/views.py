# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import TemplateView, View
from django.http import HttpResponse, JsonResponse

from datetime import datetime, time

import requests

from home.models import Fyers_Access_Token, Fyers_Auth_Inputs, MCXSymbol, EquitySymbol
from home.fyersapi import FyerApiClass
# Create your views here.

def app_detail_model(pk):
    app_model = get_object_or_404(Fyers_Auth_Inputs, user_ass_id=pk)
    client_id = app_model.client_id
    return client_id

def access_token(pk):
    access_token_model = get_object_or_404(Fyers_Access_Token, app_ass_id=pk)
    access_token = access_token_model.auth_code
    return access_token



class Martingale_Homepage(View):

    template_name = 'martingale/martingalehomepage.html'

    def get(self, request, *args, **kwargs):

        client_id = app_detail_model(kwargs['pk'])
        access_token_value = access_token(kwargs['pk'])

        api_methods = FyerApiClass(client_id, access_token_value)

        user_profile = api_methods.user_profile()

        """ Below Code to Available Funds """

        funds = api_methods.available_funds()

        equity_stocks = EquitySymbol.objects.all()
        
        context = {
            'user_profile': user_profile,
            'funds': funds,
        }
        return render(request, self.template_name, context)


class EquityMartingale(View):
    template_name = 'martingale/martingalestocklist.html'


    def get_queryset(self):
        object = get_object_or_404(EquitySymbol, symbol_ticker=self.kwargs['commodity'])
        return object

    
    def get(self, request, pk, commodity):
        
        equity_symbol = self.get_queryset
        context = {
            'equity_symbol': equity_symbol
        }
        return render(request, self.template_name, context)

def Equity_Symbols_Martingale_View(request, pk):
    query = request.GET.get('q')
    qs = EquitySymbol.objects.all()
    if query is not None:
        lookups = Q(underlying_scrip_code__icontains=query)
        qs = EquitySymbol.objects.filter(lookups)
    context = {
        'object_list': qs,
    }
    return render(request, 'martingale/martingalestocklist.html', context)


class EquityMartingaleLogicView(View):

    template_name = 'martingale/martingalepage.html'

    

    def get(self, request, *args, **kwargs):
        symbol_ticker = get_object_or_404(EquitySymbol, symbol_ticker=self.kwargs['tickername'])
        

        # quantity tradeable 

        client_id = app_detail_model(kwargs['pk'])
        access_token_value = access_token(kwargs['pk'])
        api_methods = FyerApiClass(client_id, access_token_value)
        funds_available = api_methods.available_funds()
        


        # Order Book
        orders = []
        order_book = api_methods.orderbook()
        
        for order_value in order_book['orderBook']:
            if order_value['symbol'] == symbol_ticker.symbol_ticker:
                orders.append(order_value)

        
        context = {
            'ticker': symbol_ticker,
            'order_book': order_book,
            'orders': orders,
            'funds_available': funds_available,
        }
        return render(request, self.template_name, context)


def price_quote(request, pk, ticker):

    client_id = app_detail_model(pk)
    access_token_value = access_token(pk)

    api_methods = FyerApiClass(client_id, access_token_value)

    symbol_ticker_ = EquitySymbol.objects.get(symbol_ticker=ticker)
    symbol_ticker_ = symbol_ticker_.symbol_ticker
    quote = api_methods.get_quote(symbol_ticker_)

    return JsonResponse(quote, safe=False)


def equity_martingale_place_orders(request, pk, stockname):
    client_id = app_detail_model(pk)
    access_token_value = access_token(pk)

    api_methods = FyerApiClass(client_id, access_token_value)

    # stocksymbol = MCXSymbol.objects.get(symbol_ticker=stockname)

    # tick_size = stocksymbol.tick_size

    # round(self.tick_size*round((initial_upper_limit_ltp)/self.tick_size),2)

    if request.method=='POST':
        stocksymbol = EquitySymbol.objects.get(symbol_ticker=stockname)

        tick_size = stocksymbol.tick_size


        upper_price_initial_price = round(tick_size* round((float(request.POST['initial_upper_limit_order'])/tick_size)),2)
        upper_price_target_price = round(tick_size* round((float(request.POST['target_upper_limit_order'])/tick_size)),2) 
        lower_price_initial_price = round(tick_size* round((float(request.POST['initial_lower_limit_order'])/tick_size)),2) 
        lower_price_target_price = round(tick_size*round((float(request.POST['target_lower_limit_order'])/tick_size)),2) 
        quantity = int(request.POST['quantity'])

        initial_buy_order = api_methods.intraday_buy_stop_market_order(stocksymbol.symbol_ticker, quantity, upper_price_initial_price)

        place_initial_buy_order = api_methods.place_order(initial_buy_order)

        initial_sell_order = api_methods.intraday_sell_stop_market_order(stocksymbol.symbol_ticker, quantity, lower_price_initial_price)

        place_initial_sell_order = api_methods.place_order(initial_sell_order)

        target_buy_order = api_methods.intraday_buy_stop_limit_order(stocksymbol.symbol_ticker, quantity, lower_price_target_price, tick_size)

        place_target_buy_order = api_methods.place_order(target_buy_order)

        target_sell_order = api_methods.intraday_sell_stop_limit_order(stocksymbol.symbol_ticker, quantity, upper_price_target_price, tick_size)

        place_target_sell_order = api_methods.place_order(target_sell_order)

        
        
        context = {
                'upper_price_initial_order':upper_price_initial_price,
                'upper_price_target_order': upper_price_target_price,
                'lower_price_initial_order': lower_price_initial_price,
                'lower_price_targer_order': lower_price_target_price,
                'initial_buy_order': initial_buy_order,
                'initial_sell_order': initial_sell_order,
                'target_buy_order': target_buy_order,
                'target_sell_order': target_sell_order,
                'place_initial_buy_order': place_initial_buy_order,
                'place_initial_sell_order': place_initial_sell_order,
                'place_target_buy_order': place_target_buy_order,
                'place_target_sell_order': place_target_sell_order,
            }

        return JsonResponse(context)