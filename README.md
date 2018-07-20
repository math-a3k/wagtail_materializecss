# wagtail_materializecss

Style your wagtail pages with materializecss!

Run the demo project to see how it in action.

### Includes
  * Demo project to show how you may want to style a page
  * Component blocks
    * Badge
    * Breadcrumb
    * Button
    * Card
    * Collection
    * FAB
    * Footer
    * Icon
    * links
    * Navbar
    * Preloader
    * Scrollspy (table of contents)
  * MaterializePage with base.html
    * Default page variables to style the navbar and footer
    * Additionally includes Abstract models Navbar and Footer
  * Functions to get common components for StreamFields
    * get_headings(exclude=None) - Return h1, h2, h3, h4, h5, h6 tags with scrollspy table of contetns support
    * get_components(exclude=None) - Returns blocks for Card, Collection, Button, Icon, ...
    * get_footer_blocks(exclude=None) - Returns common components that someone might want in a footer.


## Example Page

![Example Page](./example_page.PNG)

![Example Admin](example_admin.PNG)

```python
from django.db import models
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.blocks import RichTextBlock

from wagtail_materializecss.models import MaterializePage, get_headings, get_components
from wagtail_materializecss.components import Collection


class BloggerHomePage(MaterializePage):
    author = models.CharField(max_length=255)
    background_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    user_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')

    body = StreamField([
        *get_headings(exclude=['h6']),
        ('paragraph', RichTextBlock(icon='pilcrow')),
        ('collection', Collection()),
        *get_components(),
    ])

    content_panels = MaterializePage.content_panels + [
        MultiFieldPanel([
            FieldPanel('author'),
            ImageChooserPanel('background_image'),
            ImageChooserPanel('user_image'),
            ], heading="Author Fields",),
        FieldPanel('intro', classname="full"),
    ]
```

Template
```djangotemplate
{% extends "wagtail_materializecss/base.html" %}
{% load static wagtailcore_tags wagtailimages_tags wagtail_materializecss_tags %}

{% block body_class %}template-bloggerhomepage{% endblock %}

{% block before_container %}
    <div class="row">
        {% image page.background_image original as page_image %}
        <div class='hero-image' style="background-image: url('{{ page_image.url }}')"></div>
    </div>
{% endblock %}

{% block content %}
    <div class="row">
        <div class="col s12 m4 right" style="margin-top: 1rem;">
            {% image page.user_image fill-200x200 class="responsive-img circle center-object" %}
            <h3 class="center-object {{ page.color }}-text">{{ page.author }}</h3>
        </div>
        <div class="col s12 m8">
            <h1 class="{{ page.color }}-text scrollspy">Introduction</h1>
            {% include_block page.body %}
        </div>
    </div>

    <div class="row">
        <h5>Posts</h5>
        <div class="divider"></div>
        {% for post in blogpages %}
            <div class="col s12 m6 l4">
                {% make_link None "Go to Post" post.specific as post_link %}
                {% make_card post.specific.title post.specific.description post_link size='small' %}
            </div>
        {% endfor %}
    </div>
{% endblock %}
```
