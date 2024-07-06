# https://docs.blender.org/api/current/info_tips_and_tricks.html

import bpy
import os

filename = os.path.join(os.path.dirname(bpy.data.filepath), "myscript.py")
exec(compile(open(filename).read(), filename, 'exec'))