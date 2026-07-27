from pathlib import Path
import numpy as np
from spikeinterface.extractors import NwbRecordingExtractor

s3_url = "https://dandiarchive.s3.amazonaws.com/blobs/a8f/800/a8f8003e-4483-4b50-8a45-91ac5971f5d5"
DURATION_S = 90
LOCAL_FOLDER = Path("nwb_first_slice")

series_paths = NwbRecordingExtractor.fetch_available_electrical_series_paths(
        file_path=s3_url,
        stream_mode="remfile",
    )

# TODO: Explain the series
for p in series_paths:
    print("  -", p)

non_lfp = [p for p in series_paths if "lfp" not in p.lower()]
electrical_series_path = (non_lfp or series_paths)[0]

# stream_mode="remfile" (or "fsspec") reads bytes lazily over HTTP — no full download.
rec = NwbRecordingExtractor(
    file_path=s3_url,
    stream_mode="remfile",
    electrical_series_path=electrical_series_path,
)

end_frame = np.round(DURATION_S * rec.get_sampling_frequency()).astype(int)
rec_slice_remote = rec.frame_slice(start_frame=0, end_frame=end_frame)

# Create ande set 2D probe (otherwise we get 3D locations!)
rec_slice_remote.set_dummy_probe_from_locations(
    rec.get_channel_locations(axes="xy")
)

recording = rec_slice_remote.save(
    format="binary",
    folder=LOCAL_FOLDER,
    n_jobs=1,
    chunk_duration="1s",
    progress_bar=True,
    overwrite=True
)