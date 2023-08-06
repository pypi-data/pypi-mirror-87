from pathlib import Path
import h5py
from .parsers import make_structured_array
from .preprocess import accumulate_frames, slice_by_time
import numpy as np


class HDF5FolderDataset:
    def __init__(
        self,
        source_folder,
        transform=None,
        target_transform=None,
    ):
        types = ("**/*.h5")
        self.file_list = sorted(Path(source_folder).glob(types))
        self.transform = transform
        self.target_transform = target_transform

        if len(self.file_list) == 0:
            raise FileNotFoundError("No files found in" + str(source_folder))

    def __len__(self):
        return len(self.file_list)

    @staticmethod
    def _pick_data_from_file(file):
        raise NotImplementedError()

    def __getitem__(self, i):
        # opening file
        file = self.file_list[i]
        with h5py.File(file, "r") as F:
            data = self._pick_data_from_file(F)
            label = F["label"][()]

        if self.transform is not None:
            data = self.transform(data)
        if self.target_transform is not None:
            label = self.target_transform(label)

        return data, label


class FramesDataset(HDF5FolderDataset):
    def __init__(
        self,
        source_folder,
        transform=None,
        target_transform=None,
    ):
        super().__init__(
            source_folder=source_folder,
            transform=transform,
            target_transform=target_transform
        )

    @staticmethod
    def _pick_data_from_file(file):
        return file["frame"][()]


class SpikeTrainDataset(HDF5FolderDataset):
    def __init__(
        self,
        source_folder,
        transform=None,
        target_transform=None,
        dt=None,
        bins=None,
    ):
        super().__init__(
            source_folder=source_folder,
            transform=transform,
            target_transform=target_transform
        )

        self.dt = dt

    def _pick_data_from_file(self, file):
        xytp = make_structured_array(
            file["spikes"]["x"][()],
            file["spikes"]["y"][()],
            file["spikes"]["t"][()],
            file["spikes"]["p"][()]
        )
        bins_yx = (file["bins"]["y"][()], file["bins"]["x"][()])

        if self.dt is None:
            return xytp
        else:
            indices = slice_by_time(xytp, time_window=self.dt)
            sliced_xytp = np.split(xytp, indices)
            # TODO how should bins be provided here?
            return accumulate_frames(sliced_xytp, *bins_yx)
