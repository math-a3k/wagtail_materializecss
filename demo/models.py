from __future__ import unicode_literals

import os

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.html import format_html

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtailmedia.blocks import AbstractMediaChooserBlock

from wagtail_materializecss.blocks import MaterializePage, get_headings, get_components, \
    LinkBlock, Card, Collection, Carousel


class MediaChooserBlock(AbstractMediaChooserBlock):
    def render_basic(self, value, context=None):
        if not value:
            return ''

        if value.type == 'video':
            player_code = '''
            <div>
                <video controls preload="none" class="responsive-video">
                    <source src="{0}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            '''
            return format_html(player_code, value.file.url)
        else:
            ext = os.path.splitext(value.file.url)[-1].lower()[1:]
            player_code = '''
            <div>
                <audio controls preload="none">
                    <source src="{0}" type="audio/{1}">
                    Your browser does not support the audio element.
                </audio>
            </div>
            '''
        return format_html(player_code, value.file.url, ext)


class BloggerHomePage(MaterializePage):
    author = models.CharField(max_length=255)
    background_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    user_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')

    intro = RichTextField(blank=True)

    content_panels = MaterializePage.content_panels + [
        MultiFieldPanel([
            FieldPanel('author'),
            ImageChooserPanel('background_image'),
            ImageChooserPanel('user_image'),
            ], heading="Author Fields",),
        FieldPanel('intro', classname="full"),
    ]

    subpage_types = ['demo.BlogPage']

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context


class BlogPage(MaterializePage):
    date = models.DateField("Post date", default=timezone.now)
    description = RichTextField(blank=True)
    body = StreamField([
        *get_headings(exclude=['h1', 'h2']),
        ('paragraph', blocks.RichTextBlock(icon='pilcrow')),
        ('media', MediaChooserBlock(icon='media')),
        ('collection', Collection()),
        ('gallery', Carousel()),
        *get_components(),
    ])

    content_panels = MaterializePage.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('description', classname='full'),
            ], heading="Document Fields",),
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['demo.BloggerHomePage']

    @property
    def author(self):
        return self.get_parent().specific.author

    @property
    def user_image(self):
        return self.get_parent().specific.user_image
