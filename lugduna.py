"""
Make an animation of the orbit of the asteroid 1133 Lugduna.

Some notes
----------

 - This script is tested and run on a Lenovo T14 Gen 2 laptop
   + CPU: Quad Core 11th Gen Intel Core i5-1145G7
   + Graphics card: Intel TigerLake-LP GT2 [Iris Xe Graphics]
 - PNG output can only be configured by editing the ~/.xdg/gaiasky.config.yaml file. Possibly the ~/gaiasky/conf/*yaml
   files are used for defaults when first starting up GaiaSky.
 - Use a framerate of 60 fps for a smooth (non-jerky) end result.
 - No need to limit the frame rate in GaiaSky itself.
 - The script was mostly developed on GaiaSky version 3.2.0-RC1 

Anthony Brown Sep 2021 - Dec 2021
"""

from py4j.clientserver import ClientServer, JavaParameters
from pygaia.astrometry.vectorastrometry import spherical_to_cartesian
from pygaia.astrometry.constants import au_in_meter
from pygaia.astrometry.coordinates import Transformations, CoordinateTransformation
import numpy as np
import argparse

au_in_km = au_in_meter/1.0e3

# ------------ Convenience functions for positioning the camera ------------ #

def set_camera_position(posvec, gsk):
    """
    Set the camera position.

    Parameters
    ----------

    posvec: array
        Position of camera in Cartesian (x, y, z) ICRS coordinations, units of au.
    gsk : object
        The GaiaSky ClientServer instance.

    Returns
    -------

    Nothing.
    """
    gsk.setCameraPosition(np.roll(posvec*au_in_km, -1))


def set_camera_direction(dirvec, gsk):
    """
    Set the camera viewing direction.

    Parameters
    ----------

    dirvec: array
        Direction vector along which the camera points in Cartesian (x, y, z) ICRS coordinations.
    gsk : object
        The GaiaSky ClientServer instance.

    Returns
    -------

    Nothing.
    """
    gsk.setCameraDirection(np.roll(dirvec, -1))


def set_camera_up(upvec, gsk):
    """
    Set the camera up direction.

    Parameters
    ----------

    upvec: array
        The "Up" direction vector Cartesian (x, y, z) ICRS coordinations.
    gsk : object
        The GaiaSky ClientServer instance.

    Returns
    -------

    Nothing.
    """
    gsk.setCameraUp(np.roll(upvec, -1))


# ------------ Functions for camera transitions ------------ #

def do_camera_transition(posvec, dirvec, upvec, duration, gsk):
    """
    Execute a set of N camera transitions according to the input lists of camera state vectors and transition durations.

    Parameters
    ----------

    posvec: 3-array
        New camera position vector [x, y, z] in Cartesian ICRS coordinations, units of au.
    dirvec: 3-array
        New camera direction vector [x, y, z] in Cartesian ICRS coordinations.
    upvec: 3-array
        New camera up vector [x, y, z] in Cartesian ICRS coordinations.
    duration: list of N floats
        Transition duration in seconds.

    Returns
    -------

    Nothing.
    """
    gsk.cameraTransition(np.roll(posvec, -1)*au_in_meter/gsk.getInternalUnitToMeterConversion(), np.roll(dirvec, -1),
            np.roll(upvec, -1), duration, True)


def do_camera_transition_list(posvecs, dirvecs, upvecs, durations, gsk):
    """
    Execute a set of N camera transitions according to the input lists of camera state vectors and transition durations.

    Parameters
    ----------

    posvecs: nd-array of shape (N,3)
        List of camera position vectors [x, y, z] in Cartesian ICRS coordinations, units of au.
    dirvecs: nd-array of shape (N,3)
        List of camera direction vectors [x, y, z] in Cartesian ICRS coordinations.
    upvecs: nd-array of shape (N,3)
        List of camera up vectors [x, y, z] in Cartesian ICRS coordinations.
    durations: list of N floats
        List of transition durations.

    Returns
    -------

    Nothing.
    """
    for pv, dv, uv, dt in zip(posvecs*au_in_meter/gsk.getInternalUnitToMeterConversion(), dirvecs, upvecs, durations):
        gsk.cameraTransition(np.roll(pv, -1), np.roll(dv, -1), np.roll(uv, -1), dt, True)


def make_animation(args):
    """
    Execute the steps to make the animation with GaiaSky.

    Parameters
    ----------

    args : dict
        Command line parameters.

    Returns
    -------

    Nothing.
    """
    gateway = ClientServer(java_parameters=JavaParameters(auto_convert=True))
    gs = gateway.entry_point

    # ------------ Set up camera and GUI properties ------------ #
    gs.disableInput()
    gs.disableGui()
    gs.cameraStop()

    gs.setCameraSpeed(1.0)
    gs.setRotationCameraSpeed(1.0)
    gs.setTurningCameraSpeed(1.0)
    gs.setCinematicCamera(True)
    #gs.setCameraFocus("Sun")

    gs.setFov(65.0)

    # ------------ Select which animation components are visible ------------ #
    gs.setComponentTypeVisibility("element.planets", False)
    gs.setComponentTypeVisibility("element.atmospheres", False)
    gs.setComponentTypeVisibility("element.stars", True)
    gs.setComponentTypeVisibility("element.moons", False)
    gs.setComponentTypeVisibility("element.satellites", False)
    gs.setComponentTypeVisibility("element.galaxies", True)
    gs.setComponentTypeVisibility("element.milkyway", True)

    gs.setComponentTypeVisibility("element.asteroids", False)
    gs.setComponentTypeVisibility("element.orbits", False)
    gs.setComponentTypeVisibility("element.labels", False)
    gs.setComponentTypeVisibility("element.constellations", False)
    gs.setComponentTypeVisibility("element.boundaries", False)
    gs.setComponentTypeVisibility("element.equatorial", False)
    gs.setComponentTypeVisibility("element.ecliptic", False)
    gs.setComponentTypeVisibility("element.galactic", False)
    gs.setComponentTypeVisibility("element.clusters", False)
    gs.setComponentTypeVisibility("element.meshes", False)
    gs.setComponentTypeVisibility("element.titles", False)

    # ------------ Other animation parameters ------------ #
    gs.setCrosshairVisibility(False)
    gs.setLineWidthFactor(2.0)
    gs.setLensFlare(False)
    gs.setClosestCrosshairVisibility(False)

    # ------------ Configure animation frame output ------------ #
    #gs.configureFrameOutput(1920, 1080, 30, "/home/brown/Gaia/Outreach/1133Lugduna/frames/", "gs")
    gs.configureFrameOutput(1280, 720, 60, "/home/brown/Gaia/Outreach/1133Lugduna/frames/", "gs")
    gs.setFrameOutputMode("simple")
    gs.resetImageSequenceNumber()

    stdwait = 5.0
    stdwaitshort = 2.0

    # ------------ Configure animation time (start on 2022-01-01) ------------ #
    gs.stopSimulationTime()
    gs.setSimulationTime(2022, 1, 1, 12, 0, 0, 0)
    gs.setTargetTime(2023, 1, 1, 12, 0, 0, 0)

    # ------------ Configure the camera starting state ------------ #
    # Camera positions and orientation vectors are given in Cartesian Ecliptic coordinates and then transformed to ICRS.
    #
    # Start at 15 au above the ecliptic plane looking down the positive z-axis toward the sun, that is (lambda, beta, d) =
    # (270, 90, 15).

    ct = CoordinateTransformation(Transformations.ECL2ICRS)

    cam_lambda = np.deg2rad(270.0)
    cam_beta = np.deg2rad(90.0)
    start_distance = 15.0
    cam_x_ecl, cam_y_ecl, cam_z_ecl = np.cos(cam_lambda)*np.cos(cam_beta)*start_distance, \
            np.sin(cam_lambda)*np.cos(cam_beta)*start_distance, np.sin(cam_beta)*start_distance
    cam_x_icrs, cam_y_icrs, cam_z_icrs = ct.transform_cartesian_coordinates(cam_x_ecl, cam_y_ecl, cam_z_ecl)
    campos = np.array([cam_x_icrs, cam_y_icrs, cam_z_icrs])
    set_camera_position(campos, gs)

    dir_x_ecl, dir_y_ecl, dir_z_ecl = -cam_x_ecl, -cam_y_ecl, -cam_z_ecl
    dir_x_icrs, dir_y_icrs, dir_z_icrs = ct.transform_cartesian_coordinates(dir_x_ecl, dir_y_ecl, dir_z_ecl)
    camdir = np.array([dir_x_icrs, dir_y_icrs, dir_z_icrs])
    camdir = camdir/np.linalg.norm(camdir)
    set_camera_direction(camdir, gs)

    up_x_ecl, up_y_ecl, up_z_ecl = 0.0, 1.0, 0.0
    up_x_icrs, up_y_icrs, up_z_icrs = ct.transform_cartesian_coordinates(up_x_ecl, up_y_ecl, up_z_ecl)
    camup = np.array([up_x_icrs, up_y_icrs, up_z_icrs])
    camup = camup/np.linalg.norm(camup)
    set_camera_up(camup, gs)

    gs.sleep(stdwaitshort)
    gs.setFrameOutput(args['saveFrames'])

    # Enable orbits
    gs.setComponentTypeVisibility("element.planets", True)
    gs.setComponentTypeVisibility("element.orbits", True)
    gs.setComponentTypeVisibility("element.labels", True)
    gs.sleep(stdwait)

    # Show Lugduna
    gs.sleep(stdwaitshort)
    gs.setComponentTypeVisibility("element.asteroids", True)
    gs.sleep(stdwait)

    # ------------ Move smoothly to a position at (lamba, beta, d) = (270, 30, 15) ------------ #
    # Camera up vector changes from pointing along positive y to pointing along positive z

    cam_beta = np.deg2rad(30.0)
    cam_x_ecl, cam_y_ecl, cam_z_ecl = np.cos(cam_lambda)*np.cos(cam_beta)*start_distance, \
            np.sin(cam_lambda)*np.cos(cam_beta)*start_distance, np.sin(cam_beta)*start_distance
    cam_x_icrs, cam_y_icrs, cam_z_icrs = ct.transform_cartesian_coordinates(cam_x_ecl, cam_y_ecl, cam_z_ecl)
    campos = np.array([cam_x_icrs, cam_y_icrs, cam_z_icrs])

    dir_x_ecl, dir_y_ecl, dir_z_ecl = -cam_x_ecl, -cam_y_ecl, -cam_z_ecl
    dir_x_icrs, dir_y_icrs, dir_z_icrs = ct.transform_cartesian_coordinates(dir_x_ecl, dir_y_ecl, dir_z_ecl)
    camdir = np.array([dir_x_icrs, dir_y_icrs, dir_z_icrs])
    camdir = camdir/np.linalg.norm(camdir)

    up_x_ecl, up_y_ecl, up_z_ecl = 0.0, 0.0, 1.0
    up_x_icrs, up_y_icrs, up_z_icrs = ct.transform_cartesian_coordinates(up_x_ecl, up_y_ecl, up_z_ecl)
    camup = np.array([up_x_icrs, up_y_icrs, up_z_icrs])
    camup = camup/np.linalg.norm(camup)

    do_camera_transition(campos, camdir, camup, 5.0, gs)

    gs.sleep(0.5)

    # ------------ Move smoothly to a position at (lamba, beta, d) = (225, 30, 15) ------------ #

    cam_lambda = np.deg2rad(225.0)
    cam_x_ecl, cam_y_ecl, cam_z_ecl = np.cos(cam_lambda)*np.cos(cam_beta)*start_distance, \
            np.sin(cam_lambda)*np.cos(cam_beta)*start_distance, np.sin(cam_beta)*start_distance
    cam_x_icrs, cam_y_icrs, cam_z_icrs = ct.transform_cartesian_coordinates(cam_x_ecl, cam_y_ecl, cam_z_ecl)
    campos = np.array([cam_x_icrs, cam_y_icrs, cam_z_icrs])

    dir_x_ecl, dir_y_ecl, dir_z_ecl = -cam_x_ecl, -cam_y_ecl, -cam_z_ecl
    dir_x_icrs, dir_y_icrs, dir_z_icrs = ct.transform_cartesian_coordinates(dir_x_ecl, dir_y_ecl, dir_z_ecl)
    camdir = np.array([dir_x_icrs, dir_y_icrs, dir_z_icrs])
    camdir = camdir/np.linalg.norm(camdir)

    do_camera_transition(campos, camdir, camup, 5.0, gs)

    gs.sleep(0.5)

    # ------------ Move smoothly to a position at (lamba, beta, d) = (225, 30, 5) ------------ #

    end_distance = 5.0
    cam_x_ecl, cam_y_ecl, cam_z_ecl = np.cos(cam_lambda)*np.cos(cam_beta)*end_distance, \
            np.sin(cam_lambda)*np.cos(cam_beta)*end_distance, np.sin(cam_beta)*end_distance
    cam_x_icrs, cam_y_icrs, cam_z_icrs = ct.transform_cartesian_coordinates(cam_x_ecl, cam_y_ecl, cam_z_ecl)
    campos = np.array([cam_x_icrs, cam_y_icrs, cam_z_icrs])

    do_camera_transition(campos, camdir, camup, 5.0, gs)

    gs.sleep(stdwaitshort)
    gs.setComponentTypeVisibility("element.labels", False)
    gs.cameraStop()

    # ------------ Start orbit simulation ------------ #

    time_warp = 2000000
    sleep_time = np.ceil(365.25*86400/time_warp)
    gs.setTimeWarp(time_warp)

    gs.startSimulationTime()
    gs.sleep(sleep_time)

    gs.setFrameOutput(False)

    gs.enableGui()
    gs.enableInput()

    gateway.shutdown()


def parse_command_line_arguments():
    """
    Set up command line parsing.
    """
    parser = argparse.ArgumentParser("Make an animation showing the orbit of 1133 Lugduna.")
    parser.add_argument("-s", action="store_true", dest="saveFrames", help="Save the animation frames for making a video.")
    pargs = vars(parser.parse_args())
    return pargs


if __name__ in '__main__':
    cmdargs = parse_command_line_arguments()
    make_animation(cmdargs)
