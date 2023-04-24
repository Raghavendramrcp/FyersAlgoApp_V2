from django.urls import path
from .views import (
    Martingale_Homepage,
    Equity_Symbols_Martingale_View,
    EquityMartingaleLogicView,
    price_quote,
    equity_martingale_place_orders,
)

urlpatterns = [
    path(
        "martingale_homepage/<int:pk>/",
        Martingale_Homepage.as_view(),
        name="martingale_homepage",
    ),
    path(
        "martingale_stocklist/<int:pk>/",
        Equity_Symbols_Martingale_View,
        name="marrtingale_stocklist",
    ),
    path(
        "martingale/<int:pk>/<str:tickername>/",
        EquityMartingaleLogicView.as_view(),
        name="equity_martingale",
    ),
    path("price_quote/<int:pk>/<str:ticker>/", price_quote, name="price_quote"),
    path(
        "martingale/placeorders/<int:pk>/<str:stockname>/",
        equity_martingale_place_orders,
        name="equity_place_orders",
    ),
]
