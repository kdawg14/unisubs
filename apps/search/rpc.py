# Amara, universalsubtitles.org
#
# Copyright (C) 2013 Participatory Culture Foundation
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

from django.core.cache import cache
from django.core.paginator import Paginator
from django.template import RequestContext
from django.template.loader import render_to_string

from search.forms import SearchForm
from utils.rpc import add_request_to_kwargs
from videos.rpc import render_page

class SearchApiClass(object):
    def search(self, rdata, user):
        form = SearchForm(rdata)
        output = render_page(rdata.get('page', 1), form.queryset(), 20)
        output['sidebar'] = render_to_string('search/_sidebar.html', {
            'form': form,
            'rdata': rdata,
        })
        return output
