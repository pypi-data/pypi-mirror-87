

class Shot(object):
    """
    This class represents on shot and contains shot properties such as start/end frame index of a shot, shot-id and
    video_name.
    """

    def __init__(self, sid, movie_name, start_pos, end_pos):
        """
        Constructor.

        :param sid: This parameter is used to specify a shot id.
        :param movie_name: this parameter is used to specify a movie_name.
        :param start_pos: This parameter is used to specify the start frame index of a shot.
        :param end_pos: This parameter is used to specify the end frame index of a shot.
        """
        #print("create instance of shot ...");
        self.sid = sid
        self.movie_name = movie_name
        self.start_pos = start_pos
        self.end_pos = end_pos

    def convert2String(self):
        """
        This method is used to convert all properties of a shot into a semicolon-separated string.
        :return:
        """
        tmp_str = str(self.movie_name) + ";" + str(self.sid) + ";" + str(self.start_pos) + ";" + str(self.end_pos)
        return tmp_str

    def printShotInfo(self):
        """
        This method is used to print all properties of a shot.
        """
        print("------------------------")
        print("shot id: " + str(self.sid))
        print("movie name: " + str(self.movie_name))
        print("start frame: " + str(self.start_pos))
        print("end frame: " + str(self.end_pos))
