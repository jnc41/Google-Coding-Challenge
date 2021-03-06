"""A video player class."""

from .video_library import VideoLibrary
import random
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.current_playing = None
        self.paused = False
        self.playlists = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        list_videos = self._video_library.get_all_videos()
        list_videos.sort()  # uses new Video class method

        for video in list_videos:
            # Created class function to print out video class in the correct form
            # tags = (" ".join([tag for tag in video.tags]))
            # print(f"{video.title} ({video.video_id}) [{tags}]")
            print(video)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        video = self._video_library.get_video(video_id)

        if self.current_playing == None and video != None and not video.flagged:
            print(f"Playing video: {video.title}")
            self.current_playing = video

        elif self.current_playing != None and video != None and not video.flagged:
            print(f"Stopping video: {self.current_playing.title}")
            print(f"Playing video: {video.title}")
            self.current_playing = video

        elif video != None and video.flagged == True:
            print(f"Cannot play video: Video is currently flagged (reason: {video.flag_reason})")

        elif video == None:
            print("Cannot play video: Video does not exist")

        self.paused = False

    def stop_video(self):
        """Stops the current video."""

        if self.current_playing != None:
            print(f"Stopping video: {self.current_playing.title}")
            self.current_playing = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""

        list_videos = self._video_library.get_all_videos()
        list_videos = [video for video in list_videos if not video.flagged]

        if len(list_videos) != 0:
            random_vid = list_videos[random.randint(0, len(list_videos) - 1)]
            if random_vid != None:
                self.play_video(random_vid._video_id)

        else:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""

        if not self.paused and self.current_playing != None:
            print(f"Pausing video: {self.current_playing.title}")
            self.paused = True

        elif self.paused == True and self.current_playing != None:
            print(f"Video already paused: {self.current_playing.title}")

        elif self.current_playing == None:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""

        if self.paused and self.current_playing != None:
            print(f"Continuing video: {self.current_playing.title}")
            self.paused = False

        elif not self.paused and self.current_playing != None:
            print("Cannot continue video: Video is not paused")

        elif self.current_playing == None:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""

        if self.current_playing != None and not self.paused:
            # tags = (" ".join([tag for tag in self.current_playing.tags]))
            # print(f"Currently playing: {self.current_playing.title} ({self.current_playing.video_id}) [{tags}]")
            print(f"Currently playing: {self.current_playing}")

        elif self.current_playing != None and self.paused:
            print(f"Currently playing: {self.current_playing} - PAUSED")


        elif self.current_playing == None:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.upper() not in self.playlists:
            self.playlists[playlist_name.upper()] = Playlist(playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")

        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)

        # If playlist not found
        if playlist_name.upper() not in self.playlists:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

        # If playlist found
        elif playlist_name.upper() in self.playlists:

            # If video doesn't exists
            if video not in self._video_library.get_all_videos():
                print(f"Cannot add video to {playlist_name}: Video does not exist")

            # If video exist
            else:

                # If video is not in playlist
                if video not in self.playlists[playlist_name.upper()].videos and not video.flagged:
                    self.playlists[playlist_name.upper()].videos.append(video)
                    print(f"Added video to {playlist_name}: {video.title}")

                elif video.flagged:
                    print(
                        f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flag_reason})")

                # If video is already in the playlist
                else:
                    print(f"Cannot add video to {playlist_name}: Video already added")

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self.playlists) == 0:
            print("No playlists exist yet")
            return

        playlists_names = [self.playlists[playlist].name for playlist in self.playlists]
        playlists_names.sort()

        print("Showing all playlists:")
        for playlist in playlists_names:
            print(playlist)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.upper() not in self.playlists:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

        else:
            print(f"Showing playlist: {playlist_name}")

            if len(self.playlists[playlist_name.upper()].videos) != 0:
                for video in self.playlists[playlist_name.upper()].videos:
                    print(video)
            else:
                print("No videos here yet")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        video = self._video_library.get_video(video_id)

        # If playlist not found
        if playlist_name.upper() not in self.playlists:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

        # If playlist found
        elif playlist_name.upper() in self.playlists:

            # If video doesn't exists
            if video not in self._video_library.get_all_videos():
                print(f"Cannot remove video from {playlist_name}: Video does not exist")

            # If video exist
            else:

                # If video is not in playlist
                if video not in self.playlists[playlist_name.upper()].videos:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

                # If video is already in the playlist
                else:
                    self.playlists[playlist_name.upper()].videos.remove(video)
                    print(f"Removed video from {playlist_name}: {video.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        # If playlist not found
        if playlist_name.upper() not in self.playlists:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

        else:
            self.playlists[playlist_name.upper()].videos.clear()
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        # If playlist not found
        if playlist_name.upper() not in self.playlists:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

        else:
            self.playlists.pop(playlist_name.upper())
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        list_videos = self._video_library.get_all_videos()
        list_videos.sort()
        count = 0
        search_videos = []

        # Searches for video
        for video in list_videos:
            if search_term.upper() in video.title.upper() and not video.flagged:
                count += 1
                search_videos.append((str(count), video))

        # if none found
        if count == 0:
            print(f"No search results for {search_term}")

        else:
            print(f"Here are the results for {search_term}:")
            for i in search_videos:
                print(f"{i[0]}) {i[1]}")

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            try:
                user_input = int(input())
                if 1 <= user_input <= len(search_videos):
                    chosen_video = search_videos[user_input - 1][1]
                    self.play_video(chosen_video.video_id)
            except:
                pass

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        list_videos = self._video_library.get_all_videos()
        list_videos.sort()
        count = 0
        search_videos = []

        # Searches for video
        for video in list_videos:
            video_tags = [i.upper() for i in video.tags]
            if video_tag.upper() in video_tags and not video.flagged:
                count += 1
                search_videos.append((str(count), video))

        # if none found
        if count == 0:
            print(f"No search results for {video_tag}")

        else:
            print(f"Here are the results for {video_tag}:")
            for i in search_videos:
                print(f"{i[0]}) {i[1]}")

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            try:
                user_input = int(input())
                if 1 <= user_input <= len(search_videos):
                    chosen_video = search_videos[user_input - 1][1]
                    self.play_video(chosen_video.video_id)
            except:
                pass

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)

        if video != None:
            if video.flagged == False:
                video.flagged = True

                if flag_reason != "":
                    video.flag_reason = flag_reason

                if self.current_playing == video:
                    self.stop_video()

                print(f"Successfully flagged video: {video.title} (reason: {video.flag_reason})")
            else:
                print("Cannot flag video: Video is already flagged")


        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)

        if video != None:
            if video.flagged:
                video.flagged = False
                print(f"Successfully removed flag from video: {video.title}")

            else:
                print("Cannot remove flag from video: Video is not flagged")


        else:
            print("Cannot remove flag from video: Video does not exist")