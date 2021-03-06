from rest_framework import serializers
from .models import *


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class AcmeCustomerSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()

    def get_contacts(self, obj):
        return ContactSerializer(obj.contact).data

    class Meta:
        model = AcmeCustomer
        fields = '__all__'


class AcmeOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcmeOrderStatus
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()

    def get_location(self, loc):
        return {
            'latitude': loc.latitude,
            'longitude': loc.longitude,
        }

    class Meta:
        model = Location
        fields = ('address', 'location')


class AcmeOrderSerializer(serializers.ModelSerializer):
    customer_info = serializers.SerializerMethodField()
    address_from = serializers.SerializerMethodField()
    address_to = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    parcels_info = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    delivery_status = serializers.SerializerMethodField()
    delivery_period = serializers.SerializerMethodField()

    def get_customer_info(self, obj):
        return AcmeCustomerSerializer(obj.customer).data

    def get_address_from(self, obj):
        return LocationSerializer(obj.start_location).data

    def get_address_to(self, obj):
        return LocationSerializer(obj.end_location).data

    def get_delivery_period(self, obj):
        return {
            'start': obj.scheduled_time_start_time,
            'end': obj.scheduled_time_end_time
        }

    def get_status(self, obj):
        order_statuses = AcmeOrderStatus.objects.filter(order_id=obj.pk)
        current_status = order_statuses.order_by('created_on').last()
        return current_status.status if current_status is not None else None

    def get_delivery_status(self, obj):
        order_delivery = OrderDelivery.objects.filter(order_id=obj.pk).get()
        return order_delivery.delivery_status if order_delivery is not None else None

    def get_parcels_info(selfself, obj):
        parcels = Parcel.objects.filter(order_id=obj.pk)
        parcels_info = []
        for parcel in parcels:
            parcel_info = {
                'id': parcel.pk,
                'weight': parcel.weight,
                'dimensions': {
                    'x': parcel.dimension[0],
                    'y': parcel.dimension[1],
                    'z': parcel.dimension[2],
                },
                'shape': parcel.shape,
                'description': "No description provided."
            }
            parcels_info.append(parcel_info)
        return parcels_info

    def get_description(self, obj):
        return obj.comment

    class Meta:
        model = AcmeOrder
        fields = ('id', 'delivery_period', 'priority', 'address_from', 'address_to', 'description', 'parcels_info',
                  'customer_info', 'status', 'delivery_status', )


class AcmeUserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer()

    class Meta:
        model = AcmeUser
        fields = ('id', 'avatar', 'contacts')


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class AcmeDeliveryOperatorSerializer(serializers.ModelSerializer):
    operator = AcmeUserSerializer()
    location = LocationSerializer()
    assigned_orders_count = serializers.SerializerMethodField('assigned_count')
    in_progress_orders_count = serializers.SerializerMethodField('in_progress_count')

    def user_info(self, obj: DeliveryOperator):
        for user in AcmeUser.objects.all():
            if user.id == obj.operator.id:
                return AcmeUserSerializer(user).data

    def in_progress_count(self, obj: DeliveryOperator):
        orders = OrderDelivery.objects.all()
        count = 0

        for order in orders:
            if obj.id == order.delivery_operator_id and order.delivery_status == 'in_progress':
                count += 1
        return count

    def assigned_count(self, obj: DeliveryOperator):
        orders = OrderDelivery.objects.all()
        count = 0

        for order in orders:
            if obj.id == order.delivery_operator_id:
                count += 1
        return count

    class Meta:
        model = DeliveryOperator
        fields = ('operator', 'assigned_orders_count', 'in_progress_orders_count', 'location')


class AcmeOrderDeliverySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    address_from = serializers.SerializerMethodField()
    address_to = serializers.SerializerMethodField()
    delivery_period = serializers.SerializerMethodField()

    def get_delivery_period(self, obj):
        return {
            'start': obj.order.scheduled_time_start_time,
            'end': obj.order.scheduled_time_end_time
        }

    def get_priority(self, obj):
        return obj.order.priority

    def get_id(self, obj):
        return obj.order_id

    def get_address_from(self, obj):
        return LocationSerializer(obj.start_location).data

    def get_address_to(self, obj):
        return LocationSerializer(obj.end_location).data

    class Meta:
        model = OrderDelivery
        fields = ('id', 'delivery_period', 'priority', 'address_from', 'address_to', 'delivery_status')
