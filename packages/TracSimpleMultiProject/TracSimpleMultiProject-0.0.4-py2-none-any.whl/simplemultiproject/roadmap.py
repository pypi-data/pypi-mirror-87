# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Christopher Paredes
#

from genshi.builder import tag
from genshi.filters.transform import Transformer
from genshi.input import HTML
from trac.util.text import to_unicode
from trac.core import *
from trac.web.api import IRequestFilter, ITemplateStreamFilter
from trac.web.chrome import add_stylesheet
from operator import itemgetter
from trac.wiki.formatter import wiki_to_html
from simplemultiproject.model import *
from simplemultiproject.model import smp_filter_settings, smp_settings
from trac import __version__ as VERSION
from simplemultiproject.smp_model import SmpProject, SmpMilestone

__all__ = ['SmpRoadmapProject', 'SmpRoadmapProjectFilter']

class SmpRoadmapProjectFilter(Component):
    """Allows for filtering by 'Project'
    """
    
    implements(IRequestFilter, ITemplateStreamFilter)
    
    def __init__(self):
        self.__SmpModel = SmpModel(self.env)

    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        return handler
        
    def post_process_request(self, req, template, data, content_type):
        if req.path_info.startswith('/roadmap'):
            filter_projects = smp_filter_settings(req, 'roadmap', 'projects')
                
            if data:
                if filter_projects and len(filter_projects) > 0:
                    milestones = data.get('milestones')
                    milestones_stats = data.get('milestone_stats')
                    
                    filtered_milestones = []
                    filtered_milestone_stats = []
            
                    if milestones:
                        for idx, milestone in enumerate(milestones):
                            milestone_name = milestone.name
                            project = self.__SmpModel.get_project_milestone(milestone_name)
        
                            if project and project[0] in filter_projects:
                                filtered_milestones.append(milestone)
                                filtered_milestone_stats.append(milestones_stats[idx])
            
                        data['milestones'] = filtered_milestones
                        data['milestone_stats'] = filtered_milestone_stats
                
                if VERSION <= '0.12':
                    data['infodivclass'] = 'info'
                else:
                    data['infodivclass'] = 'info trac-progress'

        return template, data, content_type

    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):
        if filename.startswith("roadmap"):
            filter_projects = smp_filter_settings(req, 'roadmap', 'projects')
            filter = Transformer('//form[@id="prefs"]/fieldset/div[1]')
            stream = stream | filter.before(tag.label("Filter Projects:")) | filter.before(tag.br()) | filter.before(self._projects_field_input(req, filter_projects)) | filter.before(tag.br())

        return stream

    # Internal

    def _projects_field_input(self, req, selectedcomps):
        cursor = self.__SmpModel.get_all_projects_filtered_by_conditions(req)

        sorted_project_names_list = sorted(cursor, key=itemgetter(1))
        number_displayed_entries = len(sorted_project_names_list)+1     # +1 for special entry 'All'
        if number_displayed_entries > 15:
            number_displayed_entries = 15

        select = tag.select(name="filter-projects", id="Filter-Projects", multiple="multiple", size=("%s" % number_displayed_entries), style="overflow:auto;")
        select.append(tag.option("All", value="All"))
        
        for component in sorted_project_names_list:
            project = component[1]
            if selectedcomps and project in selectedcomps:
                select.append(tag.option(project, value=project, selected="selected"))
            else:
                select.append(tag.option(project, value=project))

        return select

class SmpRoadmapProject(Component):
    """Groups milestones by 'Project'
    """
    
    implements(IRequestFilter, ITemplateStreamFilter)
    
    def __init__(self):
        self.__SmpModel = SmpModel(self.env)

    def pre_process_request(self, req, handler):
        return handler

    def __extract_div_milestones_array(self,tag_milestone,stream_milestones):
        html_milestones = stream_milestones.render()
        ini_index = html_milestones.find(tag_milestone)
        divarray = []
        ocurrencia = True
        while (ocurrencia):
            end_index = html_milestones.find(tag_milestone, ini_index + len(tag_milestone))
            if(end_index < 0):
                divarray.append(to_unicode(html_milestones[ini_index:len(html_milestones)]))
                ocurrencia = False
            else:
                divarray.append(to_unicode(html_milestones[ini_index:end_index]))
                ini_index = end_index
        return divarray

    def __process_div_projects_milestones(self,milestones,div_milestones_array, req):
        projects = self._map_milestones_to_projects(milestones)
        hide = smp_settings(req, 'roadmap', 'hide')
        show_proj_descr = False
        if hide is None or 'projectdescription' not in hide:
            show_proj_descr = True

        hide_closed = False
        filter_projects_setting = smp_settings(req, 'roadmap', 'filter-projects')
        if filter_projects_setting is None or 'All' in filter_projects_setting:
            hide_closed = True

        div_projects_milestones = ''
        
        for project_name in sorted(projects.keys()):
            has_access = True
            can_show = True
            if (project_name == "--None Project--"):
                div_project = '<br><div id="project"><fieldset><legend><h2>No Project</h2></legend>'
            else:
                project_info = self.__SmpModel.get_project_info(project_name)
                if project_info:
                    if hide_closed and project_info[4] > 0: # column 4 of table smp_project tells if project is closed
                        can_show = False
                    if self.__SmpModel.is_not_in_restricted_users(req.authname, project_info):
                        has_access = False

                div_project = '<br><div id="project"><fieldset><legend><b>Project </b> <em style="font-size: 12pt; color: black;">%s</em></legend>' % project_name
                if can_show and has_access and project_info and show_proj_descr:
                    div_project = div_project + '<div class="description" xml:space="preserve">'
                    if project_info[2]:
                        div_project = div_project + '%s<br/><br/>' % project_info[2]
                    
                    div_project = div_project + '%s</div>' % wiki_to_html(project_info[3], self.env, req)

            div_milestone = ''
            
            if has_access:            
                if can_show and len(projects[project_name]) > 0:

                    for milestone in projects[project_name]:
                        mi = '<em>%s</em>' % milestone
                        for i in range(len(div_milestones_array)):
                            if(div_milestones_array[i].find(mi)>0):
                                div_milestone = div_milestone + div_milestones_array[i]
                else:
                    div_milestone = '<em style="color: red;">no permission</em>'
                div_project = div_project + to_unicode(div_milestone) + '</fieldset></div>'
                div_projects_milestones = to_unicode(div_projects_milestones + div_project)

        stream_div_projects_milestones = HTML(div_projects_milestones)
        return stream_div_projects_milestones
        
    def _map_milestones_to_projects(self, milestones):
        projects = {}
        for milestone in milestones:
            project_name = self.__SmpModel.get_project_milestone(milestone)
            
            if project_name == None:
                project_name = self.__SmpModel.get_project_version(milestone)
            
            if project_name == None:
                if projects.has_key("--None Project--"):
                    projects["--None Project--"].append(milestone)
                else:
                    projects["--None Project--"] = [milestone]
            else:
                if projects.has_key(project_name[0]):
                    projects[project_name[0]].append(milestone)
                else:
                    projects[project_name[0]] = [milestone]
        
        return projects

    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):
        if filename.startswith("roadmap"):
            stream_roadmap = HTML(to_unicode(stream))
            stream_milestones = HTML(to_unicode(stream_roadmap.select('//div[@class="roadmap"]/div[@class="milestones"]')))
            
            milestones = data.get('milestones')
            milestones = [milestone.name for milestone in milestones]
            
            versions = data.get('versions')
            if versions:
                for version in versions:
                    milestones.append(version.name)

            div_milestones_array = self.__extract_div_milestones_array('<div class="milestone">',stream_milestones)
            
            div_projects_milestones = self.__process_div_projects_milestones(milestones, div_milestones_array, req)
            
            return stream_roadmap | Transformer('//div[@class="roadmap"]/div[@class="milestones"]').replace(div_projects_milestones)

        return stream

    def post_process_request(self, req, template, data, content_type):
        return template, data, content_type  


class SmpRoadmapPlugin(Component):

    implements(IRequestFilter)

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):

        if req.path_info.startswith('/roadmap-disabled'):
            if data:
                # ITemplateProvider is implemented in another component
                add_stylesheet(req, "simplemultiproject/css/simplemultiproject.css")
                # Some debug printing to be removed
                # for item in data:
                #     print repr(item)
                # print
                smp_milestone = SmpMilestone(self.env)
                for item in data.get('milestones'):
                    item.id_project = smp_milestone.get_project_ids_for_resource_item('milestone', item.name)
                    # print "Milestone: ", repr(item.name)
                    # print "   id_project: ", item.id_project

                # add project information for template
                smp_project = SmpProject(self.env)
                # The following list holds some duplicate project ids
                all_id_project = [id_p for ms, id_p in smp_milestone.get_all_milestones_and_id_project_id()]
                if 'emptyprojects' in req.args.get('hide', []):
                    # Remove all projects without a milestone
                    all_proj = [ proj for proj in smp_project.get_all_projects() if proj[0] in all_id_project]
                else:
                    all_proj = smp_project.get_all_projects()

                data.update({'projects': all_proj,
                            'hide': req.args.get('hide', []),
                            'show': req.args.get('show', []),
                            'projects_with_ms': all_id_project})

                if req.args.get('smp-grouping'):
                    data['grouping'] = req.args.get('smp-grouping')
                else:
                    data['grouping'] = 'group-no'

            return "smp_roadmap.html", data, content_type

        return template, data, content_type
