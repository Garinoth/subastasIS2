# -*- encoding: utf-8 -*-
from datetime import date
import re
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.forms import Form, ModelForm, EmailField, CharField, PasswordInput, DateField, BooleanField, ImageField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Textarea
from subastas.models import User, AuctionUser, Item, Auction, Offer, Bid, DateTimeField


default_error_messages = {
    'required': 'Este campo es obligatorio',
    'invalid': 'Este campo no es válido'
}


class UserForm(ModelForm):

    username = CharField(
        label='Nombre de usuario',
        error_messages=default_error_messages,
        max_length=30,
    )
    password = CharField(
        label='Contraseña',
        error_messages=default_error_messages,
        help_text='La contraseña debe ser de al menos 6 caracteres y contener letras, números y alguno de los siguientes caracateres: -+_!@#$%^&*.,?=',
        widget=PasswordInput,
    )
    confirm_password = CharField(
        label='Confirme su contraseña',
        error_messages=default_error_messages,
        help_text='La contraseña debe ser de al menos 6 caracteres y contener letras, números y alguno de los siguientes caracateres: -+_!@#$%^&*.,?=',
        widget=PasswordInput,
    )
    email = EmailField(
        label='Correo electrónico',
        error_messages=default_error_messages,
    )
    confirm_email = EmailField(
        label='Confirme su correo electrónico',
        error_messages=default_error_messages,
    )
    first_name = CharField(
        label='Nombre',
        error_messages=default_error_messages,
        max_length=30,
        required=False,
    )
    last_name = CharField(
        label='Apellidos',
        error_messages=default_error_messages,
        max_length=30,
        required=False,
    )

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'confirm_email',
                  'password',
                  'confirm_password',
                  'first_name',
                  'last_name']

    def __init__(self, *args, **kwargs):

        if kwargs.get('instance'):
            email = kwargs['instance'].email
            password = kwargs['instance'].password
            kwargs.setdefault('initial', {})['confirm_email'] = email
            kwargs.setdefault('initial', {})['confirm_password'] = password

        return super(UserForm, self).__init__(*args, **kwargs)

    def clean(self):

        if (self.cleaned_data.get('email') !=
            self.cleaned_data.get('confirm_email')):

            raise ValidationError(
                "Las direcciones de correo deben coincidir",
                code='confirm',
            )

        if (self.cleaned_data.get('password') !=
            self.cleaned_data.get('confirm_password')):

            raise ValidationError(
                "Las contraseñas deben coincidir",
                code='confirm',
            )

        password = self.cleaned_data.get('password')
        regex = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[-+_!@#$%^&*.,?=]).{6,}$'
        if password and not re.match(regex, password):
            raise ValidationError(
                code='invalid',
            )

        return self.cleaned_data


class AuctionUserForm(ModelForm):

    address = CharField(
        label='Dirección',
        max_length=100,
        widget=Textarea,
        required=False,
    )
    postal_code = CharField(
        label='Código Postal',
        max_length=5,
        required=False,
    )
    city = CharField(
        label='Ciudad',
        max_length=40,
        required=False,
    )
    country = CharField(
        label='País',
        max_length=40,
        required=False,
    )
    phone_number = CharField(
        label='Número de teléfono',
        max_length=20,
        required=False,
    )
    birth_date = DateField(
        label='Fecha de Nacimiento',
        error_messages=default_error_messages,
        widget=SelectDateWidget(years=range(date.today().year, 1920, -1)),
    )
    tos = BooleanField(
        error_messages={
            'required': 'Debe aceptar los Términos y Condiciones'},
    )

    class Meta:
        model = AuctionUser
        fields = ['birth_date',
                  'address',
                  'postal_code',
                  'city',
                  'country',
                  'phone_number']


class ItemForm(ModelForm):
    name = CharField(
        label='Nombre',
        error_messages=default_error_messages,
        max_length=100,
    )
    description = CharField(
        label='Descripción',
        error_messages=default_error_messages,
        widget=Textarea,
        required=False,
    )
    category = CharField(
        label='Categoría',
        error_messages=default_error_messages,
        max_length=100,
    )
    image = ImageField(
        label='Imagen',
        error_messages=default_error_messages,
        required=False,
    )

    class Meta:
        model = Item
        fields = ['name',
                  'description',
                  'category',
                  'image']


class AuctionForm(ModelForm):
    base_price = PositiveIntegerField(
        label='Precio base',
        error_messages=default_error_messages,
        default=0,
    )
    start_date = DateTimeField(
        label='Fecha de inicio',
        error_messages=default_error_messages,
    )
    end_date = DateTimeField(
        label='Fecha de fin',
        error_messages=default_error_messages,
    )

    class Meta:
        model = Auction
        fields = ['base_price',
                  'start_date',
                  'end_date']


class OfferForm(ModelForm):

    class Meta:
        model = Offer
        fields = ['price',
                  'end_date']


class BidForm(ModelForm):
    points = IntegerField(
        label='Puntos',
    )

    class Meta:
        model = Bid
        fields = ['points']


class ActivationForm(Form):
    email = EmailField(
        label='Correo electrónico',
    )
    password = CharField(
        label='Contraseña',
        widget=PasswordInput,
    )
    activation_key = CharField(max_length=40)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        activation_key = self.cleaned_data.get('activation_key')
        user = authenticate(email=email, password=password)
        if not user:
            raise ValidationError(
                "El usuario y la contraseña no son válidos"
            )
        auction_user = AuctionUser.objects.get(user=user)
        if auction_user.activation_key != activation_key:
            raise ValidationError(
                "La clave de activación no es válida",
            )

        return self.cleaned_data
