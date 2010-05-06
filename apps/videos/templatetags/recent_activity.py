# Universal Subtitles, universalsubtitles.org
# 
# Copyright (C) 2010 Participatory Culture Foundation
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see 
# http://www.gnu.org/licenses/agpl-3.0.html.

#  Based on: http://www.djangosnippets.org/snippets/73/
#
#  Modified by Sean Reifschneider to be smarter about surrounding page
#  link context.  For usage documentation see:
#
#     http://www.tummy.com/Community/Articles/django-pagination/

from django import template
from videos.models import VideoCaptionVersion, TranslationVersion
from django.conf import settings
from datetime import date
from django.utils.dateformat import format as date_format

register = template.Library()

def events_info_generator(events):
    for item in events:
        obj = {}
        if isinstance(item, TranslationVersion):
            obj['language'] = item.language.get_language_display()
            obj['video'] = item.language.video
        else:
            obj['video'] = item.video
        obj['user'] = item.user
        try:
            obj['profile'] = obj['user'].profile_set.all()[0]
        except IndexError:
            pass
        if item.datetime_started.date() == date.today():
            format = 'g:i A'
        else:
            format = 'g:i A, j M Y'
        obj['time'] = date_format(item.datetime_started, format)    
        yield obj

@register.inclusion_tag('videos/_recent_activity.html')
def recent_activity(user=None):
    LIMIT = settings.RECENT_ACTIVITIES_ONPAGE
    
    video_caption_qs = VideoCaptionVersion.objects.select_related().order_by('-datetime_started')
    trans_verion_qs = TranslationVersion.objects.select_related().order_by('-datetime_started')
    
    if user:
        video_caption_qs = video_caption_qs.filter(user=user)
        trans_verion_qs = trans_verion_qs.filter(user=user)
        
    events = list(video_caption_qs[:LIMIT])
    events.extend(trans_verion_qs[:LIMIT])
    events.sort(key = lambda event: event.datetime_started, reverse=True)
    events = events[:LIMIT]
    
    return {
        'events': events_info_generator(events)
    }