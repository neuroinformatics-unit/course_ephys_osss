from pathlib import Path
import numpy as np
from spikeinterface.extractors import NwbRecordingExtractor


def download_and_slice_nwb_from_dandi(
    s3_url: str = "https://dandiarchive.s3.amazonaws.com/blobs/a8f/800/a8f8003e-4483-4b50-8a45-91ac5971f5d5",
    duration_s: int | None = 90,
    local_folder: str | Path = "data/nwb_first_slice"
):
    """
    Downloads and optionally slice NWB file from DANDI.

    Parameters
    ----------
    s3_url : str, default: "https://dandiarchive.s3.amazonaws.com/blobs/a8f/800/a8f8003e-4483-4b50-8a45-91ac5971f5d5"
        Path to s3 from DANDI archive.
    duration_s : int | None, default: 90
        Duration of the slice in seconds. If None, the full recording is downloaded.
    local_folder : str | Path, default: "data/nwb_first_slice"
        Local folder to save the sliced NWB file, by default "data/nwb_first_slice"
    """
    series_paths = NwbRecordingExtractor.fetch_available_electrical_series_paths(
        file_path=s3_url,
        stream_mode="remfile",
    )
    non_lfp = [p for p in series_paths if "lfp" not in p.lower()]
    electrical_series_path = (non_lfp or series_paths)[0]

    # stream_mode="remfile" (or "fsspec") reads bytes lazily over HTTP — no full download.
    rec = NwbRecordingExtractor(
        file_path=s3_url,
        stream_mode="remfile",
        electrical_series_path=electrical_series_path,
    )

    if duration_s is not None:
        end_frame = np.round(duration_s * rec.get_sampling_frequency()).astype(int)
        rec = rec.frame_slice(start_frame=0, end_frame=end_frame)

    # Create ande set 2D probe (otherwise we get 3D locations!)
    rec.set_dummy_probe_from_locations(
        rec.get_channel_locations(axes="xy")
    )

    _ = rec.save(
        format="binary",
        folder=local_folder,
        overwrite=True
    )

    print(f"Saved {s3_url} to {local_folder}!")

