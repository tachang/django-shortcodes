import uuid
import re
from bs4 import BeautifulSoup

from wordpress.models import *
from django.template import Template, Context
from django.template.loader import render_to_string
from django.conf import settings
from itertools import izip_longest


def parse(kwargs, text, template_name='shortcodes/caption.html', **additional_kwargs):
	soup = BeautifulSoup(text)

	image_anchor_html = str(soup.a)
	image_width = soup.a.img['width']

	# To get the caption text I need to remove the shortcode and just get the main text.
	# This is just plain ugly and results in '] caption text['
	caption_text_with_brackets = re.compile(r"\].*\[").findall(soup.text)[0]

	# Remove the right and left square brackets and whitespace
	caption_text = caption_text_with_brackets.strip('[] ')

	context = Context({
		'image_anchor_html' : image_anchor_html,
		'caption_text' : caption_text,
		'image_width' : image_width
	})
	return render_to_string(template_name, context)