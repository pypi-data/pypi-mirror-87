# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Thomas Doering, falkb
#

from genshi.builder import tag
from genshi.filters.transform import Transformer
from trac.ticket.model import Ticket
from simplemultiproject.model import *
from trac.util.text import to_unicode
from trac.util.html import Markup, unescape
from trac.core import *
from trac.web.api import IRequestFilter, ITemplateStreamFilter
from operator import itemgetter
from simplemultiproject.model import smp_filter_settings

class SmpTimelineProjectFilter(Component):
    """Allows for filtering by 'Project'
    """
    _old_render_fn = []
    _current_project = []
    _read_idx = -1
    
    implements(IRequestFilter, ITemplateStreamFilter)
    
    def __init__(self):
        self.__SmpModel = SmpModel(self.env)

    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        return handler
        
    def post_process_request(self, req, template, data, content_type):
        if template == 'timeline.html':
            filter_off = False
            displayed_projects = self._filtered_projects(req)
            if not displayed_projects: #no filter means likely more than 1 project, so we insert the project name
                filter_off = True
                displayed_projects = [project[1] for project in self.__SmpModel.get_all_projects()]

            if displayed_projects:
                filtered_events = []
                tickettypes = ("newticket", "editedticket", "closedticket", "attachment", "reopenedticket")
                self._old_render_fn = []
                self._current_project = []
                self._read_idx = -1
                for event in data['events']:
                    if event['kind'] in tickettypes:
                        resource = event['kind'] == "attachment" and event['data'][0].parent or event['data'][0]
                        if resource.realm == "ticket":
                            ticket = Ticket( self.env, resource.id )   
                            project = ticket.get_value_or_default('project')
                            if not project:
                                if filter_off: #display all tickets without a set project
                                    filtered_events.append(event)
                            elif project in displayed_projects:
                                if len(displayed_projects) > 1: #only if more than 1 filtered project
                                    #store the old render function and the project to be inserted
                                    self._old_render_fn.append(event['render'])
                                    self._current_project.append(project)
                                    #redirect to our new render function (which will insert the project name)
                                    event['render'] = self._render_ticket_event
                                #add to the list of displayed events
                                filtered_events.append(event)
                        elif resource.realm == "wiki":
                            filtered_events.append(event)
                    else:
                        filtered_events.append(event)
    
                data['events'] = filtered_events

        return template, data, content_type

    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):
        if filename == 'timeline.html':
            filter_projects = self._filtered_projects(req) 

            filter = Transformer('//form[@id="prefs"]/div[1]')
            stream = stream | filter.before(tag.label("Filter Projects:")) | filter.before(tag.br()) | filter.before(self._projects_field_input(req, filter_projects)) | filter.before(tag.br()) | filter.before(tag.br())

        return stream

    # Internal
    def _render_ticket_event(self, field, context):
        if (field == 'url'):
            self._read_idx += 1 #next index now

        if self._read_idx < len(self._old_render_fn):
            #call the original render function
            output = self._old_render_fn[self._read_idx](field, context)
    
            if field == 'title': #now it's time to insert the project name
                #split the whole string until we can insert
                splitted_output = to_unicode(output).split("</em>")
                tooltip = splitted_output[0].split('\"')
                ticket_no = splitted_output[0].split('>')
                if len(tooltip) == 3: #it's a ticket
                    #now rebuild the puzzle by inserting the name
                    ticket_summary = unescape(Markup(tooltip[1]))
                    msg_text = unescape(Markup(splitted_output[1]))
                    proj = self._current_project[self._read_idx]
                    output = tag('Ticket' + ' ', tag.em(ticket_no[1], title=ticket_summary), ' ', tag.span(proj, style="background-color: #ffffd0;"), msg_text)
                elif len(tooltip) == 1 and len(splitted_output) == 3: #it's an attachment
                    output += tag(' ', tag.span(self._current_project[self._read_idx], style="background-color: #ffffd0;"))
            return output

    def _projects_field_input(self, req, selectedcomps):
        cursor = self.__SmpModel.get_all_projects_filtered_by_conditions(req)

        sorted_project_names_list = sorted(cursor, key=itemgetter(1))
        number_displayed_entries = len(sorted_project_names_list)+1     # +1 for special entry 'All'
        if number_displayed_entries > 15:
            number_displayed_entries = 15

        select = tag.select(name="filter-projects", id="filter-projects", multiple="multiple", size=("%s" % number_displayed_entries), style="overflow:auto;")
        select.append(tag.option("All", value="All"))
        
        for component in sorted_project_names_list:
            project = to_unicode(component[1])
            if selectedcomps and project in selectedcomps:
                select.append(tag.option(project, value=project, selected="selected"))
            else:
                select.append(tag.option(project, value=project))
        return select
        
    def _filtered_projects(self, req):
        filtered_projects = smp_filter_settings(req, 'timeline', 'projects')

        return filtered_projects
