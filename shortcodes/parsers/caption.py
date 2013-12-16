import uuid
from wordpress.models import *
from django.template import Template, Context
from django.template.loader import render_to_string
from django.conf import settings
from itertools import izip_longest

def parse(kwargs, template_name='shortcodes/caption.html'):
    print kwargs

    context = Context({
    })
    return render_to_string(template_name, context)
