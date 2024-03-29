# Create your views here.
from django.http import HttpResponseRedirect
from usertraits.models import Trait, TraitRelationship
import logging
logger = logging.getLogger(__name__)



def add_trait_relationships(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=%s'%request.path)
    

    values = []
    #get the list of anwers
    for key in request.POST:
        if key.find('answer') > -1:
            values.append(request.POST[key])
          
            
    
    for v in values:
        ans = v.split('_')[1]
        tid = v.split('_')[0]
        trait = Trait.objects.get(id=tid)
        if TraitRelationship.objects.filter(trait=trait,user=request.user).count() == 0:
            print('creating relationship between' + str(trait.name))
            TraitRelationship.objects.create(trait=trait,user=request.user,relationship=ans)
        else:
            print('reset relationship between' + str(trait.name))
            TraitRelationship.objects.filter(trait=trait,user=request.user).delete()
            TraitRelationship.objects.create(trait=trait,user=request.user,relationship=ans)

    return HttpResponseRedirect('/user_details/' + str(request.user.id) + '/')

    
def get_user_traits(user):
    traits = []
    for t in Trait.objects.all():
        if TraitRelationship.objects.filter(trait=t,user=user).count() > 0:

            print(str(TraitRelationship.objects.filter(trait=t,user=user).count()))
            tr = TraitRelationship.objects.get(trait=t,user=user)
            print(tr.relationship)
#            except:
#                print('no trait')
#                logger.error('error in geting trait relationship. perhaps more than one?')
            t.value = tr.relationship
        traits.append(t)
    return traits