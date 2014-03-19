# Software License Agreement (BSD License)
#
# Copyright (c) 2010, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
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
#
# Revision $Id$

"""
rosh_base is a meta-plugin that loads in plugins contained in the
'base' variant of ROS.
"""

import roslib; roslib.load_manifest('rosh_visualization')

import os

import roslib.names

import rosh.impl.proc
import rosh.plugin
import rosh_common

def rosh_plugin_load(plugin_context, globals_=None):
    """
    Initialize rosh_common plugin
    """
    # make sure common is loaded first
    rosh.plugin.load_plugin('rosh_common', plugin_context, globals_=globals_)

    plugin = rosh.plugin.PluginData()
    plugin.add_handler(rosh_common.PLUGIN_CAMERAS_SHOW, show_camera_rviz_image_view)
    return plugin

def show_camera_rviz_image_view(ns_obj):
    """
    show camera handler that uses rviz's image_view.

    @return: image viewer node (if single camera), or tuple of image viewer nodes (if stereo)
    @rtype: Node or (Node, Node)
    """
    #NOTE: we avoid the non-rviz image_view at all costs because it is
    #ill-behaved and doesn't perform as well.

    if ns_obj._cam_info is None:
        # check to see if it's stereo
        l = ns_obj._getAttributeNames()
        if 'left' in l and 'right' in l:
            n1 = show_camera_rviz_image_view(ns_obj.left)
            n2 = show_camera_rviz_image_view(ns_obj.right)
            return n1, n2
        else:
            # NOTE: this will block
            try:
                ns_obj._init_cam_info()
            except:
                print >> sys.stderr, "%s does not appear to be a camera topic"%ns_obj._name
                return None
            
    # retrieve ctx object
    ctx = ns_obj._config.ctx
    topic = roslib.names.ns_join(ns_obj._name, 'image_raw')
    node = ctx.launch('image_view', 'image_view', remap={'image': topic})
    print "running image_view, this may be slow over a wireless network"
    return node
