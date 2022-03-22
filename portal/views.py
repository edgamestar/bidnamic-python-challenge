from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, resolve
from django.utils.http import urlencode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from bidnamic.base_settings import BASE_DIR
# Create your views here.
from portal.models import Campaign, SearchTerm, AdGroup
from portal.tasks import import_campaigns, import_ad_groups, import_search_terms
from portal.utils import write_file, get_top_roas


def csrf_failure(request, reason=""):
    return redirect(reverse('auth', kwargs={'target': 'signin'}))


class CustomLoginRequiredMixin:
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'A login is required to proceed')
            url_query = {'next': request.get_full_path()}
            return redirect(f'{reverse("auth", kwargs={"target": "signin"})}?{urlencode(url_query)}')
        return super().dispatch(request, *args, **kwargs)


class AuthenticationView(View):
    """A class to handle all authentication requests"""
    context = {}
    data = {}
    user = None
    target = None

    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            self.user = request.user
        self.data = {'status': 400}
        self.target = kwargs.get('target', None)
        return super(AuthenticationView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.target == "signin":
            if self.user and self.user.is_authenticated:
                redirect('index')
        elif self.target == "signout":
            auth_logout(request)
            return redirect(reverse('auth', kwargs={'target': 'signin'}))
        return render(request, f'auth/{self.target}.html', self.context)

    def post(self, request, *args, **kwargs):
        self.data['response'] = self.target
        if self.target == "signin":
            username = request.POST.get('username').strip()
            password = request.POST.get('password').strip()

            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    request.session.set_expiry(86400)

                    auth_login(request, user)
                    next = request.POST.get('next', None)
                    if next:
                        resolved = resolve(next)

                        redirect_kwargs = {}
                        for key, value in resolved.kwargs.items():
                            if value:
                                redirect_kwargs[key] = value

                        next = reverse(resolved.url_name, kwargs=redirect_kwargs)
                    else:
                        next = reverse('index')

                    self.data['details'] = "Sign In Successful."
                    self.data['redirect'] = next
                    self.data['status'] = 200
                else:
                    self.data['details'] = "Inactive Account."
            else:
                self.data['details'] = "Verification Failed."

        return JsonResponse(self.data, safe=False, status=self.data['status'])


class IndexView(CustomLoginRequiredMixin, View):
    """A class to handle all frontend operations"""
    template_name = 'index.html'
    user = None
    context = None
    data = None
    target = None
    action = None

    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            self.user = request.user
        self.context = {}
        self.data = {'status': 400}
        self.target = kwargs.get('target', None)
        self.action = kwargs.get('action', None)

        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.context['campaigns_count'] = Campaign.objects.count()
        self.context['ad_groups_count'] = AdGroup.objects.count()
        self.context['search_terms_count'] = SearchTerm.objects.count()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        target_dict = {
            'campaigns': {
                'file_name': 'campaigns.csv',
                'function': import_campaigns,
            },
            'ad-groups': {
                'file_name': 'adgroups.csv',
                'function': import_ad_groups,
            },
            'search-terms': {
                'file_name': 'search_terms.csv',
                'function': import_search_terms,
            },
        }
        if self.target in ['campaigns', 'ad-groups', 'search-terms']:
            if self.action == 'upload':
                csv_file = request.FILES['csv']
                file_name = target_dict[self.target]['file_name']
                write_file(BASE_DIR / file_name, csv_file)
                self.data['details'] = f"{file_name} has been uploaded successfully."
                self.data['status'] = 200
            elif self.action == 'import':
                target_dict[self.target]['function'].apply_async(args=[self.user.email])
                self.data['details'] = f"Import will run in background.<br>An email will be sent to {self.user.email} upon completion."
                self.data['status'] = 200
        elif self.target == 'roas':
            if self.action == 'fetch':
                query = request.POST.get('query').strip()
                which = request.POST.get('which').strip()
                limit = int(request.POST.get('limit', 10))
                results = get_top_roas(which, query, limit)
                self.data['no-reset'] = True
                self.data['results'] = render_to_string('includes/results-table.html', {'results': results, 'which': which})
                self.data['status'] = 200
        return JsonResponse(self.data, safe=False, status=self.data['status'])


class ApiView(APIView):
    """A class to handle all api operations"""
    http_method_names = ['post']
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    user = None
    data = None
    status = None
    target = None
    action = None

    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            self.user = request.user
        self.data = {}
        self.status = 400
        self.target = kwargs.get('target', None)
        self.action = kwargs.get('action', None)
        return super(ApiView, self).dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if self.target == 'roas':
            if self.action == 'fetch':
                query = request.POST.get('query').strip()
                which = request.POST.get('which').strip()
                try:
                    limit = int(request.POST.get('limit').strip())
                except:
                    limit = 10
                if query and query != "":
                    if which and which != "":
                        results = get_top_roas(which, query, limit)
                        self.data['results'] = list(results)
                        self.status = 200
                    else:
                        self.data['detail'] = 'Please provide which'
                else:
                    self.data['detail'] = 'Please provide query'
        return Response(self.data, self.status)
