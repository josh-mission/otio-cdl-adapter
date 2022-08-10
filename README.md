# CDL Export Adapter
This simple adapter allows users to export a collection of .cdl files
from an OTIO timeline. One .cdl file is exported for each clip/timeline event in the 
OTIO instance. The ColorCorrection Node ID within the .cdl will use the
CMX_3600 reel name/Tape of the clip, while the file itself will be named
using the timeline event name.

## Usage
`otio.adapters.write_to_file(timeline, 'path/to/output/directory', adapter_name='cdl')`