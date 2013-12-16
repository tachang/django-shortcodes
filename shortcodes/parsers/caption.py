import uuid
from django.template import Template, Context
from django.template.loader import render_to_string
from django.conf import settings

def parse(kwargs, template_name='shortcodes/gallery.html'):

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
