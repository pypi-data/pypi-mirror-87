__all__ = ['Tf', 'Gf', 'Trace', 'Work', 'Plug', 'Vt', 'Ar', 'Kind', 'Sdf', 'Ndr', 'Sdr', 'Pcp', 'Usd', 'UsdGeom', 'UsdVol', 'UsdLux', 'UsdMedia', 'UsdShade', 'UsdRender', 'UsdHydra', 'UsdRi', 'UsdSkel', 'UsdUI', 'UsdUtils']


# appended to this file for the windows PyPI package
import os, sys
dllPath = os.path.split(os.path.realpath(__file__))[0]
if sys.version_info >= (3, 8, 0):
    os.add_dll_directory(dllPath)
else:
    os.environ['PATH'] = dllPath + os.pathsep + os.environ['PATH']
