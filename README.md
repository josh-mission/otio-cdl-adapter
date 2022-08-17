# OpenTimelineIO - CDL Export Adapter
This simple adapter allows users to export a collection of .cdl files
from an OTIO instance. 

One .cdl file is exported for each clip in the OTIO instance 
(supports both Timeline and SerializableCollection OTIO schemas).

The ColorCorrection Node ID within the .cdl will use the
CMX_3600 reel name/Tape of the clip, while the file itself will be named
using the timeline event/clip name.

Please note, you must provide directory (not a file) as the output parameter.\
Due to this, you must also manually provide the adapter_name as a named
parameter as there is no file extension for otio to automatically select it.

## Usage
`otio.adapters.write_to_file(timeline, 'path/to/output/directory', adapter_name='cdl')`