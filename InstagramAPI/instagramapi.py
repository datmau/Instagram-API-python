#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import AuthenticationError
from endpoints import InstagramAPIEndPoints

class InstagramAPI(InstagramAPIEndPoints):
    """ Most of the available calls are defined in the InstagramAPIEndPoints.

        This subclass adds additional helper functions to make common operations easier.

        Clients should use this class.
        """

    AuthenticationError = AuthenticationError  # Make visible to clients for easy of reference.

    def __init__(self, username, password):
        InstagramAPIEndPoints.__init__(self, username, password)

    # Helper functions to gather complete lists/deal with pagination.

    # TODO: Replace with iterators.

    def followers_iter(self, username, delay_between_calls=0):
        """ 
            Yields a series of dictionaries describing each user that follows this user.
            Handles pagination and throttling.
        """
        maxid = None
        while True:
            _, json_dict = self.getUserFollowers(username, maxid=maxid)
            maxid = json_dict.get('next_max_id', None)
            for user in json_dict.get('users', []):
                yield user
            if not maxid:
                break
            time.sleep(delay_between_calls)  # Avoid overloading Instagram

    # TODO: Delete!
    def getTotalFollowers(self, username):
        return list(followers_iter(username))

    def getTotalFollowings(self, usernameId):
        followers = []
        next_max_id = ''
        while 1:
            self.getUserFollowings(usernameId, next_max_id)
            temp = self.LastJson

            for item in temp["users"]:
                followers.append(item)

            if not temp["big_list"]:
                return followers
            next_max_id = temp["next_max_id"]

    def getTotalUserFeed(self, usernameId, minTimestamp=None):
        user_feed = []
        next_max_id = ''
        while 1:
            self.getUserFeed(usernameId, next_max_id, minTimestamp)
            temp = self.LastJson
            for item in temp["items"]:
                user_feed.append(item)
            if not temp["more_available"]:
                return user_feed
            next_max_id = temp["next_max_id"]

    def getTotalLikedMedia(self, scan_rate=1):
        next_id = ''
        liked_items = []
        for x in range(0, scan_rate):
            # TODO: Resolve what "temp" should be.
            temp = self.getLikedMedia(next_id)
            temp = self.LastJson
            try:
                next_id = temp["next_max_id"]
                for item in temp["items"]:
                    liked_items.append(item)
            except KeyError:
                break
        return liked_items

    # Helper functions to find out information about the logged in user.

    def getSelfGeoMedia(self):
        return self.getGeoMedia(self._loggedinuserid)

    def getSelfUserFeed(self, maxid='', minTimestamp=None):
        return self.getUserFeed(self._loggedinuserid, maxid, minTimestamp)

    def getSelfUsersFollowing(self):
        return self.getUserFollowings(self._loggedinuserid)

    def getSelfUserFollowers(self, maxid=''):
        return self.getUserFollowers(self._loggedinuserid, maxid=maxid)

    def getSelfUsernameInfo(self):
        return self.getUsernameInfo(self._loggedinuserid)

    def getSelfUserTags(self):
        return self.getUserTags(self._loggedinuserid)

    def getTotalSelfUserFeed(self, minTimestamp=None):
        return self.getTotalUserFeed(self._loggedinuserid, minTimestamp)

    def getTotalSelfFollowers(self):
        return self.getTotalFollowers(self._loggedinuserid)

    def getTotalSelfFollowings(self):
        return self.getTotalFollowings(self._loggedinuserid)

    def self_followers_iter(self, delaybetweencalls=0):
        for i in self.followers_iter(self._loggedinuserid, delaybetweencalls):
            yield i