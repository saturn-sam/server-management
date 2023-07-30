from django.forms import ModelForm
from django.db.models import Q
from .models import KBTopic, KnowledgeBase
from django.core.exceptions import ValidationError

class KBCreateForm(ModelForm):
    class Meta:
        model = KnowledgeBase
        fields = ['title', 'related_service','body','status','topic','tags']

    def __init__(self,*args, **kwargs):
        super(KBCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        title = self.cleaned_data.get('title')
        if KnowledgeBase.objects.filter(title=title).exists():
            raise ValidationError(f'KB with Title  "{title}" alredy exists. Please change the title.')

class KBEditForm(ModelForm):
    class Meta:
        model = KnowledgeBase
        fields = ['title', 'related_service','body','status','topic','tags']

    def __init__(self,*args, **kwargs):
        self.pk=kwargs['instance'].pk
        super(KBEditForm, self).__init__(*args, **kwargs)

    def clean(self):
        title = self.cleaned_data.get('title')
        if KnowledgeBase.objects.filter(~Q(pk=self.pk),title=title).exists():
            raise ValidationError(f'KB with Title  "{title}" alredy exists. Please change the title.')

class KBTopicAddForm(ModelForm):
    class Meta:
        model = KBTopic
        fields = ['title']

    def __init__(self,*args, **kwargs):
        super(KBTopicAddForm, self).__init__(*args, **kwargs)

    def clean(self):
        title = self.cleaned_data.get('title')
        if KBTopic.objects.filter(title=title).exists():
            raise ValidationError(f'KB Title with Title "{title}" alredy exists. Please change the title.')
