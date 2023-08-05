from djangoldp.views import LDPViewSet
from .models import Resource, Step
from djangoldp_i18n.views import I18nLDPViewSet

class ValidatedResourcesByStepViewSet(I18nLDPViewSet):
  model = Resource

  def get_queryset(self, *args, **kwargs):
    step_id = self.kwargs['id']
    # if hasattr(self.request.user, 'contributor_profile'):
    #   target='contributor'
    # elif hasattr(self.request.user, 'searcher_profile'):
    #   target='searcher'
    # else:
    #   target='public'

    # Additional filter criteria: , target__value=target
    return super().get_queryset(*args, **kwargs)\
          .filter(steps__in=step_id, review__status='validated')\
          .exclude(submitter__username=self.request.user.username)

class PendingResourcesViewSet(I18nLDPViewSet):
  model = Resource

  def get_queryset(self, *args, **kwargs):
    # Deactivating those additional filters for now.
    # , language__in=self.request.user.contributor_profile.languages.all(), fields__in=self.request.user.contributor_profile.fields.all()
    return super().get_queryset(*args, **kwargs)\
          .filter(review__status='pending')\
          .exclude(submitter__username=self.request.user.username)