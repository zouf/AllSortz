'''
Created on Jul 9, 2012

@author: zouf
'''
from django.core.mail.message import EmailMessage
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from ratings.contexts import get_default_blank_context
import logging
import time

logger = logging.getLogger(__name__)

def feedback(request):
    if request.user.is_authenticated():
        context = get_default_blank_context(request.user)
        if request.method == 'POST':
            user = request.user
            content = request.POST['feedback']   

    
            mail = EmailMessage('AllSortz Feedback', '\nuname: '+str(user.username) + '\n firstname: ' + str(user.first_name) +  '\nlastname: ' + str(user.last_name) + '\nemail: ' +str(user.email)+ '\ntime: ' + str(time.asctime())+  '\n\n'+str(content), to=['mattzouf@gmail.com'])
            mail.send()
            logger.info('Feedback form user'+str(user.username))
            return redirect('/')
        else:
            return render_to_response('webadmin/feedback.html', context_instance=RequestContext(request,context))
 
 
 
def allsortz_help(request):
    context = get_default_blank_context(request.user)
    return render_to_response('webadmin/help.html',context_instance=RequestContext(request,context))

def allsortz_about(request):
    context = get_default_blank_context(request.user)
    return render_to_response('webadmin/about.html',context_instance=RequestContext(request,context))
