"""Preprocessing steps script.

Functional code extracted from ``book/preproecssing-steps-coding.qmd``.
Runs the full preprocessing walkthrough: download data, bandpass filter,
bad channel detection, common median reference, highpass spatial filter,
motion correction and whitening.
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import spikeinterface.preprocessing as si_prepro
import spikeinterface.widgets as si_widgets
import spikeinterface.sorters as si_sorters
from spikeinterface.extractors import NwbRecordingExtractor
import spikeinterface as si

TIME_RANGE = (49, 49.01)
PLOT = False

def plot_prepro(recordings: dict, time_range: tuple[float]) -> None:
    """Plot one or more recordings side by side as heat maps for comparison."""
    fig, axes = plt.subplots(
        1, len(recordings), figsize=(6 * len(recordings), 5),
        squeeze=False, layout="constrained",
    )
    for ax, (name, recording) in zip(axes.ravel(), recordings.items()):
        si_widgets.plot_traces(
            recording,
            time_range=time_range,
            mode="map",
            ax=ax,
            with_colorbar=True,
            clim=(-300,300)
        )
        ax.set_title(name)
    plt.show()

# ---------------------------------------------------------------------------
# Downloading the data
# ---------------------------------------------------------------------------
s3_url = "https://dandiarchive.s3.amazonaws.com/blobs/a8f/800/a8f8003e-4483-4b50-8a45-91ac5971f5d5"
DURATION_S = 90
LOCAL_FOLDER = Path("nwb_first_slice")

if not LOCAL_FOLDER.exists():

    series_paths = NwbRecordingExtractor.fetch_available_electrical_series_paths(
        file_path=s3_url,
        stream_mode="remfile",
    )

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

    recording = rec_slice_remote.save(
        format="binary",
        folder=LOCAL_FOLDER,
        n_jobs=1,
        chunk_duration="1s",
        progress_bar=True,
        overwrite=True,
    )
else:
    recording = si.load(LOCAL_FOLDER)

# ---------------------------------------------------------------------------
# Bandpass filtering
# ---------------------------------------------------------------------------
recording_bp = si_prepro.bandpass_filter(
    recording, freq_min=300, freq_max=6000
)  # common values used based on AP waveform kinetics

if PLOT:
    plot_prepro({"raw": recording, "filtered": recording_bp}, TIME_RANGE)


# ---------------------------------------------------------------------------
# Bad channel detection
# ---------------------------------------------------------------------------
bad_channel_ids_1, channel_labels_1 = si_prepro.detect_bad_channels(recording_bp)
print("first attempt labels:\n", channel_labels_1)

rec_clean_1 = recording_bp.remove_channels(bad_channel_ids_1)
if PLOT:
    plot_prepro({"filtered": recording_bp, "bad channels removed": rec_clean_1}, TIME_RANGE)

# Try again with different settings
bad_channel_ids, channel_labels = si_prepro.detect_bad_channels(
    recording_bp, dead_channel_threshold=-0.25
)
print("second attempt labels:\n", channel_labels)

rec_clean = recording_bp.remove_channels(bad_channel_ids)
if PLOT:
    plot_prepro({"filtered": recording_bp, "bad channels removed": rec_clean}, TIME_RANGE)


# ---------------------------------------------------------------------------
# Common median referencing
# ---------------------------------------------------------------------------
recording_cmr = si_prepro.common_reference(rec_clean, operator="median")
if PLOT:
    plot_prepro({"filtered": rec_clean, "recording_cmr": recording_cmr}, TIME_RANGE)

# Highpass spatial filter
recording_hsf = si_prepro.highpass_spatial_filter(rec_clean)
if PLOT:
    plot_prepro({"recording_cmr": recording_cmr, "recording_hsf": recording_hsf}, TIME_RANGE)


# ---------------------------------------------------------------------------
# Motion correction
# ---------------------------------------------------------------------------
rec_corrected, motion_info = si_prepro.correct_motion(
    recording_cmr,
    preset="dredge_fast",
    output_motion_info=True,
)
print(rec_corrected)

# Display the motion output: drift map + estimated motion over depth/time.
fig = plt.figure(figsize=(14, 8))
si_widgets.plot_motion_info(
    motion_info,
    recording=rec_corrected,
    figure=fig,
    color_amplitude=True,
    amplitude_cmap="inferno",
    scatter_decimate=10,
)
fig.suptitle("Motion correction output")
plt.show()

# ---------------------------------------------------------------------------
# Whitening
# ---------------------------------------------------------------------------
recording_whiten = si_prepro.whiten(rec_corrected)

plot_prepro({"rec_corrected": rec_corrected, "whitened": recording_whiten}, TIME_RANGE)

# For visualisation, rescale the recording (only for course visualisation, not analysis).
start_frame = int(51.475 * rec_corrected.get_sampling_frequency())
end_frame = int(51.55 * rec_corrected.get_sampling_frequency())

#noise = rec_corrected.get_traces(start_frame=start_frame, end_frame=end_frame, return_in_uV=True)
noise = np.median(
    si.get_noise_levels(rec_corrected, return_in_uV=False, method="mad")
)
print("noise level", noise)

scaled_white_recording = si_prepro.scale(recording_whiten, noise)

plot_prepro(
    {"rec_corrected": rec_corrected, "scaled_white_recording": scaled_white_recording},
    (51.475, 51.55),
)

first_data = rec_corrected.get_traces(start_frame=start_frame, end_frame=end_frame, return_in_uV=True)
third_data = scaled_white_recording.get_traces(start_frame=start_frame, end_frame=end_frame, return_in_uV=True)

# We add the offset with np.arange so the traces are vertically separated
plt.figure()
plt.plot(first_data + np.arange(first_data.shape[1]) * 1000, color="k")
plt.plot(third_data + np.arange(third_data.shape[1]) * 1000, color="r")
plt.xlabel("sample number")
plt.show()

# breakpoint()

# ---------------------------------------------------------------------------
# Spike sorting (remember to turn off KS internal preprocessing)
# ---------------------------------------------------------------------------
if False:
    sorting = si_sorters.run_sorter(
        "kilosort4",
        recording_whiten,
        folder="ks4_out",
        remove_existing_folder=True,
        verbose=True,
        skip_kilosort_preprocessing=True,
        do_correction=False,
    )
    print(sorting)


plt.show()
