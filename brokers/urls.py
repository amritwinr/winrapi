from django.urls import path
from brokers.views import (
    side_bar,
    add_broker_creds,
    add_finvasia_broker_creds,
    broker_list,
    broker_status,
    place_order_by_master,
    place_order_by_finvasia_master,
    check_credentials,
    fin_copy_test
)

app_name = 'brokers'
urlpatterns = [
    path('side_bar', side_bar.SideBarView.as_view(), name="side-bar"),
    path('add_broker_creds', add_broker_creds.BrokerStore.as_view(), name="add-broker-creds"),
    path('add_finvasia_broker_creds', add_finvasia_broker_creds.BrokerStore.as_view(), name="add_finvasia_broker_creds"),
    path('broker_list', broker_list.BrokerListView.as_view(), name="broker-list"),
    path('update_broker_status', broker_status.BrokerStatusView.as_view(), name="update-broker-status"),
    path('update_broker_quantity', add_broker_creds.AddBrokerQuantityView.as_view(), name="update-broker-quantity"),
    path('update_finvasia_broker_quantity', add_finvasia_broker_creds.AddBrokerQuantityView.as_view(), name="update_finvasia_broker_quantity"),

    path('place_orders_by_master', place_order_by_master.PlaceOrderByMaster.as_view(), name="place-order-by-master"),
    path('place_order_by_finvasia_master', place_order_by_finvasia_master.PlaceOrderByMaster.as_view(), name="place_order_by_finvasia_master"),
    path('check_credentials', check_credentials.CheckCred.as_view(), name="check_credentials"),
    path('fin_copy_test', fin_copy_test.CheckCred.as_view(), name="fin_copy_test"),
]
