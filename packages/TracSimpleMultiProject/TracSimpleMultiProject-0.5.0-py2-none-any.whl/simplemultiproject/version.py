# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Thomas Doering
#

# smp
from simplemultiproject.model import *

# trac
from trac.attachment import AttachmentModule
from trac.config import ExtensionOption
from trac.core import *
from trac.ticket.model import Version, Ticket, TicketSystem
from trac.ticket.roadmap import apply_ticket_permissions, get_ticket_stats, ITicketGroupStatsProvider, \
    DefaultTicketGroupStatsProvider
from trac.ticket.query import QueryModule
from trac.mimeview import Context
from trac import __version__ as VERSION
from trac.util.translation import _, tag_
from trac.util.datefmt import parse_date, utc, to_utimestamp, \
    get_datetime_format_hint, format_date, \
    format_datetime, from_utimestamp
from api import IRoadmapDataProvider

try:
    from trac.util.datefmt import user_time
except ImportError:
    def user_time(req, func, *args, **kwargs):
        """port from 1.0-stable"""
        if 'tzinfo' not in kwargs:
            kwargs['tzinfo'] = getattr(req, 'tz', None)
        return func(*args, **kwargs)

from trac.web.api import IRequestHandler, IRequestFilter, ITemplateStreamFilter
from trac.web.chrome import add_link, add_notice, add_script, add_stylesheet, \
    add_warning, Chrome, INavigationContributor

# genshi
from genshi.builder import tag
from genshi.filters.transform import Transformer

# python
from datetime import datetime, timedelta
from pkg_resources import resource_filename
from operator import itemgetter
import re
from simplemultiproject.session import get_filter_settings

def get_tickets_for_any(env, db, any_name, any_value, field='component'):
    cursor = db.cursor()
    fields = TicketSystem(env).get_ticket_fields()
    if field in [f['name'] for f in fields if not f.get('custom')]:
        cursor.execute("""SELECT id,status,%s FROM ticket WHERE %s=%%s ORDER BY %s""" %
                       (field, any_name, field), [any_value])
    else:
        cursor.execute("""SELECT id,status,value FROM ticket
                          LEFT OUTER JOIN ticket_custom ON (id=ticket AND name=%%s)
                          WHERE %s=%%s ORDER BY value""" % any_name, [field, any_value])
    tickets = []
    for tkt_id, status, fieldval in cursor:
        tickets.append({'id': tkt_id, 'status': status, field: fieldval})
    return tickets


def any_stats_data(env, req, stat, any_name, any_value, grouped_by='component', group=None):
    has_query = env[QueryModule] is not None

    def query_href(extra_args):
        if not has_query:
            return None
        args = {any_name: any_value, grouped_by: group, 'group': 'status'}
        args.update(extra_args)
        return req.href.query(args)

    return {'stats': stat,
            'stats_href': query_href(stat.qry_args),
            'interval_hrefs': [query_href(interval['qry_args']) for interval in stat.intervals]
            }


class SmpVersionProject(Component):
    """Create Project dependent versions"""

    implements(IRequestHandler, IRequestFilter, ITemplateStreamFilter, IRoadmapDataProvider)

    stats_provider = ExtensionOption('roadmap', 'stats_provider',
                                     ITicketGroupStatsProvider,
                                     'DefaultTicketGroupStatsProvider',
                                     """Name of the component implementing `ITicketGroupStatsProvider`,
        which is used to collect statistics on groups of tickets for display
        in the roadmap views.""")

    def __init__(self):
        self.__SmpModel = SmpModel(self.env)

    # IRequestHandler methods
    def match_request(self, req):
        match = re.match(r'/version(?:/(.+))?$', req.path_info)
        if match:
            if match.group(1):
                req.args['id'] = match.group(1)
            return True

    def process_request(self, req):
        version_id = req.args.get('id')

        db = self.env.get_read_db()
        action = req.args.get('action', 'view')
        try:
            version = Version(self.env, version_id)
        except:
            version = Version(self.env)
            version.name = version_id
            action = 'edit'  # rather than 'new' so that it works for POST/save

        if req.method == 'POST':
            if req.args.has_key('cancel'):
                if version.exists:
                    req.redirect(req.href.version(version.name))
                else:
                    req.redirect(req.href.roadmap())
            elif action == 'edit':
                return self._do_save(req, db, version)
            elif action == 'delete':
                self._do_delete(req, version)
        elif action in ('new', 'edit'):
            return self._render_editor(req, db, version)
        elif action == 'delete':
            return self._render_confirm(req, db, version)

        if not version.name:
            req.redirect(req.href.roadmap())

        return self._render_view(req, db, version)

    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if data and 'is_SMP' in data and req.path_info.startswith('/version'):  # #12371
            version = data['version']
            if version and (type(version) is Version):
                project_name = self.__SmpModel.get_project_version(version.name)
                if project_name and project_name[0]:
                    self.__SmpModel.check_project_permission(req, project_name[0])
        return template, data, content_type

    # IRoadmapDataProvider

    def add_data(self, req, data):

        hide = []
        if get_filter_settings(req, 'roadmap', 'smp_hideversions'):
            hide.append('versions')
        if get_filter_settings(req, 'roadmap', 'smp_hidemilestones'):
            hide.append('milestones')
        if get_filter_settings(req, 'roadmap', 'smp_hideprojdesc'):
            hide.append('projectdescription')

        if data and hide:
            data['hide'] = hide

        if data and (not hide or 'versions' not in hide):
            versions, version_stats = self._versions_and_stats(req, None)  # filter_projects)
            data['versions'] = versions
            data['version_stats'] = version_stats

        if data and hide and 'milestones' in hide:
            data['milestones'] = []
            data['milestone_stats'] = []

        return data

    def filter_data(self, req, data):
        return data

    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):

        if filename == "version_edit.html":
            filter_ = Transformer('//form[@id="edit"]/div[1]')
            action = req.args.get('action', 'view')
            if action == 'new':
                return stream | filter_.before(self.__new_project(req))
            elif action == 'edit':
                return stream | filter_.before(self.__edit_project(data, req))

        return stream

    # Internal methods

    def __edit_project(self, data, req):
        version = data.get('version').name
        all_projects = self.__SmpModel.get_all_projects_filtered_by_conditions(req)
        id_project_version = self.__SmpModel.get_id_project_version(version)

        if id_project_version != None:
            id_project_selected = id_project_version[0]
        else:
            id_project_selected = None

        return tag.div(
            tag.label(
                'Project:',
                tag.br(),
                tag.select(
                    tag.option(),
                    [tag.option(row[1], selected=(id_project_selected == row[0] or None), value=row[0]) for row in
                     sorted(all_projects, key=itemgetter(1))],
                    name="project")
            ),
            class_="field")

    def __new_project(self, req):
        all_projects = self.__SmpModel.get_all_projects_filtered_by_conditions(req)

        return tag.div(
            tag.label(
                'Project:',
                tag.br(),
                tag.select(
                    tag.option(),
                    [tag.option(row[1], value=row[0]) for row in sorted(all_projects, key=itemgetter(1))],
                    name="project")
            ),
            class_="field")

    def _do_delete(self, req, version):
        req.perm.require('MILESTONE_DELETE')
        version_name = version.name
        version.delete()

        self.__SmpModel.delete_version_project(version_name)

        add_notice(req, _('The version "%(name)s" has been deleted.',
                          name=version_name))
        req.redirect(req.href.roadmap())

    def _do_save(self, req, db, version):
        version_name = req.args.get('name')
        version_project = req.args.get('project')
        old_version_project = self.__SmpModel.get_id_project_version(version.name)

        if version.exists:
            req.perm.require('MILESTONE_MODIFY')
        else:
            req.perm.require('MILESTONE_CREATE')

        old_name = version.name
        new_name = version_name

        version.description = req.args.get('description', '')

        time = req.args.get('time', '')
        if time:
            version.time = user_time(req, parse_date, time, hint='datetime')
        else:
            version.time = None

        # Instead of raising one single error, check all the constraints and
        # let the user fix them by going back to edit mode showing the warnings
        warnings = []

        def warn(msg):
            add_warning(req, msg)
            warnings.append(msg)

        # -- check the name
        # If the name has changed, check that the version doesn't already
        # exist
        # FIXME: the whole .exists business needs to be clarified
        #        (#4130) and should behave like a WikiPage does in
        #        this respect.
        try:
            new_version = Version(self.env, new_name, db)
            if new_version.name == old_name:
                pass  # Creation or no name change
            elif new_version.name:
                warn(_('Version "%(name)s" already exists, please '
                       'choose another name.', name=new_version.name))
            else:
                warn(_('You must provide a name for the version.'))
        except:
            version.name = new_name

        if warnings:
            return self._render_editor(req, db, version)

        # -- actually save changes

        if version.exists:
            version.update()

            if old_name != version.name:
                self.__SmpModel.rename_version_project(old_name, version.name)

            if not version_project:
                self.__SmpModel.delete_version_project(version.name)
            elif not old_version_project:
                self.__SmpModel.insert_version_project(version.name, version_project)
            else:
                self.__SmpModel.update_version_project(version.name, version_project)
        else:
            version.insert()
            if version_project:
                self.__SmpModel.insert_version_project(version.name, version_project)

        add_notice(req, _('Your changes have been saved.'))
        req.redirect(req.href.version(version.name))

    def _render_confirm(self, req, db, version):
        req.perm.require('MILESTONE_DELETE')

        version = [v for v in Version.select(self.env)
                   if v.name != version.name
                   and 'MILESTONE_VIEW' in req.perm]
        data = {
            'version': version
        }
        return 'version_delete.html', data, None

    def _render_editor(self, req, db, version):
        # Suggest a default due time of 18:00 in the user's timezone
        default_time = datetime.now(req.tz).replace(hour=18, minute=0, second=0,
                                                    microsecond=0)
        if default_time <= datetime.now(utc):
            default_time += timedelta(days=1)

        data = {
            'version': version,
            'datetime_hint': get_datetime_format_hint(),
            'default_time': default_time
        }

        if version.exists:
            req.perm.require('MILESTONE_MODIFY')
            versions = [v for v in Version.select(self.env)
                        if v.name != version.name and 'MILESTONE_VIEW' in req.perm]
        else:
            req.perm.require('MILESTONE_CREATE')

        Chrome(self.env).add_wiki_toolbars(req)
        return 'version_edit.html', data, None

    def _render_view(self, req, db, version):
        version_groups = []
        available_groups = []
        component_group_available = False
        ticket_fields = TicketSystem(self.env).get_ticket_fields()

        # collect fields that can be used for grouping
        for field in ticket_fields:
            if field['type'] == 'select' and field['name'] != 'version' \
                    or field['name'] in ('owner', 'reporter'):
                available_groups.append({'name': field['name'],
                                         'label': field['label']})
                if field['name'] == 'component':
                    component_group_available = True

        # determine the field currently used for grouping
        by = None
        if component_group_available:
            by = 'component'
        elif available_groups:
            by = available_groups[0]['name']
        by = req.args.get('by', by)

        tickets = get_tickets_for_any(self.env, db, 'version', version.name, by)
        tickets = apply_ticket_permissions(self.env, req, tickets)
        stat = get_ticket_stats(self.stats_provider, tickets)

        context = Context.from_request(req)

        if VERSION <= '0.12':
            infodivclass = 'info'
        else:
            infodivclass = 'info trac-progress'

        data = {
            'context': context,
            'version': version,
            'attachments': AttachmentModule(self.env).attachment_data(context),
            'available_groups': available_groups,
            'grouped_by': by,
            'groups': version_groups,
            'infodivclass': infodivclass,
            'is_SMP': True
        }
        data.update(any_stats_data(self.env, req, stat, 'version', version.name))

        if by:
            groups = []
            for field in ticket_fields:
                if field['name'] == by:
                    if 'options' in field:
                        groups = field['options']
                        if field.get('optional'):
                            groups.insert(0, '')
                    else:
                        cursor = db.cursor()
                        cursor.execute("""
                            SELECT DISTINCT COALESCE(%s,'') FROM ticket
                            ORDER BY COALESCE(%s,'')
                            """, [by, by])
                        groups = [row[0] for row in cursor]

            max_count = 0
            group_stats = []

            for group in groups:
                values = group and (group,) or (None, group)
                group_tickets = [t for t in tickets if t[by] in values]
                if not group_tickets:
                    continue

                gstat = get_ticket_stats(self.stats_provider, group_tickets)
                if gstat.count > max_count:
                    max_count = gstat.count

                group_stats.append(gstat)

                gs_dict = {'name': group}
                gs_dict.update(any_stats_data(self.env, req, gstat,
                                              'version', version.name, by, group))
                version_groups.append(gs_dict)

            for idx, gstat in enumerate(group_stats):
                gs_dict = version_groups[idx]
                percent = 1.0
                if max_count:
                    percent = float(gstat.count) / float(max_count) * 100
                gs_dict['percent_of_max_total'] = percent

        add_stylesheet(req, 'common/css/roadmap.css')
        add_script(req, 'common/js/folding.js')
        return 'version_view.html', data, None

    @staticmethod
    def _version_time(version):
        if version.time:
            return version.time.replace(tzinfo=None).strftime('%Y%m%d%H%M%S')
        else:
            return datetime(9999, 12, 31).strftime('%Y%m%d%H%M%S') + version.name

    def _versions_and_stats(self, req, filter_projects):
        req.perm.require('MILESTONE_VIEW')

        versions = Version.select(self.env)
        db = self.env.get_read_db()

        filtered_versions = []
        stats = []

        show = req.args.getlist('show')

        for version in sorted(versions, key=lambda v: self._version_time(v)):
            project = self.__SmpModel.get_project_version(version.name)
            version.due = None
            version.completed = None
            if not filter_projects or (project and project[0] in filter_projects):
                if not version.time or version.time.replace(tzinfo=None) >= datetime.now() or 'completed' in show:
                    if version.time:
                        if version.time.replace(tzinfo=None) >= datetime.now():
                            version.due = version.time
                        else:
                            version.completed = version.time

                    filtered_versions.append(version)
                    tickets = get_tickets_for_any(self.env, db, 'version', version.name,
                                                  'owner')
                    tickets = apply_ticket_permissions(self.env, req, tickets)
                    stat = get_ticket_stats(self.stats_provider, tickets)
                    stats.append(any_stats_data(self.env, req, stat,
                                                'version', version.name))

        return filtered_versions, stats

######################################################################################################################
#     Everything below this point is (c) Cinc
######################################################################################################################

# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Cinc
#
# License: 3-clause BSD
#

from smp_model import SmpVersion
from genshi import HTML
from trac.web.chrome import Chrome
from admin_filter import SmpFilterDefaultVersionPanels


class SmpVersionModule(Component):
    """Module to keep version information for projects up to date when SmpFilterDefaultVersionPanel is deactivated."""
    implements(IRequestFilter, ITemplateStreamFilter)

    def __init__(self):
        self.smp_model = SmpVersion(self.env)
        self.version_tmpl = Chrome(self.env).load_template("roadmap_versions.html")
        # CSS class for milestones and versions
        if VERSION <= '0.12':
            self.infodivclass = 'info'
        else:
            self.infodivclass = 'info trac-progress'

    # IRequestFilter methods

    def pre_process_request(self, req, handler):
        if self._is_valid_request(req) and req.method == "POST":
            # Try to delete only if version page filter is disabled. Deleting is usually done there.
            if not self.env.enabled[SmpFilterDefaultVersionPanels]:
                if 'remove' in req.args:
                    # 'Remove' button on main version panel
                    self.smp_model.delete(req.args.get('sel'))
                elif 'save' in req.args:
                    # 'Save' button on 'Manage version' panel
                    p_ids = req.args.get('sel')
                    self.smp_model.delete(req.args.get('path_info'))
                    self.smp_model.add_after_delete(req.args.get('name'), p_ids)
        return handler

    @staticmethod
    def _is_valid_request(req):
        """Check request for correct path and valid form token"""
        if req.path_info.startswith('/admin/ticket/versions') and req.args.get('__FORM_TOKEN') == req.form_token:
            return True
        return False

    def post_process_request(self, req, template, data, content_type):
        return template, data, content_type

    # ITemplateStreamFilter methods

    def filter_stream(self, req, method, filename, stream, data):

        if filename == 'roadmap.html':
            # Add button to create new versions
            filter_ = Transformer('//div[@class="buttons"][2]')
            stream = stream | filter_.append(HTML('<form action="%s" method="get"><div>'
                                                  '<input type="hidden" value="new" name="action"/>'
                                                  '<input value="Add new Version" type="submit">'
                                                  '</div></form>' % req.href.version()))
            # Change label to include versions
            filter_ = Transformer('//label[@for="showcompleted"]')
            stream = stream | filter_.replace(HTML('<label for="showcompleted">Show completed milestones and '
                                                   'versions</label>'))
            # Add additional checkboxes to preferences
            data['smp_render'] = 'prefs'
            filter_ = Transformer('//form[@id="prefs"]')
            stream = stream | filter_.prepend(self.version_tmpl.generate(**data))

            # Add versions to page
            if 'smp_groupproject' not in data:  # Roadmap group plugin is grouping by project
                data['infodivclass'] = self.infodivclass
                data['smp_render'] = 'versions'  # Specify part of template to be rendered
                filter_ = Transformer('//div[@class="milestones"]')
                stream = stream | filter_.after(self.version_tmpl.generate(**data))

        return stream
