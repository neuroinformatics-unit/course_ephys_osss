from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import spikeinterface as si
import spikeinterface.preprocessing as si_prepro
import spikeinterface.widgets as si_widgets

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

LOCAL_FOLDER = Path("_tmp/nwb_first_slice")
S3_URL = "https://dandiarchive.s3.amazonaws.com/blobs/a8f/800/a8f8003e-4483-4b50-8a45-91ac5971f5d5"
DURATION_S = 90
TIME_RANGE = (49, 49.02)


def load_recording():
    if not LOCAL_FOLDER.exists():
        download_and_slice_nwb_from_dandi(
            s3_url=S3_URL,
            duration_s=DURATION_S,
            local_folder=LOCAL_FOLDER,
        )

    return si.load(LOCAL_FOLDER)


def plot_prepro(recordings: dict, time_range: tuple[float, float]) -> None:
    fig, axes = plt.subplots(
        1,
        len(recordings),
        figsize=(6 * len(recordings), 5),
        squeeze=False,
        layout="constrained",
    )

    for ax, (name, recording) in zip(axes.ravel(), recordings.items()):
        si_widgets.plot_traces(
            recording,
            time_range=time_range,
            mode="map",
            ax=ax,
            with_colorbar=True,
        )
        ax.set_title(name)


def main():
    recording = load_recording()

    recording_bp = si_prepro.bandpass_filter(
        recording,
        freq_min=300,
        freq_max=6000,
    )
    plot_prepro({"raw": recording, "filtered": recording_bp}, time_range=(0, 5))
    plt.show()

    plot_prepro({"raw": recording, "filtered": recording_bp}, time_range=TIME_RANGE)
    plt.show()

    bad_channel_ids_1, channel_labels_1 = si_prepro.detect_bad_channels(recording_bp)
    print("first attempt labels:\n", channel_labels_1)

    rec_clean_1 = recording_bp.remove_channels(bad_channel_ids_1)
    plot_prepro({"filtered": recording_bp, "bad channels removed": rec_clean_1}, TIME_RANGE)
    plt.show()

    bad_channel_ids, channel_labels = si_prepro.detect_bad_channels(
        recording_bp,
        dead_channel_threshold=-0.25,
    )
    print("second attempt labels:\n", channel_labels)

    rec_clean = recording_bp.remove_channels(bad_channel_ids)
    plot_prepro({"filtered": recording_bp, "bad channels removed": rec_clean}, TIME_RANGE)
    plt.show()

    recording_cmr = si_prepro.common_reference(rec_clean, operator="median")
    plot_prepro({"filtered": rec_clean, "recording_cmr": recording_cmr}, TIME_RANGE)
    plt.show()

    recording_hsf = si_prepro.highpass_spatial_filter(rec_clean)
    plot_prepro({"recording_cmr": recording_cmr, "recording_hsf": recording_hsf}, TIME_RANGE)
    plt.show()

    rec_corrected, motion_info = si_prepro.correct_motion(
        recording_cmr,
        preset="dredge_fast",
        estimate_motion_kwargs={"rigid": True},
        output_motion_info=True,
    )
    print(rec_corrected)

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

    recording_whiten = si_prepro.whiten(rec_corrected)
    plot_prepro({"rec_corrected": rec_corrected, "whitened": recording_whiten}, TIME_RANGE)
    plt.show()

    time_range = TIME_RANGE
    start_frame = int(time_range[0] * rec_corrected.get_sampling_frequency())
    end_frame = int(time_range[1] * rec_corrected.get_sampling_frequency())

    noise = np.mean(si.get_noise_levels(rec_corrected, return_in_uV=False, method="std"))
    scaled_white_recording = si_prepro.scale(recording_whiten, noise)

    plot_prepro({"rec_corrected": rec_corrected, "scaled_white_recording": scaled_white_recording}, time_range,)
    plt.show()

    orig_data = rec_corrected.get_traces(start_frame=start_frame, end_frame=end_frame, return_in_uV=True,)[200:400, :4]

    whitened_data = scaled_white_recording.get_traces(start_frame=start_frame, end_frame=end_frame, return_in_uV=True,)[200:400, :4]

    plt.figure(figsize=(8, 5))
    plt.plot(orig_data + np.arange(orig_data.shape[1]) * 750, color="k")
    plt.plot(whitened_data + np.arange(whitened_data.shape[1]) * 750, color="r")
    plt.xlabel("sample number")
    plt.show()

if __name__ == "__main__":
    main()