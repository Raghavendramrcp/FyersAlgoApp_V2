from django.urls import path
from .views import HomePageView, AccessTokenView, delete_auth_code
from .views import HomePageView, AccessTokenView, delete_auth_code, SymbolUploadView, currency_symbol_upload, delete_currency_symbols, mcx_symbols_upload, delete_mcx_symbols, equity_symbols_upload, delete_equity_symbols


urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('access-token/<int:pk>/',  AccessTokenView.as_view(), name='access_token'),
    path('delete-auth_code/<int:pk>/', delete_auth_code, name='delete_auth_code'),
    path('upload_symbol/', SymbolUploadView.as_view(), name='symbol_update'),
    path('currency_symbol', currency_symbol_upload, name='currency_update'),
    path('currency_delete', delete_currency_symbols, name='currency_delete'),
    path('mcx_symbol_upload', mcx_symbols_upload, name='mcx_update'),
    path('mcx_delete', delete_mcx_symbols, name='mcx_delete'),
    path('equity_symbol_upload', equity_symbols_upload, name='equity_update'),
    path('equity_delete', delete_equity_symbols, name='equity_delete'),
]
