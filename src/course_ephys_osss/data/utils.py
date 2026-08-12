from pathlib import Path
import numpy as np
from spikeinterface.extractors import NwbRecordingExtractor
from pynwb import NWBHDF5IO
from pynwb.ecephys import ElectricalSeries, LFP

def download_and_slice_nwb_from_dandi(
    s3_url: str,
    duration_s: int | None,
    local_folder: str | Path 
):
    """
    Downloads and optionally slice NWB file from DANDI.

    Parameters
    ----------
    s3_url : str
        Path to s3 from DANDI archive.
    duration_s : int | None
        Duration of the slice in seconds. If None, the full recording is downloaded.
    local_folder : str | Path, default: 
        Local folder to save the sliced NWB file.
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


def strip_recording_from_nwb(
    nwb_path: str | Path,
    output_path: str | Path | None = None,
    drop_interfaces: tuple[str, ...] = ("Accelerometer",),
) -> Path:
    """
    Strip raw electrical series from an NWB file, keeping spike times and behaviour.

    Removes all ``ElectricalSeries`` (raw/LFP traces) from acquisition and
    processing modules, then writes a new NWB file containing everything else
    (e.g. the ``units`` table and behavioural data). The kept data is copied
    into the new file rather than linked back to the source.

    Parameters
    ----------
    nwb_path : str | Path
        Path to the source NWB file.
    output_path : str | Path | None, default: None
        Path to write the stripped NWB file. If None, ``_stripped`` is appended
        to the source file name.
    drop_interfaces : tuple[str, ...], default: ("Accelerometer",)
        Names of additional processing data interfaces to drop (e.g. the large
        raw ``Accelerometer`` stream). Pass an empty tuple to keep everything
        except the electrical series.

    Returns
    -------
    Path
        The path to the stripped NWB file.
    """
    nwb_path = Path(nwb_path)

    if output_path is None:
        output_path = nwb_path.with_name(f"{nwb_path.stem}_stripped.nwb")
    output_path = Path(output_path)

    with NWBHDF5IO(str(nwb_path), mode="r") as read_io:
        nwbfile = read_io.read()

        # Drop raw traces stored directly in acquisition.
        for name in list(nwbfile.acquisition.keys()):
            if isinstance(nwbfile.acquisition[name], (ElectricalSeries, LFP)):
                nwbfile.acquisition.pop(name)

        # Drop traces stored inside processing modules (e.g. an 'ecephys' LFP),
        # plus any explicitly requested interfaces (e.g. a large Accelerometer).
        for module in nwbfile.processing.values():
            for name in list(module.data_interfaces.keys()):
                if name in drop_interfaces or isinstance(
                    module[name], (ElectricalSeries, LFP)
                ):
                    module.data_interfaces.pop(name)

        # link_data=False copies the kept data into the new file instead of
        # linking back to the (large) source file.
        with NWBHDF5IO(str(output_path), mode="w") as export_io:
            export_io.export(
                src_io=read_io,
                nwbfile=nwbfile,
                write_args={"link_data": False},
            )

    print(f"Saved stripped NWB to {output_path}!")

    return output_path