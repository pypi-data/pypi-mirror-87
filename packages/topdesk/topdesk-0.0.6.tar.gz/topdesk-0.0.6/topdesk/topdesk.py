"""Main topdesk module"""
import json
from functools import wraps

import requests

from topdesk import errors

def logged_in(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if not self.token and not self.app_creds:
            raise NotLoggedIn()
        return f(self, *args, **kwargs)
    return wrapper

class Topdesk():
    """
    The class for interacting with topdesk. Create an instance using a URL and
    an API key
    and start requesting!

    N.B.: The Knowledge Base API is currently not supported, because it uses
          GraphQL whereas the rest of the API uses REST.
    N.B.: The Supporting Files API is not yet supported.
    """

    def __init__(self, url, token=None, verify=None, app_creds=None):
        """
        Constructs a new Topdesk object.

        If you have a token from a valid session, you can reuse it here.
        Otherwise you’ll have to call one of the login methods before sending
        any other API requests. You can invalidate your token by calling logout.
        """
        self.token = token
        self.verify = verify
        self.app_creds = app_creds
        self.url = '{}/tas/api{{}}'.format(url)

    def _treat_id_or_num(self, id_or_number):
        """
        Internal helper function to determine whether a parameter is an ID or
        number.

        Currently it uses a dirty heuristic: all numbers seem to contain spaces,
        whereas IDs are regular UUIDs.
        """
        if ' ' in id_or_number:
            return 'number/{}'.format(id_or_number)
        return 'id/{}'.format(id_or_number)

    def request(self, scheme, url, data=None, params=None, extra=None):
        """
        Low-level request interface to topdesk. Takes a HTTP request scheme
        (lower case!), a URL to request (relative), and optionally data to add
        to the request. Either returns the JSON body of the request or raises a
        HttpException.
        """
        if extra is None:
            extra = {}

        url = self.url.format(url)
        headers = {
            'User-Agent':
                'topdesk Python wrapper: https://gitlab.com/wobcom/topdesk',
            'Content-Type': 'application/json',
        }
        if self.token is not None:
            headers['authorization'] = 'TOKEN id="{}"'.format(self.token)
        if self.app_creds is not None:
            extra['auth'] = self.app_creds
        # this is a nice little hack to make the API nicer
        # we pass the scheme as string, but have it as attributes in requests
        fn = requests.__getattribute__(scheme)

        res = fn(url, headers=headers, data=json.dumps(data), params=params,
                 verify=self.verify, **extra)

        if not res.ok:
            self._raise_exception(res.status_code, res)

        if not res.content:
            return None

        try:
            return res.json()
        except ValueError:
            return res.content

    def _raise_exception(self, code, res):
        raise errors.get_exception(code, res)

    def get(self, url, data=None, params=None, extra=None):
        """
        Low-level GET request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.
        """
        return self.request('get', url, data, params, extra)

    def put(self, url, data=None, params=None, extra=None):
        """
        Low-level PUT request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.
        """
        return self.request('put', url, data, params, extra)

    def post(self, url, data=None, params=None, extra=None):
        """
        Low-level POST request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.
        """
        return self.request('post', url, data, params, extra)

    def patch(self, url, data=None, params=None, extra=None):
        """
        Low-level PATCH request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.
        """
        return self.request('patch', url, data, params, extra)

    def delete(self, url, data=None, params=None, extra=None):
        """
        Low-level DELETE request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.
        """
        return self.request('delete', url, data, params, extra)

    def login_person(self, username, password):
        """
        Log in as a person.
        """
        token = self.get('/login/person',
                         extra={'auth': (username, password)})
        self.token = token.decode('ascii')

    def login_operator(self, username, password):
        """
        Log in as an operator.
        """
        token = self.get('/login/operator',
                         extra={'auth': (username, password)})
        self.token = token.decode('ascii')

    def logout(self):
        """
        Log out. Invalidates token.
        """
        res = self.get('/logout')
        self.token = None
        return res

    @logged_in
    def create_incident(self, data):
        """
        Create a new incident. Takes a lot of possible values; please refer to
        the topdesk API docs (https://developers.topdesk.com/documentation/index.html#api-Incident-CreateIncident)
        to find out more.
        """
        return self.post('/incidents', data=data)

    @logged_in
    def incident(self, id_or_number):
        """Get an incident by ID or number."""
        path = self._treat_id_or_num(id_or_number)
        return self.get('/incidents/{}'.format(path))

    @logged_in
    def incidents(self, params):
        """
        Get a list of incidents. Takes a lot of possible filters; please refer
        to the topdesk API (https://developers.topdesk.com/documentation/index.html#api-Incident-GetListOfIncidents)
        to find out more.
        """
        return self.get('/incidents', params=params)

    def _treat_incident(self, url_template, id_or_number, params):
        """
        Internal function that prepares incident API functions. Abstracts over
        IDs and numbers.
        """
        path = self._treat_id_or_num(id_or_number)
        return self.get(url_template.format(path), params)

    @logged_in
    def escalate_incident(self, id_or_number, reason_id=None):
        """
        Escalates an incident. Takes the ID of an escalation reason (might be
        optional, depending on context).
        """
        params = {
            'id': reason_id
        }
        return self._treat_incident('/incidents/id/{}/escalate', id_or_number,
                                   params=params)

    @logged_in
    def deescalate_incident(self, id_or_number, reason_id=None):
        """
        Deescalates an incident. Takes the ID of an escalation reason (might be
        optional, depending on context).
        """
        params = {
            'id': reason_id
        }
        return self._treat_incident('/incidents/id/{}/deescalate', id_or_number,
                                    params=params)

    @logged_in
    def archive_incident(self, id_or_number, reason_id=None):
        """
        Archives an incident. Takes the ID of an archive reason (might be
        optional, depending on context).
        """
        params = {
            'id': reason_id
        }
        return self._treat_incident('/incidents/id/{}/archive', id_or_number,
                                    params=params)

    @logged_in
    def unarchive_incident(self, id_or_number, unarchive_partials=True):
        """
        Unarchives an incident. Optional parameters
        - unarchive_partials: signals whether partial calls should also be
                              unarchived (defaults: true).
        """
        params = {
            'unarchive_partials': unarchive_partials
        }
        return self._treat_incident('/incidents/id/{}/unarchive', id_or_number,
                                    params=params)

    @logged_in
    def action_by_incident(self, incident_id_or_number, action_id,
                           inline_images=False):
        """
        Get an action by incident ID or number and action ID. Optional
        parameters:
        - inline_images: signals whether inline images should be included
                         (default: false).
        """
        path = self._treat_id_or_num(incident_id_or_number)
        params = {
            'inlineimages': inline_images
        }
        return self.get('/incidents/{}/actions/{}'.format(path, action_id),
                        params=params)

    @logged_in
    def incident_actions_by_incident(self, id_or_number, start=0,
                                     page_size=10, inline_images=False):
        """
        Get incident actions by incident ID or number. Takes the optional
        parameters `start`, `page_size`, and `inline_images`.
        """
        params = {
            'start': start,
            'page_size': page_size,
            'inlineimages': inline_images
        }
        return self._treat_incident('/incidents/id/{}/actions', id_or_number,
                                    params=params)

    @logged_in
    def progress_trail_by_incident(self, id_or_number, start=0, page_size=10,
                                   inline_images=False):
        """
        Get incident progress trail by incident ID or number. Takes the optional
        parameters `start`, `page_size`, and `inline_images`.
        """
        params = {
            'start': start,
            'page_size': page_size,
            'inlineimages': inline_images
        }
        return self._treat_incident('/incidents/id/{}/progresstrail',
                                    id_or_number, params=params)


    @logged_in
    def progress_trail_count_by_incident(self, id_or_number):
        """
        Get incident progress trail entry count by incident ID or number.
        """
        return self._treat_incident('/incidents/id/{}/progresstrail/count',
                                    id_or_number)

    @logged_in
    def requests_by_incident(self, id_or_number, start=0, page_size=10,
                             inline_images=False):
        """
        Get incident requests by incident ID or number. Takes the optional
        parameters `start`, `page_size`, and `inline_images`.
        """
        params = {
            'start': start,
            'page_size': page_size,
            'inlineimages': inline_images
        }
        return self._treat_incident('/incidents/id/{}/requests', id_or_number,
                                    params=params)

    @logged_in
    def incident_drop_down(self, tab, searchlist):
        """
        Get a list of optional drop-down values by tab and search list.
        """
        url = '/incidents/free_fields/{}/searchlists/{}'
        return self.get(url.format(tab, searchlist))

    @logged_in
    def register_incident_time(self, id_or_number, time):
        """
        Register time spent on an incident by ID or number in minutes.
        """
        path = self._treat_id_or_num(id_or_number)
        params = { 'timeSpent': time }
        return self.post('/incidents/{}/timespent'.format(path), params=params)

    @logged_in
    def incident_time(self, id_or_number):
        """
        Get time spent on an incident by ID or number in minutes.
        """
        return self._treat_incident('/incidents/{}/timespent', id_or_number)

    @logged_in
    def update_incident(self, id_or_number, data=None):
        """
        Update an incident by ID or number. Takes the same parameters as
        incident creation.
        """
        path = self._treat_id_or_num(id_or_number)
        return self.put('/incidents/{}'.format(path), data=data)

    @logged_in
    def budgetholders(self):
        """Get a list of budget holders"""
        return self.get('/budgetholders')

    @logged_in
    def call_types(self):
        """Get a list of call types"""
        return self.get('/incidents/call_types')

    @logged_in
    def categories(self):
        """Get a list of categories"""
        return self.get('/incidents/categories')

    @logged_in
    def closure_codes(self):
        """Get a list of closure codes"""
        return self.get('/incidents/closure_codes')

    @logged_in
    def countries(self):
        """Get a list of countries"""
        return self.get('/countries')

    @logged_in
    def durations(self):
        """Get a list of durations"""
        return self.get('/durations')

    @logged_in
    def entry_types(self):
        """Get a list of entry types"""
        return self.get('/entry_types')

    @logged_in
    def impacts(self):
        """Get a list of impacts"""
        return self.get('/impacts')

    @logged_in
    def priorities(self):
        """Get a list of priorities"""
        return self.get('/priorities')

    @logged_in
    def processing_status(self):
        """Get a list of processing stati"""
        return self.get('/incidents/statuses')

    @logged_in
    def archiving_reasons(self):
        """Get a list of archiving reasons"""
        return self.get('/archiving-reasons')

    @logged_in
    def deescalation_reasons(self):
        """Get a list of deescalation reasons"""
        return self.get('/incidents/deescalation-reasons')

    @logged_in
    def escalation_reasons(self):
        """Get a list of escalation reasons"""
        return self.get('/incidents/escalation-reasons')

    @logged_in
    def timespent_reasons(self):
        """Get a list of reasons for spent time"""
        return self.get('/timespent-reasons')

    @logged_in
    def service_windows(self, top=1000, name='', archived=None):
        """
        Get a list of service windows. Optional parameters:
        - top: the number of windows to be returned (default: 1000)
        - name: the prefix to search for (default: '')
        - archived: whether or not the service windows should be archived
                    (default None)
        """
        params = {
            'top': top,
            'name': name,
            'archived': archived
        }
        return self.get('/serviceWindow/lookup/', params=params)

    @logged_in
    def incident_services(self):
        """Get a list of services"""
        return self.get('incidents/slas/services')

    @logged_in
    def subcategories(self):
        """Get a list of subcategories"""
        return self.get('/incidents/subcategories')

    @logged_in
    def urgencies(self):
        """Get a list of urgencies"""
        return self.get('/incidents/urgencies')

    @logged_in
    def service_window(self, id_):
        """Get service window by ID"""
        return self.get('/serviceWindow/lookup/{}'.format(id_))

    @logged_in
    def download_incident_attachment(self, incident_id, attachment_id):
        """Download an attachment by incident ID and attachment ID"""
        url = '/incidents/id/{}/attachments/{}/download'
        return self.get(url.format(incident_id, attachment_id))

    @logged_in
    def incident_attachments(self, id_or_number, start=0, page_size=10):
        """
        Get attachments by incident ID or number. Optionally takes:
        - start: the offset (default: 0)
        - page_size: the amount of attachments returned (default: 10)
        """
        path = self._treat_id_or_num(id_or_number)
        params = {
            'start': start,
            'page_size': page_size
        }
        return self.get('/incidents/{}/attachments'.format(path), params=params)

    @logged_in
    def upload_incident_attachment(self, id_or_number, f):
        """
        Upload a file to an incident identified by ID or number.
        """
        path = self._treat_id_or_num(id_or_number)
        extra = {
            'files': {
                'file': f
            }
        }
        return self.post('/incidents/{}/attachments'.format(path), extra=extra)

    @logged_in
    def email(self, id_):
        """Get email details by ID"""
        return self.get('/emails/id/{}'.format(id_))

    @logged_in
    def search(self, query, index='incidents', start=0):
        """
        Search. Currently it only indexes incidents (but topdesk still takes the
        index argument). Optional parameters:
        - index: the search index (currently only 'incidents')
        - start: the offset to start search at (default: 0)
        """
        params = {
            'query': query,
            'index': index,
            'start': start
        }
        return self.get('/search', params=params)

    def version(self):
        """Get the API version (not the wrapper version!)."""
        return self.get('/version')

    @logged_in
    def operational_activities(self, data=None):
        """
        Get a list of operational activities. Takes a lot of optional filters,
        please review the topdesk documentation (https://developers.topdesk.com/explorer/?page=operations-management#/Operational%20Activities/get_operationalActivities)
        to find out more.
        """
        return self.get('/operationalActivities', params=data)

    @logged_in
    def operational_activity(self, id_):
        """Get an operational activity by ID"""
        return self.get('/operationalActivities/{}'.format(id_))

    @logged_in
    def look_and_feel(self):
        """Get the look and feel of the logged in user"""
        return self.get('/myLookAndFeelProfile')

    @logged_in
    def look_and_feel_logo(self):
        """Get the logo for the look and feel of the logged in user"""
        return self.get('/myLookAndFeelProfile/logo')

    @logged_in
    def look_and_feel_banner(self):
        """Get the banner for the look and feel of the logged in user"""
        return self.get('/myLookAndFeelProfile/banner')

    @logged_in
    def create_task_notification(self, data):
        """
        Create a custom task notification. Takes a lot of parameters, please
        review the topdesk documentation (https://developers.topdesk.com/explorer/?page=task-notifications#/Task%20Notifications/sendNotification)
        to find out more.

        Caution: This feature is currently only available if you enabled it in
        Labs.
        """
        return self.post('/tasknotifications/custom', data=data)

    @logged_in
    def services(self, object_id=None, asset_id=None, top=1000):
        """
        Get a list of services. Optional parameters:
        - object_id: The ID of an object to filter on (default: null)
        - asset_id: The asset ID of an object to filter on (default: null)
        - top: The maximum number of results to return (default: 1000)
        """
        params = {
            'objectId': object_id,
            'assetId': asset_id,
            'top': top
        }
        return self.get('/services', params=params)

    @logged_in
    def create_service(self, data):
        """
        Create a service. Takes a lot of data, please review the topdesk
        documentation (https://developers.topdesk.com/explorer/?page=services#/Services/createService)
        to find out more.
        """
        return self.post('/services', data=data)

    @logged_in
    def service(self, id_):
        """Get a service by ID"""
        return self.get('/services/{}'.format(id_))

    @logged_in
    def service_assets(self, id_):
        """Get linked assets of a service from its ID"""
        return self.get('/services/{}/linkedAssets'.format(id_))

    @logged_in
    def link_service_to_asset(self, id_, asset_id):
        """
        Link asset and service by providing their IDs.
        """
        data = {
            'id': id_,
            'assetId': asset_id
        }
        return self.post('/services/{}/linkedAssets'.format(id_), data=data)

    @logged_in
    def unlink_service_from_asset(self, id_, asset_id):
        """
        Unlink asset and service by providing their IDs.
        """
        return self.delete('/services/{}/linkedAssets/{}'.format(id_, asset_id))

    @logged_in
    def reservations(self, data=None):
        """
        Get a list of reservations. Takes a lot of optional parameters, please
        review the topdesk documentation (https://developers.topdesk.com/explorer/?page=reservations#/Reservations/retrieveReservations)
        to find out more.
        """
        return self.get('/reservations', params=data)

    @logged_in
    def create_reservation(self, data):
        """
        Create a single reservation. Takes a lot of information, please review
        the topdesk documentation (https://developers.topdesk.com/explorer/?page=reservations#/Reservations/createReservation)
        to find out more.
        """
        return self.post('/reservations', data=data)

    @logged_in
    def reservation(self, id_or_number, fields=None):
        """
        Get a single reservation. Optionally you can filter the fields that you
        want to see.
        """
        params = {
            'fields': fields
        }
        # TODO: less duplication
        if " " in id_or_number:
            url = '/reservations/number/{}'
        else:
            url = '/reservations/{}'
        return self.get(url.format(id_or_number), params=params)

    @logged_in
    def cancel_reservation(self, id_, reason_id):
        """
        Cancel a reservation using a reason ID.
        """
        data = {
            'id': reason_id
        }
        return self.post('/reservations/{}/cancel'.format(id_), data=data)

    @logged_in
    def reschedule_reservation(self, id_, start_date, end_date):
        """
        Reschedule a reservation using a new start and end date.
        """
        data = {
            'plannedStartDate': start_date or '',
            'plannedEndDate': end_date or ''
        }
        return self.post('/reservations/{}/reschedule'.format(id_), data=data)

    @logged_in
    def reservation_cancellation_reasons(self):
        """
        Get the list of reservation cancellation reasons.
        """
        return self.get('/reservationCancellationReasons')

    @logged_in
    def reservable_locations(self, fields=None, top=1000, branch_id=None):
        """
        Get the list of reservable locations. Optional parameters:
        - fields: a list of fields to include (default: all)
        - top: the amount of locations to show (default: 1000)
        - branch_id: the uuid of the branch of the location. locations which
                     are not part of the specified branch, will be excluded
                    from the return object. multiple uuids may be specified by
                    providing the parameter multiple times.
        """
        params = {
            'fields': fields,
            'top': top,
            'branchId': branch_id
        }
        return self.get('/reservableLocations', params=params)

    @logged_in
    def reservable_location(self, id_, fields=None):
        """
        Get a single reservation location. Optionally you can filter the fields
        that you want to see.
        """
        params = {
            'fields': fields
        }
        return self.get('/reservableLocations/{}'.format(id_), params=params)

    @logged_in
    def reservable_location_interval(self, id_, from_=None):
        """
        Get a single reservation location interval. Optionally you can filter by
        the start of the interval.
        """
        params = {
            'from': str(from_ or '')
        }
        url = '/reservableLocations/{}/reservableInterval'
        return self.get(url.format(id_), params=params)

    @logged_in
    def facility_occupancies(self, data=None):
        """
        Get the list of occupancy rates of the selected facilities. Takes a lot
        of parameters, please review the topdesk documentation (https://developers.topdesk.com/explorer/?page=reservations#/Facility%20Occupancies/getOccupancy)
        to find out more.
        """
        return self.get('/facilityOccupancies', params=data)

    @logged_in
    def assets(self, template_id, fields=None, include_archived=None):
        """
        Get the list of assets of a given type. Optional parameters:
        - fields: limit the fields you get back (default: all)
        - include_archived: if true, archived assets will be included (default:
                            None)
        """
        params = {
            'field': fields,
            'includeArchived': include_archived
        }
        return self.get('/assetmgmt/assets/templateId/{}'.format(template_id),
                        params=params)

    @logged_in
    def asset_templates(self):
        """Get a list of asset templates (card types)."""
        return self.get('/assetmgmt/cardTypes')

    @logged_in
    def asset_dropdown_options(self, dropdown_id, fields=None):
        """
        Get a list of option for a given dropdown. Optional parameters:
        - fields: limit the fields you get back (default: all)
        """
        params = {
            'field': fields
        }
        return self.get('/assetmgmt/dropdowns/{}'.format(dropdown_id),
                        params=params)

    @logged_in
    def add_branches_to_asset(self, template_id, asset_id, branch_ids):
        """Assign branches to an asset"""
        url = '/assetmgmt/assets/templateId/{}/{}/assignment/branches'
        data = {
            'ids': branch_ids
        }
        return self.put(url.format(template_id, asset_id), data=data)

    @logged_in
    def add_locations_to_asset(self, template_id, asset_id, location_ids):
        """Assign locations to an asset"""
        url = '/assetmgmt/assets/templateId/{}/{}/assignment/locations'
        data = {
            'ids': location_ids
        }
        return self.put(url.format(template_id, asset_id), data=data)

    @logged_in
    def add_person_groups_to_asset(self, template_id, asset_id, group_ids):
        """Assign person_groups to an asset"""
        url = '/assetmgmt/assets/templateId/{}/{}/assignment/personGroups'
        data = {
            'ids': group_ids
        }
        return self.put(url.format(template_id, asset_id), data=data)

    @logged_in
    def add_persons_to_asset(self, template_id, asset_id, person_ids):
        """Assign persons to an asset"""
        url = '/assetmgmt/assets/templateId/{}/{}/assignment/persons'
        data = {
            'ids': person_ids
        }
        return self.put(url.format(template_id, asset_id), data=data)

    @logged_in
    def asset_links(self, source_id):
        """Get linked assets for a given source ID"""
        params = {
            'sourceId': source_id
        }
        return self.get('/assetmgmt/assetLinks', params=params)

    @logged_in
    def link_assets(self, source_id, target_id, type_='child',
                    capability_id=None):
        """
        Link assets. Requires a source and target ID. Optional parameters:
        - type_: the type of relationship (default: child)
        - capability_id: id of the capability that is offered through the link
                         (mutually exclusive with type_)
        """
        data = {
            'sourceId': source_id,
            'targetId': target_id,
            'type': type_,
            'capabilityId': capability_id
        }
        return self.post('/assetmgmt/assetLinks', data=data)

    @logged_in
    def possible_asset_link_relations(self, source_id, target_id):
        """Return possible link relations between two assets."""
        params = {
            'sourceId': source_id,
            'targetId': target_id,
        }
        return self.get('/assetmgmt/assetLinks/possibleRelations',
                        params=params)

    @logged_in
    def unlink_assets(self, relation_id):
        """Unlink assets given the the relation ID."""
        return self.delete('/assetmgmt/assetLinks/{}'.format(relation_id))

    @logged_in
    def assets(self, params):
        """
        Get a list of assets. Takes a lot of filter parameters, please review
        the topdesk documentation (https://developers.topdesk.com/explorer/?page=assets#/Assets/getAssets)
        to find out more.
        """
        return self.get('/assetmgmt/assets', params=params)

    @logged_in
    def create_asset(self, template_id, data):
        """
        Create a new asset by providing a template ID and data that matches
        the asset.
        """
        data['type_id'] = template_id
        return self.post('/assetmgmt/assets', data=data)

    def update_asset(self, id_, template_id, data):
        """
        Update an existing asset. A description of the model can be found in the
        topdesk documentation (https://developers.topdesk.com/explorer/?page=assets#/Asset%20Management%20Import%20API/createByImport).
        """
        url = '/assetmgmt/assets/templateId/{}/{}'
        return self.patch(url.format(template_id, id_), data=data)

    @logged_in
    def blank_asset(self, template_id=None, template_name=None):
        """
        Get a blank asset from a specified template. Either template_id or
        template_name must be specified, otherwise a ValueError is thrown.
        """
        if template_id is None and template_name is None:
            raise ValueError('blank_asset requires either a template id or name')
        params = {
            'templateId': template_id,
            'templateName': template_name
        }
        return self.get('/assetmgmt/assets/blank', params=params)

    @logged_in
    def delete_assets(self, ids):
        """Delete a list of assets identified by their ID"""
        data = {
            'unids': ids
        }
        return self.post('/assetmgmt/assets/delete', data=data)

    @logged_in
    def grid_assets(self, asset_id, field_id):
        """Get assets of grid fields"""
        params = {
            'assetId': asset_id,
            'fieldId': field_id
        }
        return self.get('/assetmgmt/assets/getGridFieldValues', params=params)

    @logged_in
    def asset(self, id_):
        """Get asset by ID"""
        return self.get('/assetmgmt/assets/{}'.format(id_))

    @logged_in
    def update_asset(self, id_, data):
        """
        Update asset by ID. Takes a lot of possible values, please review the
        topdesk documentation (https://developers.topdesk.com/explorer/?page=assets#/Assets/update)
        to find out more.
        """
        return self.post('/assetmgmt/assets/{}'.format(id_), data=data)

    @logged_in
    def archive_asset(self, id_, reason_id):
        """Archive an asset by ID. Must provide a reason."""
        data = {
            'reasonId': reason_id
        }
        return self.post('/assetmgmt/assets/{}/archive'.format(id_), data=data)

    @logged_in
    def unarchive_asset(self, id_, reason_id):
        """Unarchive an asset by ID"""
        return self.post('/assetmgmt/assets/{}/unarchive'.format(id_))

    @logged_in
    def assign_to_asset(self, asset_id, data):
        """
        Assign branch, location, person or person group to an asset by ID. Takes
        a lot of possible values, please refer to the topdesk documentation
        (https://developers.topdesk.com/explorer/?page=assets#/Assignments/addLink)
        to find out more.
        """
        return self.put('/assetmgmt/assets/{}/assignments'.format(asset_id),
                        data=data)

    @logged_in
    def delete_asset_link(self, link_type, target_id):
        """
        Caution: This operation is documented wrongly in topdesk. Currently
        throws a NotImplemented error.
        """
        raise NotImplemented("This method is not documented correctly in topdesk")

    @logged_in
    def asset_assignments(self, asset_id):
        """Get asset assignments"""
        return self.get('/assetmgmt/assets/{}/assignments'.format(asset_id))

    @logged_in
    def unassign_from_asset(self, asset_id, link_id):
        """
        Unassign branch, location, person or person group to an asset by ID.
        """
        url = '/assetmgmt/assets/{}/assignments/{}'
        return self.delete(url.format())

    @logged_in
    def capabilities(self):
        """Get a list of capabilities"""
        return self.get('/assetmgmt/capabilities')

    @logged_in
    def create_capability(self, name):
        """Create a named capability"""
        data = {
            'name': name
        }
        return self.post('/assetmgmt/capabilities', data=data)

    @logged_in
    def capability(self, id_):
        """Get a capability by ID"""
        return self.get('/assetmgmt/capabilities/{}'.format(id_))

    @logged_in
    def update_capability(self, id_, name, etag=None):
        """
        Update capability name by ID. Optional parameters:
        - etag: etag, used for concurrent modification checking with optimistic
                locking
        """
        data = {
            'name': name,
            '@etag': etag
        }
        return self.post('/assetmgmt/capabilities/{}'.format(id_), data=data)

    @logged_in
    def archive_capability(self, id_):
        """Archive capability"""
        return self.post('/assetmgmt/capabilities/{}/archive'.format(id_))

    @logged_in
    def unarchive_capability(self, id_):
        """Unarchive capability"""
        return self.post('/assetmgmt/capabilities/{}/unarchive'.format(id_))

    @logged_in
    def field(self, id_):
        """Get a field by ID"""
        return self.get('/assetmgmt/fields/{}'.format(id_))

    @logged_in
    def templates(self, archived=None):
        """
        Get a list of templates. Optional parameters:
        - archived: whether to show archived templates. If left out, all
                    templates will be shown.
        """
        params = {
            'archived': archived
        }
        return self.get('/assetmgmt/templates', params=params)

    @logged_in
    def uploads(self, asset_id):
        """Get a list of uploaded files for a given asset"""
        params = {
            'assetId': asset_id
        }
        return self.get('/assetmgmt/uploads', params)

    @logged_in
    def create_upload(self, asset_id, f):
        """Upload a file to attach to an asset"""
        params = {
            'assetId': assetd_id
        }

        extra = {
            'files': {
                'file': f
            }
        }

        return self.post('/assetmgmt/uploads', params=params, extra=extra)

    @logged_in
    def delete_upload(self, id_):
        """Delete an uploaded file by ID"""
        return self.delete('/assetmgmt/uploads/{}'.format(id_))

    @logged_in
    def my_authorizables(self, manager_actions=None):
        """
        Return a list of changes or authorization activities for which the
        current user is the manager. Optional parameters:
        - manager_actions: a list of latest actions performed by the manager
        """
        params = {
            'managerAction': manager_actions
        }
        return self.get('/managerAuthorizables', params=params)

    @logged_in
    def change(self, id_):
        """Get a change by ID. Must be the manager of the change."""
        return self.get('/managerAuthorizableChanges/{}'.format(id_))

    @logged_in
    def change_progress_trail(self, id_):
        """Get progress trail for a change identified by ID"""
        url = '/managerAuthorizableChanges/{}/progresstrail'
        return self.get(url.format(id_))

    @logged_in
    def create_action_for_change(self, id_, memo_text, type_):
        """Create a new action for change identified by ID"""
        url = '/managerAuthorizableChanges/{}/progresstrail'
        data = {
            'memoText': memo_text,
            'type': type_
        }
        return self.post(url.format(id_), data=data)

    @logged_in
    def download_change_attachment(self, id_, attachment_id):
        """Download a change attachment by ID"""
        url = '/managerAuthorizableChanges/{}/attachments/{}'
        return self.get(url.format(id_, attachment_id))

    @logged_in
    def create_change_attachment(self, id_, f):
        """Upload a file to attach to a change"""
        extra = {
            'files': {
                'file': f
            }
        }

        url = '/managerAuthorizableChanges/{}/attachments'
        return self.post(url.format(id_), extra=extra)

    @logged_in
    def change_requests(self, id_, inline_images=False,
                        browser_friendly_urls=False):
        """
        Get the list of requests for a change. Optional parameters:
        - inline_images: whether inline images should be returned
        - browser_friendly_urls: whether download URLs should browser URLs
                                 instead of API URLs
        """
        params = {
            'inlineimages': inline_images,
            'browserFriendlyUrls': browser_friendly_urls
        }
        return self.get('/managerAuthorizableChanges/{}/requests'.format(id_),
                        params=params)

    @logged_in
    def change_ordered_items(self, id_):
        """Get the list of requests for a change."""
        url = '/managerAuthorizableChanges/{}/orderedItems'
        return self.get(url.format(id_))

    @logged_in
    def update_change_status(self, id_, from_, action, reason=None,
                             comment=None):
        """
        Approve or reject an authorized change. from_ is the status before the
        transaction, action is the action to be applied. Optional parameters:
        - reason: reason for transaction (can be ID or text)
        - comment: comment about transaction
        """
        data = {
            'from': from_,
            'action': action,
            'reason': reason,
            'comment': comment
        }
        url = '/managerAuthorizableChanges/{}/processingStatusTransitions'
        return self.post(url.format(id_), data=data)

    @logged_in
    def authorization_activity(self, id_):
        """Get authorization activity"""
        return self.get('/managerAuthorizableActivities/{}'.format(id_))

    @logged_in
    def update_authorization_activity(self, id_, action, reason=None,
                                      comment=None):
        """
        Approve or reject an authorization activity. action is the action to be
        applied. Optional parameters:
        - reason: reason for transaction (can be ID or text)
        - comment: comment about transaction
        """
        data = {
            'action': action,
            'reason': reason,
            'comment': comment
        }
        url = '/managerAuthorizableActivities/{}/managerAction'
        return self.put(url.format(id_), data=data)

    @logged_in
    def activity_progress_trail(self, id_):
        """Get progress trail for an activity identified by ID"""
        url = '/managerAuthorizableActivities/{}/progresstrail'
        return self.get(url.format(id_))

    @logged_in
    def create_activity_action(self, id_, memo_text, type_):
        """
        Create action for activity identified by an ID. memo_text is the
        description if it is of type memo, type is the type of the action.
        """
        data = {
            'memoText': memo_text,
            'type': type_
        }
        url = '/managerAuthorizableActivities/{}/progresstrail'
        return self.post(url.format(id_), data=data)

    @logged_in
    def download_activity_attachment(self, id_, attachment_id):
        """Download an activity attachment by ID"""
        url = '/managerAuthorizableActivities/{}/attachments/{}'
        return self.get(url.format(id_, attachment_id))

    @logged_in
    def activity_requests(self, id_, inline_images=False,
                          browser_friendly_urls=False):
        """
        Get the list of requests for an activity. Optional parameters:
        - inline_images: whether inline images should be returned
        - browser_friendly_urls: whether download URLs should browser URLs
                                 instead of API URLs
        """
        params = {
            'inlineimages': inline_images,
            'browserFriendlyUrls': browser_friendly_urls
        }
        url = '/managerAuthorizableActivities/{}/requests'
        return self.get(url.format(id_), params=params)

    @logged_in
    def activity_change_progress_trail(self, id_):
        """
        Get progress trail for a change an activity identified by ID belongs to
        """
        url = '/managerAuthorizableActivites/{}/change/progresstrail'
        return self.get(url.format(id_))

    @logged_in
    def activity_change_requests(self, id_):
        """
        Get requests for a change on an activity identified by ID belongs to
        """
        url = '/managerAuthorizableActivites/{}/change/requests'
        return self.get(url.format(id_))

    @logged_in
    def download_activity_change_attachment(self, id_, attachment_id):
        """Download a change attachment for a change identified by ID"""
        url = '/managerAuthorizableActivites/{}/attachments/{}'
        return self.get(url.format(id_, attachment_id))

    @logged_in
    def change_rejection_reasons(self):
        return self.get('/changeRejectionReasons')

    @logged_in
    def change_activity_rejection_reasons(self):
        return self.get('/changeActivityRejectionReasons')

    @logged_in
    def requester_changes(self, ids=None, requester_ids=None, open_=None):
        """
        Get a list of changes. Optional parameters:
        - ids: limit to changes with these IDs
        - requester_ids: limit to changes requested by people with these IDs
        - open_: whether the changes should still be open (None means all)
        """
        params = {
            'id': ids,
            'requesterId': requester_ids,
            'open': open_
        }
        return self.get('/requesterChanges', params=params)

    @logged_in
    def requester_change(self, id_):
        """Get a change by ID"""
        return self.get('/requesterChanges/{}'.format(id_))

    @logged_in
    def download_requester_change_attachment(self, id_, attachment_id):
        """
        Download an attachment associated to a change, both identified by ID
        """
        url = '/requesterChanges/{}/attachments/{}'
        return self.get(url.format(id_, attachment_id))

    @logged_in
    def create_requester_change_attachment(self, id_, f):
        """Upload a file to attach to a requester change"""
        extra = {
            'files': {
                'file': f
            }
        }

        url = '/requesterChanges/{}/attachments'
        return self.post(url.format(id_), extra=extra)

    @logged_in
    def requester_change_progress_trail(self, id_, ):
        """Get progress trail for a requester change identified by ID"""
        return self.get('/requesterChanges/{}/progresstrail'.format(id_))

    @logged_in
    def create_action_for_requester_change(self, id_, memo_text, type_):
        """Create a new action for requester change identified by ID"""
        url = '/requesterChanges/{}/progresstrail'
        data = {
            'memoText': memo_text,
            'type': type_
        }
        return self.post(url.format(id_), data=data)

    @logged_in
    def requester_change_requests(self, id_, inline_images=False,
                                  browser_friendly_urls=False):
        """
        Get the list of requests for a change. Optional parameters:
        - inline_images: whether inline images should be returned
        - browser_friendly_urls: whether download URLs should browser URLs
                                 instead of API URLs
        """
        params = {
            'inlineimages': inline_images,
            'browserFriendlyUrls': browser_friendly_urls
        }
        return self.get('/requesterChanges/{}/requests'.format(id_),
                        params=params)

    @logged_in
    def requester_change_ordered_items(self, id_):
        """Get the list of requests for a requester change."""
        return self.get('/requesterChanges/{}/orderedItems'.format(id_))

    @logged_in
    def create_operator_change(self, data):
        """
        Create a new operator change. Takes a lot of data, please review the
        topdesk documentation (https://developers.topdesk.com/explorer/?page=change#/Working%20as%20an%20operator/post_operatorChanges)
        to find out more.
        """
        return self.post('/operatorChanges', data=data)

    @logged_in
    def update_operator_change(self, id_, data):
        """
        Create a new operator change. Takes a lot of data, please review the
        topdesk documentation (https://developers.topdesk.com/explorer/?page=change#/Working%20as%20an%20operator/patch_operatorChanges__identifier_)
        to find out more.
        """
        return self.post('/operatorChanges/{}'.format(id_), data=data)

    @logged_in
    def operator_changes(self, params):
        """
        Get a list of operator changes. Takes a lot of possible filters; please
        refer to the topdesk API (https://developers.topdesk.com/explorer/?page=change#/Working%20as%20an%20operator/get_operatorChanges)
        to find out more.
        """
        return self.get('/operatorChanges', params=params)

    @logged_in
    def operator_change(self, id_):
        """Get operator change by ID"""
        return self.get('/operatorChanges/{}'.format(id_))

    @logged_in
    def process_operator_change(self, id_, from_, action, reason=None,
                                comment=None):
        """
        Process a change through a phase by ID. from is the status before the
        transaction, action is the action to be applied. Optional parameters:
        - reason: the reason for the transaction
        - comment: a comment about the transaction
        """
        data = {
            'from': from_,
            'action': action,
            'reason': reason,
            'comment': comment
        }
        url = '/operatorChanges/{}/processingStatusTransitions'
        return self.post(url.format(id_), data=data)

    @logged_in
    def operator_change_requests(self, id_, inline_images=False,
                                 browser_friendly_urls=False):
        """
        Get the list of requests for an operator change. Optional parameters:
        - inline_images: whether inline images should be returned
        - browser_friendly_urls: whether download URLs should browser URLs
                                 instead of API URLs
        """
        params = {
            'inlineimages': inline_images,
            'browserFriendlyUrls': browser_friendly_urls
        }
        return self.get('/operatorChanges/{}/requests'.format(id_),
                        params=params)

    @logged_in
    def operator_change_progress_trail(self, id_):
        """Get progress trail for an operator change identified by ID"""
        return self.get('/operatorChanges/{}/progresstrail'.format(id_))

    @logged_in
    def create_action_for_operator_change(self, id_, memo_text, type_):
        """
        Create a new action for operator change by ID. memo_text describes the
        action, type is the type of the action.
        """
        data = {
            'memoText': memo_text,
            'type': type_
        }
        return self.post('/operatorChanges/{}/progresstrail'.format(id_),
                         data=data)

    @logged_in
    def download_operator_change_attachment(self, id_, attachment_id):
        """Download an operator change attachment by ID"""
        return self.get('/operatorChanges/{}/attachments/{}'.format(id_,
                                                            attachment_id))

    @logged_in
    def create_operator_change_attachment(self, id_, f):
        """Upload a file to attach to an operator change"""
        extra = {
            'files': {
                'file': f
            }
        }

        url = '/operatorChanges/{}/attachments'
        return self.post(url.format(id_), extra=extra)

    @logged_in
    def operator_change_activities(self, changes=None, archived=None):
        """
        Get a list of change activities. Optional parameters:
        - changes: a list of IDs or numbers of the parent change
        - archived: whether to show activities that are archived or not
        """
        params = {
            'change': changes,
            'archived': archived
        }
        return self.get('/operatorChangeActivities', params=params)

    @logged_in
    def create_operator_change_activity(self, data):
        """
        Create a new change activity. Takes a lot of possible values, please
        review the topdesk documentation (https://developers.topdesk.com/explorer/?page=change#/Working%20as%20an%20operator/post_operatorChangeActivities)
        to find out more.
        """
        return self.post('/operatorChangeActivities', data=data)

    @logged_in
    def update_operator_change_activity(self, id_, data):
        """
        Update change activity. Takes a lot of possible values, please review
        the topdesk documentation (https://developers.topdesk.com/explorer/?page=change#/Working%20as%20an%20operator/patch_operatorChangeActivities__identifier_)
        to find out more.
        """
        return self.patch('/operatorChangeActivities/{}'.format(id_), data=data)

    @logged_in
    def change_activity(self, id_):
        """Get a change activity by ID"""
        return self.get('/operatorChangeActivities/{}'.format(id_))

    @logged_in
    def operator_change_activity_requests(self, id_, inline_images=False,
                                          browser_friendly_urls=False):
        """
        Get requests for this change activity.
        - inline_images: whether inline images should be returned
        - browser_friendly_urls: whether download URLs should browser URLs
                                 instead of API URLs
        """
        params = {
            'inlineimages': inline_images,
            'browserFriendlyUrls': browser_friendly_urls
        }
        return self.get('/operatorChangeActivities/{}/requests'.format(id_),
                        params=params)

    @logged_in
    def operator_change_activity_progress_trail(self, id_,
                                                inline_images=False,
                                                browser_friendly_urls=False):
        """
        Get progress trail for an operator change activity identified by ID.
        Optional parameters:
        - inline_images: whether inline images should be returned
        - browser_friendly_urls: whether download URLs should browser URLs
                                 instead of API URLs
        """
        params = {
            'inlineimages': inline_images,
            'browserFriendlyUrls': browser_friendly_urls
        }
        url = '/operatorChangeActivities/{}/progresstrail'
        return self.get(url.format(id_), params=params)

    @logged_in
    def create_operator_change_activity_action(self, id_, memo_text, type_):
        """
        Create action for activity identified by an ID. memo_text is the
        description if it is of type memo, type is the type of the action.
        """
        data = {
            'memoText': memo_text,
            'type': type_
        }
        url = '/operatorChangeActivities/{}/progresstrail'
        return self.post(url.format(id_), data=data)

    @logged_in
    def create_operator_change_activity_attachment(self, id_, f):
        """Upload a file to attach to a change activity identified by ID"""
        extra = {
            'files': {
                'file': f
            }
        }

        url = '/operatorChangeActivities/{}/attachments'
        return self.post(url.format(id_), extra=extra)

    @logged_in
    def download_operator_change_activity_attachment(self, id_,
                                                     attachment_id):
        """Download the attachment of a change identified by ID"""
        url = '/operatorChangeActivities/{}/attachments/{}'
        return self.get(url.format(id_, attachment_id))

    @logged_in
    def change_calendar(self, start, end, data=None):
        """
        Get a list of upcoming changes and activities in a date range. start
        is the start datetime, end is the end datetime. Takes a lot of
        optional parameters, please review the topdesk documentation (https://developers.topdesk.com/explorer/?page=change#/Working%20as%20an%20operator/get_changeCalendar)
        to find out more.
        """
        if data is None:
            data = {}
        data['start'] = start
        data['end'] = end
        return self.get('/changeCalendar', params=data)

    @logged_in
    def change_calendar_detail(self, id_):
        """Get change or activity from the calendar by ID"""
        return self.get('/changeCalendar/{}'.format(id_))

    @logged_in
    def change_calendar_requests(self, id_, inline_images=False,
                                 browser_friendly_urls=False):
        """
        Get requests for this change activity.
        - inline_images: whether inline images should be returned
        - browser_friendly_urls: whether download URLs should browser URLs
                                 instead of API URLs
        """
        params = {
            'inlineimages': inline_images,
            'browserFriendlyUrls': browser_friendly_urls
        }
        return self.get('/changeCalendar/{}/requests'.format(id_),
                        params=params)

    @logged_in
    def change_calendar_progress_trail(self, id_, inline_images=False,
                                       browser_friendly_urls=False):
        """
        Get progress trail for an operator change activity identified by ID.
        Optional parameters:
        - inline_images: whether inline images should be returned
        - browser_friendly_urls: whether download URLs should browser URLs
                                 instead of API URLs
        """
        params = {
            'inlineimages': inline_images,
            'browserFriendlyUrls': browser_friendly_urls
        }
        url = '/changeCalendar/{}/progresstrail'
        return self.get(url.format(id_), params=params)

    @logged_in
    def download_change_calendar_attachment(self, id_, attachment_id):
        """Download the attachment of a change identified by ID"""
        return self.get('/changeCalendar/{}/attachments/{}'.format(id_,
                                                            attachment_id))

    @logged_in
    def applicable_change_templates(self):
        """Get templates that can be used to create new change requests"""
        return self.get('/applicableChangeTemplates')
