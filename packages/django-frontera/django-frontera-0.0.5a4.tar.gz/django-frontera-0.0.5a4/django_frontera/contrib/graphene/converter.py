from modelcluster.contrib.taggit import ClusterTaggableManager, TaggableManager
from wagtail.core.fields import StreamField


@convert_django_field.register(ClusterTaggableManager)
def convert_cluster_taggable_manager(field, registry=None):
    return graphene.String()


@convert_django_field.register(TaggableManager)
def convert_taggable_manager(field, registry=None):
    return graphene.String()


@convert_django_field.register(StreamField)
def convert_stream_field(field, registry=None):
    # Customization here
    return graphene.String()