# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the OpenTimelineIO project

"""
This simple adapter allows users to export a collection of .cdl files
from an OTIO timeline. One .cdl file is exported for each clip/timeline event
in theOTIO instance. The ColorCorrection Node ID within the .cdl will use the
CMX_3600 reel name/Tape of the clip, while the file itself will be named
using the timeline event name.

To use:
otio.adapters.write_to_file(
    timeline,
    'path/to/output/directory',
    adapter_name='cdl'
)
"""
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from otio_cdl_adapter.utils import secure_filename


def get_reel_name_from_clip(clip):
    # Tries to get the reelname of a clip from all the possible locations
    # (varies based on input)

    # Reelname location for EDL sources
    reel_name = clip.metadata.get("cmx_3600", {}).get("reel")

    if not reel_name:
        # Reelname location for ALE sources
        reel_name = clip.metadata.get('ALE', {}).get("Tape")

    if not reel_name:
        # Reelname location for xml sources
        reel_name = clip.media_reference.metadata.get('fcp_xml', {}).get(
            "reel", {}).get('name')

    if not reel_name:
        # Resort to using clip name if no reel name is found.
        reel_name = clip.name

    return reel_name


def convert_to_cdl(clip):
    slope_src = clip.metadata["cdl"]["asc_sop"]["slope"]
    offset_src = clip.metadata["cdl"]["asc_sop"]["offset"]
    power_src = clip.metadata["cdl"]["asc_sop"]["power"]
    saturation_src = clip.metadata["cdl"]["asc_sat"]
    reel_name = get_reel_name_from_clip(clip)

    slope = " ".join(str("{:.6f}".format(x)) for x in slope_src)
    offset = " ".join(str("{:.6f}".format(x)) for x in offset_src)
    power = " ".join(str("{:.6f}".format(x)) for x in power_src)
    saturation = str("{:.6f}".format(saturation_src))

    color_decision_list = ET.Element(
        "ColorDecisionList",
        xmlns="urn:ASC:CDL:v1.01"
    )
    color_decision = ET.SubElement(color_decision_list, "ColorDecision")
    color_correction = ET.SubElement(
        color_decision,
        "ColorCorrection",
        id=reel_name
    )

    sop_node = ET.SubElement(color_correction, "SOPNode")
    ET.SubElement(sop_node, "Slope").text = slope
    ET.SubElement(sop_node, "Offset").text = offset
    ET.SubElement(sop_node, "Power").text = power

    sat_node = ET.SubElement(color_correction, "SATNode")
    ET.SubElement(sat_node, "Saturation").text = saturation

    tree = ET.ElementTree(color_decision_list)

    # Python 3.8 doesn't support ET.indent(), using minidom as a workaround.
    stringified = ET.tostring(tree.getroot(), 'utf-8')
    reparsed = minidom.parseString(stringified)

    return reparsed.toprettyxml(indent="    ", encoding='utf-8')


def create_cdl_file(clip, output_dir_path):
    try:
        cdl_filepath = os.path.join(
            output_dir_path,
            secure_filename(clip.name + ".cdl")
        )
        cdl_string = convert_to_cdl(clip)

        with open(cdl_filepath, "w") as f:
            f.write(str(cdl_string.decode('utf-8')))
    finally:
        pass


def extract_cdls_from_timeline(otio_timeline, output_dir_path):
    for track in otio_timeline.tracks:
        if track.kind == "Video":  # Don't parse audio tracks
            for timeline_event in track:
                if "cdl" in timeline_event.metadata:
                    create_cdl_file(timeline_event, output_dir_path)


def extract_cdls_from_serializable_collection(
        otio_serializable_collection,
        output_dir_path
):
    for clip in otio_serializable_collection:
        if type(clip).__name__ == "Clip":
            create_cdl_file(clip, output_dir_path)


def write_to_file(input_otio, filepath):
    """
      Required OTIO function hook.
      Actually writes to multiple .cdl files (one per clip in an otio instance)
      filepath parameter should be a directory where the CDLs should be saved.
    """
    output_dir_path = filepath

    if os.path.isdir(output_dir_path):
        if type(input_otio).__name__ == 'Timeline':
            extract_cdls_from_timeline(input_otio, output_dir_path)
        elif type(input_otio).__name__ == 'SerializableCollection':
            extract_cdls_from_serializable_collection(
                input_otio,
                output_dir_path
            )
    else:
        err = filepath + " is not a valid directory, " \
                         "please create it and run again."
        raise RuntimeError(err)
