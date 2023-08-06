"""
Tools for generating PowerPoint presentations

"""
import os
import cv2

def get_movie_frame(movie_file, frame=0):
    """Creates a picture file of a specified frame from a movie file. Returns the filename of the picture file and the resolution of the picture.

    Parameters
    ----------
    movie_file : str
        Filename of a movie
    frame : int, optional
        Frame number to get, by default 0

    Returns
    -------
    str
        Filename of the picture file
    int
        Height of the picture in pixels
    int
        Width of the picture in pixels
        
    """
    movie = cv2.VideoCapture(movie_file)
    _, image = movie.read()    
    height, width, _ = image.shape
    filename = os.path.splitext(movie_file)[0] + f'_{frame}.jpg'
    cv2.imwrite(filename, image)
    
    return filename, height, width
