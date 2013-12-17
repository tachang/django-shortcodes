import uuid
from wordpress.models import *
from django.template import Template, Context
from django.template.loader import render_to_string
from django.conf import settings
from itertools import izip_longest


def parse(kwargs, text, template_name='shortcodes/gallery.html', **additional_kwargs):

    if 'ids' not in kwargs:
      return ""

    ids = kwargs.get('ids').split(',')

    images  = []

    for id in ids:
    	post = Post.objects.get(pk=id)

    	image = {
			'medium' : post.get_attached_image('medium'),
			'full' : post.get_attached_image()
    	}
    	images.append(image)

    imagegroups = list( izip_longest(*(iter(images),) * 3) )

    context = Context({
    	'imagegroups' : imagegroups,
    	'uuid' : uuid.uuid4()
    })
    return render_to_string(template_name, context)
