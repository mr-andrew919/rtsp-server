#!/usr/bin/env python

import os
import sys
import gi
import logging

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject, GLib

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

loop = GLib.MainLoop()
Gst.init(None)

class TestRtspMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        super().__init__()

    def do_create_element(self, url):
        pipeline = (
            f"filesrc location=videos/{src_file} ! decodebin ! "
            f"x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! "
            f"rtph264pay name=pay0 config-interval=1 pt=96"
        )
        logging.info(f"GStreamer pipeline created:\n  {pipeline}")
        try:
            return Gst.parse_launch(pipeline)
        except Exception as e:
            logging.error(f"Failed to create pipeline: {e}")
            raise

class GstreamerRtspServer():
    def __init__(self):
        self.rtspServer = GstRtspServer.RTSPServer()
        factory = TestRtspMediaFactory()
        factory.set_shared(True)

        mountPoints = self.rtspServer.get_mount_points()
        mount_path = f"/{dst_stream}"
        mountPoints.add_factory(mount_path, factory)

        self.rtspServer.attach(None)
        logging.info(f"RTSP server mounted at rtsp://<host>:8554{mount_path}")

if __name__ == '__main__':
    try:
        src_file = os.environ.get('MP4_FILENAME')
        dst_stream = os.environ.get('DST_STREAM')

        if not src_file or not dst_stream:
            logging.error("Environment variables MP4_FILENAME and DST_STREAM must be set.")
            sys.exit(1)

        logging.info(f"Using MP4 file: videos/{src_file}")
        logging.info(f"RTSP stream path: /{dst_stream}")

        s = GstreamerRtspServer()
        logging.info("RTSP server started. Waiting for clients...")
        loop.run()

    except Exception as e:
        logging.exception("Unexpected error occurred:")
        sys.exit(1)
