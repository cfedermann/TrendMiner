"""
Django forms for the MUSING Service reputation application.

Defines the views for the MUSING Service reputation section.

"""
from django import forms
from django.utils.translation import ugettext_lazy as _


class RateCompanyForm(forms.Form):
    """ Form class for rate company operation. """
    source_url = forms.CharField(
      label=_(u'Source URL'),
      widget=forms.TextInput(attrs={'size': '80'}),
      required=True,
      help_text=_(u'Enter the URL of the source data (a ZIP file) here.'),
    )
