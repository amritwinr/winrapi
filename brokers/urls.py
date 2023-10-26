from django.urls import path
from brokers.views import (
    side_bar,
    check_credentials,
    place_order_by_master
)

from brokers.views.Strategy import (
    add_romil_broker,
    strategy
)

from brokers.views.TradingView import (
    add_finvasia_trading_view,
    trading_view,
)

from brokers.views.Telegram import (
    telegram,
    add_telegram
)

from brokers.views.Brokers import (
    add_broker_creds,
    add_finvasia_broker_creds,
    broker_list,
    broker_status,
    add_angel_broker_creds,
    add_upstox_broker_creds,
    add_fyers_broker_creds,
    add_flattrade_broker_creds,
    add_5paisa_broker_creds,
)

from brokers.views.PlaceOrder import (
    place_order_by_finvasia_master,
    place_order_by_angel_master,
    place_order_by_upstox_master,
    place_order_by_5paisa_master
)

app_name = 'brokers'
urlpatterns = [
    path('side_bar', side_bar.SideBarView.as_view(), name="side-bar"),

    # to create brokers
    path('add_broker_creds', add_broker_creds.BrokerStore.as_view(),
         name="add-broker-creds"),
    path('add_finvasia_broker_creds', add_finvasia_broker_creds.BrokerStore.as_view(
    ), name="add_finvasia_broker_creds"),
    path('add_angel_broker_creds', add_angel_broker_creds.BrokerStore.as_view(
    ), name="add_angel_broker_creds"),
    path('add_upstox_broker_creds', add_upstox_broker_creds.BrokerStore.as_view(
    ), name="add_upstox_broker_creds"),
    path('add_fyers_broker_creds', add_fyers_broker_creds.BrokerStore.as_view(
    ), name="add_fyers_broker_creds"),
    path('add_flattrade_broker_creds', add_flattrade_broker_creds.BrokerStore.as_view(
    ), name="add_flattrade_broker_creds"),
    path('add_5paisa_broker_creds', add_5paisa_broker_creds.BrokerStore.as_view(
    ), name="add_5paisa_broker_creds"),

    # get broker list
    path('broker_list', broker_list.BrokerListView.as_view(), name="broker-list"),

    # update brokers data like quantity and status
    path('update_broker_status', broker_status.BrokerStatusView.as_view(),
         name="update-broker-status"),
    path('update_broker_quantity', add_broker_creds.AddBrokerQuantityView.as_view(
    ), name="update-broker-quantity"),
    path('update_finvasia_broker_quantity', add_finvasia_broker_creds.AddBrokerQuantityView.as_view(
    ), name="update_finvasia_broker_quantity"),
    path('update_angel_broker_quantity', add_angel_broker_creds.AddBrokerQuantityView.as_view(
    ), name="update_angel_broker_quantity"),
    path('update_upstox_broker_quantity', add_upstox_broker_creds.AddBrokerQuantityView.as_view(
    ), name="update_upstox_broker_quantity"),
    path('update_fyers_broker_quantity', add_fyers_broker_creds.AddBrokerQuantityView.as_view(
    ), name="update_fyers_broker_quantity"),
    path('update_flattrade_broker_quantity', add_flattrade_broker_creds.AddBrokerQuantityView.as_view(
    ), name="update_flattrade_broker_quantity"),
    path('update_5paisa_broker_quantity', add_5paisa_broker_creds.AddBrokerQuantityView.as_view(
    ), name="update_5paisa_broker_quantity"),
    path('update_romil_broker_quantity', add_romil_broker.AddBrokerQuantityView.as_view(
    ), name="update_5paisa_broker_quantity"),

    # place order
    path('place_orders_by_master', place_order_by_master.PlaceOrderByMaster.as_view(
    ), name="place-order-by-master"),
    path('place_order_by_finvasia_master', place_order_by_finvasia_master.PlaceOrderByFinvasiaMaster.as_view(
    ), name="place_order_by_finvasia_master"),
    path('place_order_by_angel_master', place_order_by_angel_master.PlaceOrderByAngelMaster.as_view(
    ), name="place_order_by_angel_master"),
    path('place_order_by_upstox_master', place_order_by_upstox_master.PlaceOrderByUpstoxMaster.as_view(
    ), name="place_order_by_upstox_master"),
    path('place_order_by_5paisa_master', place_order_by_5paisa_master.PlaceOrderBy5paisaMaster.as_view(
    ), name="place_order_by_5paisa_master"),

    # check credentials
    path('check_credentials', check_credentials.CheckCred.as_view(),
         name="check_credentials"),

    # trading View (create and update data)
    path('add_finvasia_trading_view', add_finvasia_trading_view.BrokerStore.as_view(
    ), name="add_finvasia_trading_view"),
    path('tradingView', trading_view.FinvasiaTradingView.as_view(),
         name="tradingView"),
    path('update_finvasia_trading_view', add_finvasia_trading_view.AddBrokerQuantityView.as_view(
    ), name="update_finvasia_trading_view"),

    # telegram for view and add
    path('telegram', telegram.Telegram.as_view(),
         name="telegram"),
    path('add_telegram', add_telegram.BrokerStore.as_view(), name="add_telegram"),

    # strategy
    path('strategy', strategy.Strategy.as_view(), name="strategy"),
    # get broker details for romil only in strategy
    path('add_romil_broker', add_romil_broker.BrokerStore.as_view(
    ), name="add_5paisa_broker_creds"),
]
