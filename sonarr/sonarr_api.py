# -*- coding: utf-8 -*-
from .request_api import RequestAPI
class SonarrAPI(RequestAPI):

    def __init__(
            self, 
            host_url: str, 
            api_key: str,
        ):
        """Constructor requires Host-URL and API-KEY

            Args:
                host_url (str): Host url to sonarr.
                api_key: API key from Sonarr. You can find this
        """
        super().__init__(host_url, api_key)

    # ENDPOINT CALENDAR
    def get_calendar(
            self, 
            start_date: str=None, 
            end_date: str=None
        ):
        # optional params: start (date) & end (date)
        """Gets upcoming episodes, if start/end are not supplied episodes 
        airing today and tomorrow will be returned
        
            Returns:
                List of dict's from response.

        """
        path = "/api/calendar"
        res = self.request_get(path)
        return res.json()


    # ENDPOINT COMMAND
    def command(self, path, **kwargs):
        """Command Function
        """
        pass

    
    def manual_import(self, **kwargs):
        """Manual import command
            Kwargs:
                folder (str): Folder to manually look at.
                sort_by (str): What field to sort by.
                order (str): desc or asc. 
        
        """     
        url_params = {
            'folder': kwargs.get('folder', "/"),
            'sort_by': kwargs.get('sort_by', "qualityWeight"),
            'order': kwargs.get('sort_by', "desc"),
            'apikey': self.api_key
        }        
        
        path = '/api/manualimport'

        response = self.request_get(path, **url_params)
        return response

    def auto_manual_import(self, **kwargs):
        """Manual import command
            Kwargs:
                folder (str): Folder to manually look at.
                sort_by (str): What field to sort by.
                order (str): desc or asc. 
        
        """     
        manual_import = self.manual_import(**kwargs)




    # ENDPOINT DISKSPACE
    def get_diskspace(self):
        """Return Information about Diskspace"""
        path = "/diskspace"
        res = self.request_get(path)
        return res.json()


    # ENDPOINT EPISODE
    def get_episodes_by_series_id(self, **kwargs):
        """Returns all episodes for the given series
            Kwargs:
                seriesId
        """
        path = "/episode"
        res = self.request_get(path, **kwargs)
        return res.json()

    def get_episode_by_episode_id(self, episode_id):
        """Returns the episode with the matching id"""
        path = "/episode/{}".format(episode_id)
        res = self.request_get(path)
        return res.json()

    def upd_episode(self, data):
        #TEST THIS
        """Update the given episodes, currently only monitored is changed, all other modifications are ignored"""
        '''NOTE: All parameters (you should perform a GET/{id} and submit the full body with the changes,
        as other values may be editable in the future.'''
        path = "/episode"
        res = self.request_put(path, data)
        return res.json()


    # ENDPOINT EPISODE FILE
    def get_episode_files_by_series_id(self, **kwargs):
        """Returns all episode files for the given series
            Kwargs:
                seriesId (str): 
        """
        path = "/episodefile"
        res = self.request_get(path, **kwargs)
        return res.json()

    # TEST THIS
    def get_episode_file_by_episode_id(self, episode_id):
        """Returns the episode file with the matching id"""
        path = "/episodefile/{}".format(episode_id)
        res = self.request_get(path)
        return res.json()

    # TEST THIS
    def rem_episode_file_by_episode_id(self, episode_id):
        """Delete the given episode file"""
        path = "/episodefile/{}".format(episode_id)
        res = self.request_del(path, data=None)
        return res.json()


    # ENDPOINT HISTORY
    # DOES NOT WORK
    def get_history(self):
        """Gets history (grabs/failures/completed)"""
        path = "/history"
        res = self.request_get(path)
        return res.json()


    # ENDPOINT WANTED MISSING
    # DOES NOT WORK
    def get_wanted_missing(self):
        """Gets missing episode (episodes without files)"""
        path = "/wanted/missing/"
        res = self.request_get(path)
        return res.json()


    # ENDPOINT QUEUE
    def get_queue(self):
        """Gets current downloading info"""
        path = "/queue"
        res = self.request_get(path)
        return res.json()


    # ENDPOINT PROFILE
    def get_quality_profiles(self):
        """Gets all quality profiles"""
        path = "/profile"
        res = self.request_get(path)
        return res.json()


    # ENDPOINT RELEASE


    # ENDPOINT RELEASE/PUSH
    def push_release(self, **kwargs):
        """Notifies Sonarr of a new release.
            title: release name
            downloadUrl: .torrent file URL
            protocol: usenet / torrent
            publishDate: ISO8601 date string

            Kwargs:
                title (str): 
                downloadUrl (str):
                protocol (str):
                publishDate (str):
        """
        path = "/release/push"
        res = self.request_post(path, data=kwargs)
        return res.json()


    # ENDPOINT ROOTFOLDER
    def get_root_folder(self):
        """Returns the Root Folder"""
        path = "/rootfolder"
        res = self.request_get(path)
        return res.json()


    # ENDPOINT SERIES
    def get_series(self):
        """Return all series in your collection"""
        path = "/series"
        res = self.request_get(path)
        return res.json()

    def get_series_by_series_id(self, series_id):
        """Return the series with the matching ID or 404 if no matching series is found"""
        path = "/series/{}".format(series_id)
        res = self.request_get(path)
        return res.json()

    def constuct_series_json(self, tvdbId, quality_profile):
        """Searches for new shows on trakt and returns Series object to add"""
        path = "/series/lookup?term={}".format('tvdbId:' + str(tvdbId))
        res = self.request_get(path)
        s_dict = res.json()[0]

        # get root folder path
        root = self.get_root_folder()[0]['path']
        series_json = {
            'title': s_dict['title'],
            'seasons': s_dict['seasons'],
            'path': root + s_dict['title'],
            'qualityProfileId': quality_profile,
            'seasonFolder': True,
            'monitored': True,
            'tvdbId': tvdbId,
            'images': s_dict['images'],
            'titleSlug': s_dict['titleSlug'],
            "addOptions": {
                          "ignoreEpisodesWithFiles": True,
                          "ignoreEpisodesWithoutFiles": True
                        }
                    }
        return series_json

    def add_series(self, series_json):
        """Add a new series to your collection"""
        path = "/series"
        res = self.request_post(path, data=series_json)
        return res.json()

    def upd_series(self, data):
        """Update an existing series"""
        path = "/series"
        res = self.request_put(path, data)
        return res.json()

    def rem_series(self, series_id, rem_files=False):
        """Delete the series with the given ID"""
        # File deletion does not work
        data = {
            # 'id': series_id,
            'deleteFiles': 'true'
        }
        path = "/series/{}".format(series_id)
        res = self.request_del(path, data)
        return res.json()


    # ENDPOINT SERIES LOOKUP
    def lookup_series(self, **kwargs):
        """Searches for new shows on trakt
        
            Kwargs:
                term (str): term filter for lookup_series.
        """
        path = "/series/lookup"
        res = self.request_get(path, **kwargs)
        return res.json()


    # ENDPOINT SYSTEM-STATUS
    def get_system_status(self):
        """Returns the System Status"""
        path = "/system/status"
        res = self.request_get(path)
        return res.json()
