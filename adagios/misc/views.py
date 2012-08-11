# -*- coding: utf-8 -*-
#
# Copyright 2010, Pall Sigurdsson <palli@opensource.is>
#
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.template import RequestContext
import forms

import pynag.Model

from time import mktime
from datetime import datetime
from os.path import dirname

def index(request):
    c = {}
    return render_to_response('frontpage.html', c, context_instance = RequestContext(request))

def settings(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'GET':
        c['form'] = forms.AdagiosSettingsForm(initial=request.GET)
    else:
        c['form'] = forms.AdagiosSettingsForm(data=request.POST)
        if c['form'].is_valid():
            c['form'].save()
    return render_to_response('settings.html', c, context_instance = RequestContext(request))

def contact_us( request ):
    """ Bring a small form that has a "contact us" form on it """
    c={}
    c.update(csrf(request))
    if request.method == 'GET':
        form = forms.ContactUsForm(initial=request.GET)
    else:
        form = forms.ContactUsForm(data=request.POST)
        if form.is_valid():
            form.save()
            c['thank_you'] = True
            c['sender'] = form.cleaned_data['sender']
        
    c['form'] = form
    return render_to_response('contact_us.html', c,  context_instance = RequestContext(request))

def nagios(request):
    c = {}
    return render_to_response('nagios.html', c, context_instance = RequestContext(request))

def gitlog(request):
    """ View that displays a nice log of previous git commits in dirname(config.cfg_file) """
    c = { }
    c['errors'] = []
    configdir = dirname( pynag.Model.config.cfg_file or '/etc/nagios/')
    c['configdir'] = configdir
    try:
        import git
        repo = git.Repo(configdir)
        c['commits'] = repo.commits()
        commit_id = request.GET.get('commit', None)
        for commit in c['commits']:
            if commit.id == commit_id:
                c['commit'] = commit
    except ImportError:
        c['errors'].append('Could not import python module git. Make sure your system has package python-git installed.' )
    except git.InvalidGitRepositoryError:
        c['errors'].append("'%s' does not seem to be a git repository. No log created." % configdir)
    return render_to_response('gitlog.html', c, context_instance = RequestContext(request))
