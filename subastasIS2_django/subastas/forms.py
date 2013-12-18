# -*- encoding: utf-8 -*-
import datetime
import re
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.forms import Form, ModelForm, EmailField, CharField, PasswordInput, DateField, BooleanField, ImageField, IntegerField, HiddenInput
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Textarea
from django.utils import timezone
from subastas.models import User, AuctionUser, Item, Auction, Offer, Bid


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
        if 'email' in self.cleaned_data and 'confirm_email' in self.cleaned_data:
            if (self.cleaned_data.get('email') !=
                self.cleaned_data.get('confirm_email')):

                self._errors['email'] = [
                    "Las direcciones de correo deben coincidir"]
                self._errors['confirm_email'] = [
                    "Las direcciones de correo deben coincidir"]

        if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data:
            if (self.cleaned_data.get('password') !=
                self.cleaned_data.get('confirm_password')):

                self._errors['password'] = [
                    "Las contraseñas deben coincidir"]
                self._errors['confirm_password'] = [
                    "Las contraseñas deben coincidir"]

        password = self.cleaned_data.get('password')
        regex = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[-+_!@#$%^&*.,?=]).{6,}$'
        if password and not re.match(regex, password):
            self._errors['password'] = ["Contraseña mal formada"]

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
        widget=SelectDateWidget(
            years=range(datetime.date.today().year, 1920, -1)),
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


class ItemForm(ModelForm):
    name = CharField(
        label='Nombre',
        error_messages=default_error_messages,
        max_length=40,
    )
    description = CharField(
        label='Descripción',
        error_messages=default_error_messages,
        widget=Textarea,
        max_length=140,
        required=False,
    )
    category = CharField(
        label='Categoría',
        error_messages=default_error_messages,
        max_length=40,
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
    start_date = DateField(
        label='Fecha de inicio',
        error_messages=default_error_messages,
        widget=SelectDateWidget,
    )
    end_date = DateField(
        label='Fecha de fin',
        error_messages=default_error_messages,
        widget=SelectDateWidget,
    )

    class Meta:
        model = Auction
        fields = ['start_date',
                  'end_date']

    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if start_date < datetime.date.today():
            raise ValidationError(
                "La fecha de inicio no puede ser anterior a hoy"
            )

        if start_date >= end_date:
            raise ValidationError(
                "La fecha de inicio debe ser anterior a la de fin"
            )

        return self.cleaned_data


class OfferForm(ModelForm):
    price = IntegerField(
        label='Precio',
        error_messages=default_error_messages,
    )

    end_date = DateField(
        label='Fecha de fin',
        error_messages=default_error_messages,
        widget=SelectDateWidget,
    )

    class Meta:
        model = Offer
        fields = ['price',
                  'end_date']


class BidForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.auction = kwargs.pop('auction', None)
        super(BidForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bid
        fields = []

    def clean(self):
        auction_user = AuctionUser.objects.get(user=self.user)
        if self.auction.end_date < timezone.now():
            raise ValidationError(
                "Esta subasta ya ha finalizado."
            )

        if auction_user == self.auction.winner:
            raise ValidationError(
                "Ya eres el ganador actual, no puedes volver a pujar."
            )

        if auction_user.auction_points <= 0:
            raise ValidationError(
                'recharge'
            )

        return self.cleaned_data


class SaleForm(Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.offer = kwargs.pop('offer', None)
        super(SaleForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.offer.end_date < timezone.now():
            raise ValidationError(
                "Esta oferta ya ha finalizado."
            )

        if self.offer.sold:
            raise ValidationError(
                "Este producto ya ha sido vendido."
            )

        auction_user = AuctionUser.objects.get(user=self.user)
        if auction_user == self.offer.item.owner:
            raise ValidationError(
                "Eres el dueño del producto, no puedes comprarlo."
            )

        if auction_user.offer_points < self.offer.price:
            raise ValidationError(
                "No tienes suficientes puntos acumulados para adquirir este producto. Sigue pujando para obtener puntos.",
            )

        return self.cleaned_data


class UpdateAuctionUserForm(ModelForm):
    class Meta:
        model = AuctionUser
        fields = ['description',
                  'interests']
