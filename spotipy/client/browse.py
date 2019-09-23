from typing import List, Union

from spotipy.client.base import SpotifyBase
from spotipy.model import (
    SimplePlaylistPaging,
    SimpleAlbumPaging,
    CategoryPaging,
    Category,
    Recommendations
)

recommendation_prefixes = {'min', 'max', 'target'}
recommendation_attributes = {
    'acousticness',
    'danceability',
    'duration_ms',
    'energy',
    'instrumentalness',
    'key',
    'liveness',
    'loudness',
    'mode',
    'popularity',
    'speechiness',
    'tempo',
    'time_signature',
    'valence'
}


class SpotifyBrowse(SpotifyBase):
    def featured_playlists(
            self,
            country: str = None,
            locale: str = None,
            timestamp: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> tuple:
        """
        Get a list of Spotify featured playlists.

        Parameters
        ----------
        country
            an ISO 3166-1 alpha-2 country code
        locale
            the desired language, consisting of a lowercase ISO 639 language code
            and an uppercase ISO 3166-1 alpha-2 country code joined by an underscore
        timestamp
            Timestamp in ISO 8601 format: yyyy-MM-ddTHH:mm:ss.
            Used to specify the user's local time to get results tailored for
            that specific date and time in the day.
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        tuple
            (str, SimplePlaylistPaging): message for the playlists and a list of
            simplified playlist objects wrapped in a paging object
        """
        json = self._get(
            'browse/featured-playlists',
            locale=locale,
            country=country,
            timestamp=timestamp,
            limit=limit,
            offset=offset
        )
        return json['message'], SimplePlaylistPaging(**json['playlists'])

    def new_releases(
            self,
            country: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> tuple:
        """
        Get a list of new album releases featured in Spotify.

        Parameters
        ----------
        country
            an ISO 3166-1 alpha-2 country code
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        tuple
            (str, SimpleAlbumPaging): message for the albums and a list of
            simplified album objects wrapped in a paging object
        """
        json = self._get(
            'browse/new-releases',
            country=country,
            limit=limit,
            offset=offset
        )
        return json['message'], SimpleAlbumPaging(**json['albums'])

    def categories(
            self,
            country: str = None,
            locale: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> CategoryPaging:
        """
        Get a list of categories used to tag items in Spotify.

        Parameters
        ----------
        country
            an ISO 3166-1 alpha-2 country code
        locale
            the desired language, consisting of a lowercase ISO 639 language code
            and an uppercase ISO 3166-1 alpha-2 country code joined by an underscore
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        CategoryPaging
            paging object containing a list of categories
        """
        json = self._get(
            'browse/categories',
            country=country,
            locale=locale,
            limit=limit,
            offset=offset
        )
        return CategoryPaging(**json['categories'])

    def category(
            self,
            category_id: str,
            country: str = None,
            locale: str = None
    ) -> Category:
        """
        Get a single category used to tag items in Spotify.

        Parameters
        ----------
        category_id
            category ID
        country
            an ISO 3166-1 alpha-2 country code
        locale
            the desired language, consisting of a lowercase ISO 639 language code
            and an uppercase ISO 3166-1 alpha-2 country code joined by an underscore

        Returns
        -------
        Category
            category object
        """
        json = self._get(
            'browse/categories/' + category_id,
            country=country,
            locale=locale
        )
        return Category(**json)

    def category_playlists(
            self,
            category_id: str = None,
            country: str = None,
            limit: int = 20,
            offset: int = 0
    ) -> SimplePlaylistPaging:
        """
        Get a list of Spotify playlists tagged with a particular category.

        Parameters
        ----------
        category_id
            category ID
        country
            an ISO 3166-1 alpha-2 country code
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimplePlaylistPaging
            paging object containing a list of simplified playlist objects
        """
        json = self._get(
            f'browse/categories/{category_id}/playlists',
            country=country,
            limit=limit,
            offset=offset
        )
        return SimplePlaylistPaging(**json['playlists'])

    def recommendations(
            self,
            artist_ids: list = None,
            genres: list = None,
            track_ids: list = None,
            limit: int = 20,
            market: Union[str, None] = 'from_token',
            **attributes
    ) -> Recommendations:
        """
        Get a list of recommended tracks for seeds.

        Parameters
        ----------
        artist_ids
            list of artist IDs, URIs or URLs
        genres
            list of genre names
        track_ids
            list of artist IDs, URIs or URLs
        limit
            the number of items to return (1..100)
        market
            None, an ISO 3166-1 alpha-2 country code or 'from_token'
        attributes
            min/max/target_<attribute> - For the tuneable track
            attributes listed in the documentation, these values
            provide filters and targeting on results.

        Returns
        -------
        Recommendations
            recommendations object containing track recommendations and seeds
        """
        params = dict(limit=limit)
        if artist_ids is not None:
            params['seed_artists'] = ','.join(artist_ids)
        if genres is not None:
            params['seed_genres'] = ','.join(genres)
        if track_ids is not None:
            params['seed_tracks'] = ','.join(track_ids)
        if market is not None:
            params['market'] = market

        for name, value in attributes.items():
            p, a = name.split('_')
            if p in recommendation_prefixes and a in recommendation_attributes:
                params[name] = value

        json = self._get('recommendations', **params)
        return Recommendations(**json)

    def recommendation_genre_seeds(self) -> List[str]:
        """
        Get a list of available genre seeds.

        Returns
        -------
        list
            list of genres to use as seeds
        """
        return self._get('recommendations/available-genre-seeds')['genres']
