#!/usr/bin/env python
# coding: utf-8

# Author : Rahul Bhadani
# Initial Date: Apr 2, 2020
# About: Contains a class to find files that are overlapping in time and space
# Read associated README for full description
# License: MIT License

#   Permission is hereby granted, free of charge, to any person obtaining
#   a copy of this software and associated documentation files
#   (the "Software"), to deal in the Software without restriction, including
#   without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to
#   permit persons to whom the Software is furnished to do so, subject
#   to the following conditions:

#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.

#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
#   ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
#   TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#   PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
#   SHALL THE AUTHORS, COPYRIGHT HOLDERS OR ARIZONA BOARD OF REGENTS
#   BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
#   AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#   OR OTHER DEALINGS IN THE SOFTWARE.

import os
import ntpath
import glob
import gc
import numpy as np
from pathlib import Path
import math

from ..utils import configure_logworker
LOGGER = configure_logworker()

from ..strymmap import strymmap

class  platoons:
    def __init__(self, folders, **kwargs):
        """
        `platoons finds one or more files that overlapping in time and space based on timestamp and GPS  location.
        This function is helpful to identify a subset of strym data 


        Parameters
        -------------

        folders:  `list`
            A list of folder that contains data files captured using libpanda and comma.ai Panda black/grey panda devices

        
        Attributes
        ------------
        
        success: `bool`
            This flag tells of call to `platoons` was able to successfully instantiate a platoon object
            
        CAN_files: `list`
            list of CAN data files found from the folder
        
        GPS fileS: `list`
            list of GPS data files found from the folder
        
        
        
        
        """
        self.success = False

        self.CAN_files = None
        self.GPS_files = None
        
        # Check if the folder exists and is not empty

        if isinstance(folders, str):
            
            folders = [folders]
        
        isDIR = []
        valid_folders = []
        for f in folders:
            isDirectory = os.path.isdir(f)
            if not isDirectory:
                LOGGER.warn("{} is not a directory, we will skip it.".format(f))
            else:
                valid_folders.append(f)
            isDIR.append(isDirectory)


        if  ~np.any(isDIR):
            del isDIR
            gc.collect()
            LOGGER.error("None of the directory in the provided list of folders is valid.")
            return

        CAN_files = []
        for f in valid_folders:
            for path in Path(f).rglob('*CAN*.csv'):
                CAN_files.append(str(path))

        GPS_files = []
        for f in valid_folders:
            for path in Path(f).rglob('*GPS*.csv'):
                GPS_files.append(str(path))
        
        self.CAN_files = CAN_files
        self.GPS_files = GPS_files

        del CAN_files
        del GPS_files
        gc.collect()

    def spatial_finder(self, space_eps = 0.0001):
        """
        `spatial_finder` finds the two or more datasets that have been collected in nearly same geographical location

        Parameters
        -------------
        space_eps: `float`
            
        
        """

        map_obj = []
        for gps in self.GPS_files:
            g = strymmap(csvfile= gps)
            map_obj.append(g)

        
    @staticmethod
    def spatial_similarity(p1, p2, space_eps = 0.0001):
        """
        Calculates spatial similarity between two points.

        Parameters
        --------------
        p1: `tuple`
            (Longitude, Latitutde) pair representing the first point
        
        p2: `tuple`
            (Longitude, Latitutde) pair representing the second point

        space_eps: `float`
            A parameter specifying the maximum allowable distance for two points p1, and p2 to match
        """

        phi_1 = p1[1]*math.pi/180.0 # in radians
        phi_2 = p2[1]*math.pi/180.0 # in radians
        delta_phi = phi_1 - phi_2
        lamda_1 = p1[0]
        lamda_2 = p2[0]

        delta_lambda  = (lamda_1 - lamda_2 )*math.pi/180.0

        R = 6371000 # Earthe radius in meter

        a = (math.sin(delta_phi/2))**2 + math.cos(phi_1)*math.cos(phi_2)*math.sin(delta_lambda/2)*math.sin(delta_lambda/2)

        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        great_circle_distance = R*c # in meters

        similarity_score = 0
        if great_circle_distance > space_eps:
            similarity_score = 0
        else:
            similarity_score = 1 - great_circle_distance/space_eps

        return similarity_score


    @staticmethod
    def score_LCS(T1, T2):
        """
        A recursive algorithm to find a longest common subsequence
        given a (long, lat) sequence of two trajectories T1 and T2

        Parameters
        --------------
        T1: `np.array`
            A numpy array with two columns (Long, Lat) representing  the first trajectory

        T2: `np.array`
            A numpy array with two columns (Long, Lat) representing the second trajectory
        """
        n = T1.shape[0]
        m = T2.shape[0]
        if n == 0 or m == 0:
            return 0

        s1 = platoons.score_LCS(T1[:-1], T2[:-1]) + platoons.spatial_similarity(T1[-1], T2[-1])
        s2 = platoons.score_LCS(T1, T2[:-1])
        s3 =platoons.score_LCS(T1[:-1], T2)

        return np.max([s1, s2, s3])
        

        