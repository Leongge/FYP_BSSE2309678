# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions 
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------
'''Wrapper for /System/Library/Frameworks/AGL.framework/Headers/agl.h

Generated by tools/gengl.py.
Do not modify this file.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: gengl.py 601 2007-02-04 05:36:59Z Alex.Holkner $'

from ctypes import *
from pyglet.gl.lib import link_AGL as _link_function

if not _link_function:
    raise ImportError('AGL framework is not available.')

# BEGIN GENERATED CONTENT (do not edit below this line)

# This content is generated by tools/gengl.py.
# Wrapper for /System/Library/Frameworks/AGL.framework/Headers/agl.h


AGL_VERSION_2_0 = 1 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:41
class struct_GDevice(Structure):
    __slots__ = [
    ]
struct_GDevice._fields_ = [
    ('_opaque_struct', c_int)
]

GDevice = struct_GDevice 	# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/QD.framework/Headers/Quickdraw.h:1347
GDPtr = POINTER(GDevice) 	# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/QD.framework/Headers/Quickdraw.h:1348
GDHandle = POINTER(GDPtr) 	# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/QD.framework/Headers/Quickdraw.h:1349
AGLDevice = GDHandle 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:46
class struct_OpaqueGrafPtr(Structure):
    __slots__ = [
    ]
struct_OpaqueGrafPtr._fields_ = [
    ('_opaque_struct', c_int)
]

GrafPtr = POINTER(struct_OpaqueGrafPtr) 	# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/QD.framework/Headers/Quickdraw.h:1009
CGrafPtr = GrafPtr 	# /System/Library/Frameworks/ApplicationServices.framework/Frameworks/QD.framework/Headers/Quickdraw.h:1392
AGLDrawable = CGrafPtr 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:51
class struct___AGLRendererInfoRec(Structure):
    __slots__ = [
    ]
struct___AGLRendererInfoRec._fields_ = [
    ('_opaque_struct', c_int)
]

AGLRendererInfo = POINTER(struct___AGLRendererInfoRec) 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:56
class struct___AGLPixelFormatRec(Structure):
    __slots__ = [
    ]
struct___AGLPixelFormatRec._fields_ = [
    ('_opaque_struct', c_int)
]

AGLPixelFormat = POINTER(struct___AGLPixelFormatRec) 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:57
class struct___AGLContextRec(Structure):
    __slots__ = [
    ]
struct___AGLContextRec._fields_ = [
    ('_opaque_struct', c_int)
]

AGLContext = POINTER(struct___AGLContextRec) 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:58
class struct___AGLPBufferRec(Structure):
    __slots__ = [
    ]
struct___AGLPBufferRec._fields_ = [
    ('_opaque_struct', c_int)
]

AGLPbuffer = POINTER(struct___AGLPBufferRec) 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:59
AGL_NONE = 0 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:66
AGL_ALL_RENDERERS = 1 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:67
AGL_BUFFER_SIZE = 2 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:68
AGL_LEVEL = 3 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:69
AGL_RGBA = 4 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:70
AGL_DOUBLEBUFFER = 5 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:71
AGL_STEREO = 6 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:72
AGL_AUX_BUFFERS = 7 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:73
AGL_RED_SIZE = 8 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:74
AGL_GREEN_SIZE = 9 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:75
AGL_BLUE_SIZE = 10 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:76
AGL_ALPHA_SIZE = 11 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:77
AGL_DEPTH_SIZE = 12 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:78
AGL_STENCIL_SIZE = 13 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:79
AGL_ACCUM_RED_SIZE = 14 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:80
AGL_ACCUM_GREEN_SIZE = 15 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:81
AGL_ACCUM_BLUE_SIZE = 16 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:82
AGL_ACCUM_ALPHA_SIZE = 17 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:83
AGL_PIXEL_SIZE = 50 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:88
AGL_MINIMUM_POLICY = 51 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:89
AGL_MAXIMUM_POLICY = 52 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:90
AGL_OFFSCREEN = 53 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:91
AGL_FULLSCREEN = 54 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:92
AGL_SAMPLE_BUFFERS_ARB = 55 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:93
AGL_SAMPLES_ARB = 56 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:94
AGL_AUX_DEPTH_STENCIL = 57 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:95
AGL_COLOR_FLOAT = 58 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:96
AGL_MULTISAMPLE = 59 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:97
AGL_SUPERSAMPLE = 60 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:98
AGL_SAMPLE_ALPHA = 61 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:99
AGL_RENDERER_ID = 70 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:104
AGL_SINGLE_RENDERER = 71 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:105
AGL_NO_RECOVERY = 72 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:106
AGL_ACCELERATED = 73 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:107
AGL_CLOSEST_POLICY = 74 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:108
AGL_ROBUST = 75 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:109
AGL_BACKING_STORE = 76 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:110
AGL_MP_SAFE = 78 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:111
AGL_WINDOW = 80 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:113
AGL_MULTISCREEN = 81 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:114
AGL_VIRTUAL_SCREEN = 82 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:115
AGL_COMPLIANT = 83 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:116
AGL_PBUFFER = 90 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:118
AGL_BUFFER_MODES = 100 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:135
AGL_MIN_LEVEL = 101 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:136
AGL_MAX_LEVEL = 102 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:137
AGL_COLOR_MODES = 103 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:138
AGL_ACCUM_MODES = 104 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:139
AGL_DEPTH_MODES = 105 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:140
AGL_STENCIL_MODES = 106 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:141
AGL_MAX_AUX_BUFFERS = 107 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:142
AGL_VIDEO_MEMORY = 120 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:143
AGL_TEXTURE_MEMORY = 121 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:144
AGL_RENDERER_COUNT = 128 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:145
AGL_SWAP_RECT = 200 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:150
AGL_BUFFER_RECT = 202 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:151
AGL_SWAP_LIMIT = 203 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:152
AGL_COLORMAP_TRACKING = 210 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:153
AGL_COLORMAP_ENTRY = 212 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:154
AGL_RASTERIZATION = 220 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:155
AGL_SWAP_INTERVAL = 222 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:156
AGL_STATE_VALIDATION = 230 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:157
AGL_BUFFER_NAME = 231 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:158
AGL_ORDER_CONTEXT_TO_FRONT = 232 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:159
AGL_CONTEXT_SURFACE_ID = 233 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:160
AGL_CONTEXT_DISPLAY_ID = 234 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:161
AGL_SURFACE_ORDER = 235 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:162
AGL_SURFACE_OPACITY = 236 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:163
AGL_CLIP_REGION = 254 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:164
AGL_FS_CAPTURE_SINGLE = 255 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:165
AGL_SURFACE_BACKING_SIZE = 304 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:166
AGL_ENABLE_SURFACE_BACKING_SIZE = 305 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:167
AGL_SURFACE_VOLATILE = 306 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:168
AGL_FORMAT_CACHE_SIZE = 501 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:172
AGL_CLEAR_FORMAT_CACHE = 502 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:173
AGL_RETAIN_RENDERERS = 503 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:174
AGL_MONOSCOPIC_BIT = 1 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:177
AGL_STEREOSCOPIC_BIT = 2 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:178
AGL_SINGLEBUFFER_BIT = 4 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:179
AGL_DOUBLEBUFFER_BIT = 8 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:180
AGL_0_BIT = 1 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:183
AGL_1_BIT = 2 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:184
AGL_2_BIT = 4 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:185
AGL_3_BIT = 8 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:186
AGL_4_BIT = 16 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:187
AGL_5_BIT = 32 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:188
AGL_6_BIT = 64 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:189
AGL_8_BIT = 128 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:190
AGL_10_BIT = 256 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:191
AGL_12_BIT = 512 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:192
AGL_16_BIT = 1024 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:193
AGL_24_BIT = 2048 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:194
AGL_32_BIT = 4096 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:195
AGL_48_BIT = 8192 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:196
AGL_64_BIT = 16384 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:197
AGL_96_BIT = 32768 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:198
AGL_128_BIT = 65536 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:199
AGL_RGB8_BIT = 1 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:202
AGL_RGB8_A8_BIT = 2 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:203
AGL_BGR233_BIT = 4 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:204
AGL_BGR233_A8_BIT = 8 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:205
AGL_RGB332_BIT = 16 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:206
AGL_RGB332_A8_BIT = 32 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:207
AGL_RGB444_BIT = 64 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:208
AGL_ARGB4444_BIT = 128 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:209
AGL_RGB444_A8_BIT = 256 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:210
AGL_RGB555_BIT = 512 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:211
AGL_ARGB1555_BIT = 1024 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:212
AGL_RGB555_A8_BIT = 2048 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:213
AGL_RGB565_BIT = 4096 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:214
AGL_RGB565_A8_BIT = 8192 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:215
AGL_RGB888_BIT = 16384 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:216
AGL_ARGB8888_BIT = 32768 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:217
AGL_RGB888_A8_BIT = 65536 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:218
AGL_RGB101010_BIT = 131072 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:219
AGL_ARGB2101010_BIT = 262144 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:220
AGL_RGB101010_A8_BIT = 524288 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:221
AGL_RGB121212_BIT = 1048576 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:222
AGL_ARGB12121212_BIT = 2097152 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:223
AGL_RGB161616_BIT = 4194304 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:224
AGL_ARGB16161616_BIT = 8388608 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:225
AGL_INDEX8_BIT = 536870912 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:226
AGL_INDEX16_BIT = 1073741824 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:227
AGL_RGBFLOAT64_BIT = 16777216 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:228
AGL_RGBAFLOAT64_BIT = 33554432 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:229
AGL_RGBFLOAT128_BIT = 67108864 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:230
AGL_RGBAFLOAT128_BIT = 134217728 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:231
AGL_RGBFLOAT256_BIT = 268435456 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:232
AGL_RGBAFLOAT256_BIT = 536870912 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:233
AGL_NO_ERROR = 0 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:238
AGL_BAD_ATTRIBUTE = 10000 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:240
AGL_BAD_PROPERTY = 10001 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:241
AGL_BAD_PIXELFMT = 10002 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:242
AGL_BAD_RENDINFO = 10003 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:243
AGL_BAD_CONTEXT = 10004 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:244
AGL_BAD_DRAWABLE = 10005 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:245
AGL_BAD_GDEV = 10006 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:246
AGL_BAD_STATE = 10007 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:247
AGL_BAD_VALUE = 10008 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:248
AGL_BAD_MATCH = 10009 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:249
AGL_BAD_ENUM = 10010 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:250
AGL_BAD_OFFSCREEN = 10011 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:251
AGL_BAD_FULLSCREEN = 10012 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:252
AGL_BAD_WINDOW = 10013 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:253
AGL_BAD_POINTER = 10014 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:254
AGL_BAD_MODULE = 10015 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:255
AGL_BAD_ALLOC = 10016 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:256
AGL_BAD_CONNECTION = 10017 	# /System/Library/Frameworks/AGL.framework/Headers/agl.h:257
GLint = c_long 	# /System/Library/Frameworks/OpenGL.framework/Headers/gl.h:47
# /System/Library/Frameworks/AGL.framework/Headers/agl.h:264
aglChoosePixelFormat = _link_function('aglChoosePixelFormat', AGLPixelFormat, [POINTER(AGLDevice), GLint, POINTER(GLint)], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:265
aglDestroyPixelFormat = _link_function('aglDestroyPixelFormat', None, [AGLPixelFormat], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:266
aglNextPixelFormat = _link_function('aglNextPixelFormat', AGLPixelFormat, [AGLPixelFormat], None)

GLboolean = c_ubyte 	# /System/Library/Frameworks/OpenGL.framework/Headers/gl.h:43
# /System/Library/Frameworks/AGL.framework/Headers/agl.h:267
aglDescribePixelFormat = _link_function('aglDescribePixelFormat', GLboolean, [AGLPixelFormat, GLint, POINTER(GLint)], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:268
aglDevicesOfPixelFormat = _link_function('aglDevicesOfPixelFormat', POINTER(AGLDevice), [AGLPixelFormat, POINTER(GLint)], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:273
aglQueryRendererInfo = _link_function('aglQueryRendererInfo', AGLRendererInfo, [POINTER(AGLDevice), GLint], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:274
aglDestroyRendererInfo = _link_function('aglDestroyRendererInfo', None, [AGLRendererInfo], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:275
aglNextRendererInfo = _link_function('aglNextRendererInfo', AGLRendererInfo, [AGLRendererInfo], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:276
aglDescribeRenderer = _link_function('aglDescribeRenderer', GLboolean, [AGLRendererInfo, GLint, POINTER(GLint)], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:281
aglCreateContext = _link_function('aglCreateContext', AGLContext, [AGLPixelFormat, AGLContext], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:282
aglDestroyContext = _link_function('aglDestroyContext', GLboolean, [AGLContext], None)

GLuint = c_ulong 	# /System/Library/Frameworks/OpenGL.framework/Headers/gl.h:51
# /System/Library/Frameworks/AGL.framework/Headers/agl.h:283
aglCopyContext = _link_function('aglCopyContext', GLboolean, [AGLContext, AGLContext, GLuint], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:284
aglUpdateContext = _link_function('aglUpdateContext', GLboolean, [AGLContext], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:289
aglSetCurrentContext = _link_function('aglSetCurrentContext', GLboolean, [AGLContext], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:290
aglGetCurrentContext = _link_function('aglGetCurrentContext', AGLContext, [], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:295
aglSetDrawable = _link_function('aglSetDrawable', GLboolean, [AGLContext, AGLDrawable], None)

GLsizei = c_long 	# /System/Library/Frameworks/OpenGL.framework/Headers/gl.h:48
GLvoid = None 	# /System/Library/Frameworks/OpenGL.framework/Headers/gl.h:56
# /System/Library/Frameworks/AGL.framework/Headers/agl.h:296
aglSetOffScreen = _link_function('aglSetOffScreen', GLboolean, [AGLContext, GLsizei, GLsizei, GLsizei, POINTER(GLvoid)], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:297
aglSetFullScreen = _link_function('aglSetFullScreen', GLboolean, [AGLContext, GLsizei, GLsizei, GLsizei, GLint], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:298
aglGetDrawable = _link_function('aglGetDrawable', AGLDrawable, [AGLContext], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:303
aglSetVirtualScreen = _link_function('aglSetVirtualScreen', GLboolean, [AGLContext, GLint], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:304
aglGetVirtualScreen = _link_function('aglGetVirtualScreen', GLint, [AGLContext], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:309
aglGetVersion = _link_function('aglGetVersion', None, [POINTER(GLint), POINTER(GLint)], None)

GLenum = c_ulong 	# /System/Library/Frameworks/OpenGL.framework/Headers/gl.h:42
# /System/Library/Frameworks/AGL.framework/Headers/agl.h:314
aglConfigure = _link_function('aglConfigure', GLboolean, [GLenum, GLuint], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:319
aglSwapBuffers = _link_function('aglSwapBuffers', None, [AGLContext], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:324
aglEnable = _link_function('aglEnable', GLboolean, [AGLContext, GLenum], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:325
aglDisable = _link_function('aglDisable', GLboolean, [AGLContext, GLenum], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:326
aglIsEnabled = _link_function('aglIsEnabled', GLboolean, [AGLContext, GLenum], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:327
aglSetInteger = _link_function('aglSetInteger', GLboolean, [AGLContext, GLenum, POINTER(GLint)], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:328
aglGetInteger = _link_function('aglGetInteger', GLboolean, [AGLContext, GLenum, POINTER(GLint)], None)

Style = c_ubyte 	# /System/Library/Frameworks/CoreServices.framework/Headers/../Frameworks/CarbonCore.framework/Headers/MacTypes.h:524
# /System/Library/Frameworks/AGL.framework/Headers/agl.h:333
aglUseFont = _link_function('aglUseFont', GLboolean, [AGLContext, GLint, Style, GLint, GLint, GLint, GLint], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:338
aglGetError = _link_function('aglGetError', GLenum, [], None)

GLubyte = c_ubyte 	# /System/Library/Frameworks/OpenGL.framework/Headers/gl.h:49
# /System/Library/Frameworks/AGL.framework/Headers/agl.h:339
aglErrorString = _link_function('aglErrorString', POINTER(GLubyte), [GLenum], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:344
aglResetLibrary = _link_function('aglResetLibrary', None, [], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:349
aglSurfaceTexture = _link_function('aglSurfaceTexture', None, [AGLContext, GLenum, GLenum, AGLContext], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:354
aglCreatePBuffer = _link_function('aglCreatePBuffer', GLboolean, [GLint, GLint, GLenum, GLenum, c_long, POINTER(AGLPbuffer)], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:355
aglDestroyPBuffer = _link_function('aglDestroyPBuffer', GLboolean, [AGLPbuffer], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:356
aglDescribePBuffer = _link_function('aglDescribePBuffer', GLboolean, [AGLPbuffer, POINTER(GLint), POINTER(GLint), POINTER(GLenum), POINTER(GLenum), POINTER(GLint)], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:357
aglTexImagePBuffer = _link_function('aglTexImagePBuffer', GLboolean, [AGLContext, AGLPbuffer, GLint], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:362
aglSetPBuffer = _link_function('aglSetPBuffer', GLboolean, [AGLContext, AGLPbuffer, GLint, GLint, GLint], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:363
aglGetPBuffer = _link_function('aglGetPBuffer', GLboolean, [AGLContext, POINTER(AGLPbuffer), POINTER(GLint), POINTER(GLint), POINTER(GLint)], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:368
aglGetCGLContext = _link_function('aglGetCGLContext', GLboolean, [AGLContext, POINTER(POINTER(None))], None)

# /System/Library/Frameworks/AGL.framework/Headers/agl.h:369
aglGetCGLPixelFormat = _link_function('aglGetCGLPixelFormat', GLboolean, [AGLPixelFormat, POINTER(POINTER(None))], None)

__all__ = ['AGL_VERSION_2_0', 'AGLDevice', 'AGLDrawable', 'AGLRendererInfo',
'AGLPixelFormat', 'AGLContext', 'AGLPbuffer', 'AGL_NONE', 'AGL_ALL_RENDERERS',
'AGL_BUFFER_SIZE', 'AGL_LEVEL', 'AGL_RGBA', 'AGL_DOUBLEBUFFER', 'AGL_STEREO',
'AGL_AUX_BUFFERS', 'AGL_RED_SIZE', 'AGL_GREEN_SIZE', 'AGL_BLUE_SIZE',
'AGL_ALPHA_SIZE', 'AGL_DEPTH_SIZE', 'AGL_STENCIL_SIZE', 'AGL_ACCUM_RED_SIZE',
'AGL_ACCUM_GREEN_SIZE', 'AGL_ACCUM_BLUE_SIZE', 'AGL_ACCUM_ALPHA_SIZE',
'AGL_PIXEL_SIZE', 'AGL_MINIMUM_POLICY', 'AGL_MAXIMUM_POLICY', 'AGL_OFFSCREEN',
'AGL_FULLSCREEN', 'AGL_SAMPLE_BUFFERS_ARB', 'AGL_SAMPLES_ARB',
'AGL_AUX_DEPTH_STENCIL', 'AGL_COLOR_FLOAT', 'AGL_MULTISAMPLE',
'AGL_SUPERSAMPLE', 'AGL_SAMPLE_ALPHA', 'AGL_RENDERER_ID',
'AGL_SINGLE_RENDERER', 'AGL_NO_RECOVERY', 'AGL_ACCELERATED',
'AGL_CLOSEST_POLICY', 'AGL_ROBUST', 'AGL_BACKING_STORE', 'AGL_MP_SAFE',
'AGL_WINDOW', 'AGL_MULTISCREEN', 'AGL_VIRTUAL_SCREEN', 'AGL_COMPLIANT',
'AGL_PBUFFER', 'AGL_BUFFER_MODES', 'AGL_MIN_LEVEL', 'AGL_MAX_LEVEL',
'AGL_COLOR_MODES', 'AGL_ACCUM_MODES', 'AGL_DEPTH_MODES', 'AGL_STENCIL_MODES',
'AGL_MAX_AUX_BUFFERS', 'AGL_VIDEO_MEMORY', 'AGL_TEXTURE_MEMORY',
'AGL_RENDERER_COUNT', 'AGL_SWAP_RECT', 'AGL_BUFFER_RECT', 'AGL_SWAP_LIMIT',
'AGL_COLORMAP_TRACKING', 'AGL_COLORMAP_ENTRY', 'AGL_RASTERIZATION',
'AGL_SWAP_INTERVAL', 'AGL_STATE_VALIDATION', 'AGL_BUFFER_NAME',
'AGL_ORDER_CONTEXT_TO_FRONT', 'AGL_CONTEXT_SURFACE_ID',
'AGL_CONTEXT_DISPLAY_ID', 'AGL_SURFACE_ORDER', 'AGL_SURFACE_OPACITY',
'AGL_CLIP_REGION', 'AGL_FS_CAPTURE_SINGLE', 'AGL_SURFACE_BACKING_SIZE',
'AGL_ENABLE_SURFACE_BACKING_SIZE', 'AGL_SURFACE_VOLATILE',
'AGL_FORMAT_CACHE_SIZE', 'AGL_CLEAR_FORMAT_CACHE', 'AGL_RETAIN_RENDERERS',
'AGL_MONOSCOPIC_BIT', 'AGL_STEREOSCOPIC_BIT', 'AGL_SINGLEBUFFER_BIT',
'AGL_DOUBLEBUFFER_BIT', 'AGL_0_BIT', 'AGL_1_BIT', 'AGL_2_BIT', 'AGL_3_BIT',
'AGL_4_BIT', 'AGL_5_BIT', 'AGL_6_BIT', 'AGL_8_BIT', 'AGL_10_BIT',
'AGL_12_BIT', 'AGL_16_BIT', 'AGL_24_BIT', 'AGL_32_BIT', 'AGL_48_BIT',
'AGL_64_BIT', 'AGL_96_BIT', 'AGL_128_BIT', 'AGL_RGB8_BIT', 'AGL_RGB8_A8_BIT',
'AGL_BGR233_BIT', 'AGL_BGR233_A8_BIT', 'AGL_RGB332_BIT', 'AGL_RGB332_A8_BIT',
'AGL_RGB444_BIT', 'AGL_ARGB4444_BIT', 'AGL_RGB444_A8_BIT', 'AGL_RGB555_BIT',
'AGL_ARGB1555_BIT', 'AGL_RGB555_A8_BIT', 'AGL_RGB565_BIT',
'AGL_RGB565_A8_BIT', 'AGL_RGB888_BIT', 'AGL_ARGB8888_BIT',
'AGL_RGB888_A8_BIT', 'AGL_RGB101010_BIT', 'AGL_ARGB2101010_BIT',
'AGL_RGB101010_A8_BIT', 'AGL_RGB121212_BIT', 'AGL_ARGB12121212_BIT',
'AGL_RGB161616_BIT', 'AGL_ARGB16161616_BIT', 'AGL_INDEX8_BIT',
'AGL_INDEX16_BIT', 'AGL_RGBFLOAT64_BIT', 'AGL_RGBAFLOAT64_BIT',
'AGL_RGBFLOAT128_BIT', 'AGL_RGBAFLOAT128_BIT', 'AGL_RGBFLOAT256_BIT',
'AGL_RGBAFLOAT256_BIT', 'AGL_NO_ERROR', 'AGL_BAD_ATTRIBUTE',
'AGL_BAD_PROPERTY', 'AGL_BAD_PIXELFMT', 'AGL_BAD_RENDINFO', 'AGL_BAD_CONTEXT',
'AGL_BAD_DRAWABLE', 'AGL_BAD_GDEV', 'AGL_BAD_STATE', 'AGL_BAD_VALUE',
'AGL_BAD_MATCH', 'AGL_BAD_ENUM', 'AGL_BAD_OFFSCREEN', 'AGL_BAD_FULLSCREEN',
'AGL_BAD_WINDOW', 'AGL_BAD_POINTER', 'AGL_BAD_MODULE', 'AGL_BAD_ALLOC',
'AGL_BAD_CONNECTION', 'aglChoosePixelFormat', 'aglDestroyPixelFormat',
'aglNextPixelFormat', 'aglDescribePixelFormat', 'aglDevicesOfPixelFormat',
'aglQueryRendererInfo', 'aglDestroyRendererInfo', 'aglNextRendererInfo',
'aglDescribeRenderer', 'aglCreateContext', 'aglDestroyContext',
'aglCopyContext', 'aglUpdateContext', 'aglSetCurrentContext',
'aglGetCurrentContext', 'aglSetDrawable', 'aglSetOffScreen',
'aglSetFullScreen', 'aglGetDrawable', 'aglSetVirtualScreen',
'aglGetVirtualScreen', 'aglGetVersion', 'aglConfigure', 'aglSwapBuffers',
'aglEnable', 'aglDisable', 'aglIsEnabled', 'aglSetInteger', 'aglGetInteger',
'aglUseFont', 'aglGetError', 'aglErrorString', 'aglResetLibrary',
'aglSurfaceTexture', 'aglCreatePBuffer', 'aglDestroyPBuffer',
'aglDescribePBuffer', 'aglTexImagePBuffer', 'aglSetPBuffer', 'aglGetPBuffer',
'aglGetCGLContext', 'aglGetCGLPixelFormat']
# END GENERATED CONTENT (do not edit above this line)



