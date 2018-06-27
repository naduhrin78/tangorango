from django import forms
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User


class CatForm(forms.ModelForm):
    name = forms.CharField(help_text="Please enter category name.", max_length=128)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(help_text='Please enter title of page.', max_length=128)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    url = forms.URLField(help_text='Please enter url of page', max_length=200)

    class Meta:
        model = Page
        exclude = ('category','slug',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://'+url
            cleaned_data['url'] = url

            return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture', )

