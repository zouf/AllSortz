from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from privatebeta.forms import InviteRequestForm
from privatebeta.models import InviteRequest
import logging
import random
import string


logger = logging.getLogger(__name__)

def invite(request, form_class=InviteRequestForm, template_name="privatebeta/invite.html", extra_context=None):
    """
    Allow a user to request an invite at a later dte by entering their email address.
    
    **Arguments:**
    
    ``template_name``
        The name of the tempalte to render.  Optional, defaults to
        privatebeta/invite.html.

    ``extra_context``
        A dictionary to add to the context of the view.  Keys will become
        variable names and values will be accessible via those variables.
        Optional.
    
    **Context:**
    
    The context will contain an ``InviteRequestForm`` that represents a
    :model:`invitemelater.InviteRequest` accessible via the variable ``form``.
    If ``extra_context`` is provided, those variables will also be accessible.
    
    **Template:**
    
    :template:`privatebeta/invite.html` or the template name specified by
    ``template_name``.
    """
    
    form = form_class(request.POST or None)
    if form.is_valid():
        email = form['email']
       
        email = request.POST['email']
        
        InviteRequest.objects.create(email=email,invited=False)
        mail = EmailMessage('Invite Request', 'User with email ' + str(email) + 'requested access. ', to=['matt@allsortz.com'])
        mail.send()
        #end_mail('Invite Request', 'Welcome to AllSortz. Go to http://www.allsortz.com/accounts/register to register!', 'matt@allsortz.com',
        #          [email], fail_silently=False)
        #accept(email)
        return render_to_response('privatebeta/sent.html',RequestContext(request))

    context = {'form': form}
    #context['key'] = "".join([random.choice(string.letters+string.digits) for x in range(1, 10)])

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template_name, context,
        context_instance=RequestContext(request))

def accept(email):
    
    try:
        ir = InviteRequest.objects.get(email=email)
        ir.invited = True
        ir.save() 
        mail = EmailMessage('Welcome to AllSortz should never be called!', 'Go to http://www.allsortz.com/accounts/register/\
            to register your account\n\n\n - The AllSortz Team ', to=[ir.email])
        mail.send()
 
        
    except:
        logger.ERROR('Invalid invite request')
        print('error invalid invite request')
   
   
def signupreq(request):
    return render_to_response('privatebeta/signuprequired.html',  context_instance=RequestContext(request))


def sent(request, template_name="privatebeta/sent.html", extra_context=None):
    """
    Display a message to the user after the invite request is completed
    successfully.
    
    **Arguments:**
    
    ``template_name``
        The name of the tempalte to render.  Optional, defaults to
        privatebeta/sent.html.

    ``extra_context``
        A dictionary to add to the context of the view.  Keys will become
        variable names and values will be accessible via those variables.
        Optional.
    
    **Context:**
    
    There will be nothing in the context unless a dictionary is passed to
    ``extra_context``.
    
    **Template:**
    
    :template:`privatebeta/sent.html` or the template name specified by
    ``template_name``.
    """
    return direct_to_template(request, template=template_name, extra_context=extra_context)
