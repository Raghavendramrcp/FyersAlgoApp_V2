from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView


from .models import Fyers_Access_Token, Fyers_Auth_Inputs, MCXSymbol, CurrencySymbol, EquitySymbol
from .forms import Fyers_Access_TokenForm
# Create your views here.


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
