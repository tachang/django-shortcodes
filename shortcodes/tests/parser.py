from django.test import TestCase
from shortcodes.parser import parse

class TestParser(TestCase):


     def test_caption(self):
         parse("[caption a='1' b='2'][/caption] [caption]Simple caption[/caption] [caption a='1' b='2']")

     def test_gallery(self):
         parse("<p>[gallery ids=\"12916,12917,12918,12919,12920\"]</p>")


