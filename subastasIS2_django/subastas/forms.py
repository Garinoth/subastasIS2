from datetime import date
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm, EmailField, CharField, PasswordInput, DateField, BooleanField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Textarea
from subastas.models import User, AuctionUser, Item, Auction, Offer, Bid


class UserForm(ModelForm):

    password = CharField(
        widget=PasswordInput,
    )
    confirm_password = CharField(
        widget=PasswordInput,
    )
    confirm_email = EmailField()

    class Meta:
        model = User
        fields = ['username',
                  'password',
                  'first_name',
                  'last_name',
                  'email']

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
                "Email addresses must match."
            )

        if (self.cleaned_data.get('password') !=
            self.cleaned_data.get('confirm_password')):

            raise ValidationError(
                "Passwords must match."
            )

        if (len(self.cleaned_data.get('password')) < 6):

          raise ValidationError(
                "Passwords must be at least 6 characters long."
            )

        return self.cleaned_data


class AuctionUserForm(ModelForm):

    birth_date = DateField(
        widget=SelectDateWidget(years=range(date.today().year, 1920, -1)),
    )
    address = CharField(
        max_length=100,
        widget=Textarea,
        required=False,
    )
    tos = BooleanField(
        error_messages={'required': 'You must accept the terms and conditions'},
    )

    class Meta:
        model = AuctionUser
        fields = ['address',
                  'postal_code',
                  'city',
                  'country',
                  'birth_date',
                  'phone_number']


class ItemForm(ModelForm):

    class Meta:
        model = Item
        fields = ['name',
                  'description',
                  'image',
                  'category']


class AuctionForm(ModelForm):

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

    class Meta:
        model = Bid
        fields = ['user',
                  'auction',
                  'points']

class ActivationForm(Form):
    email = EmailField()
    password = PasswordInput()
    activation_key = CharField(max_length=40)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        activation_key = self.cleaned_data.get('activation_key')
        user = authenticate(email=email,password=password)
        if user is None:
            raise ValidationError(
                activation_form.error_messages['invalid_login'],
                code='invalid_login',
            )
        if user.activation_key != activation_key:
            raise ValidationError(
                activation_form.error_messages['invalid_key'],
                code='invalid_key',
            )

        return self.cleaned_data