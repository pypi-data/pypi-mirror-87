
import numpy as np
import sidpy
import h5py
import pyNSID
import ipywidgets as widgets
from IPython.display import display

class ChooseDataset(object):
    def __init__(self, input_object):
        if isinstance(input_object, sidpy.Dataset):
            if isinstance(input_object.h5_dataset, h5py.Dataset):
                self.current_channel = input_object.h5_dataset.parent
        elif isinstance(input_object, h5py.Group):
            self.current_channel = input_object
        elif isinstance(input_object, h5py.Dataset):
            self.current_channel = input_object.parent
        else:
            raise ValueError('Need hdf5 group or sidpy Dataset to determine image choices')
        self.dataset_names = []
        self.dataset_list = []
        self.dataset_type = None
        self.dataset = None
        self.reader = pyNSID.NSIDReader(self.current_channel)

        self.get_dataset_list()
        self.select_image = widgets.Dropdown(options=self.dataset_names,
                                             value=self.dataset_names[0],
                                             description='Select image:',
                                             disabled=False,
                                             button_style='')
        display(self.select_image)

        self.select_image.observe(self.set_dataset, names='value')
        self.set_dataset(0)
        self.select_image.index = (len(self.dataset_names) - 1)

    def get_dataset_list(self):
        datasets = self.reader.read()
        for dset in datasets[::-1]:
            if self.dataset_type is None:
                self.dataset_names.append('/'.join(dset.title.replace('-', '_').split('/')[-2:]))
                self.dataset_list.append(dset)
            else:
                if dset.data_type == self.data_type:
                    self.dataset_names.append('/'.join(dset.title.replace('-', '_').split('/')[-2:]))
                    self.dataset_list.append(dset)

    def set_dataset(self, b):
        index = self.select_image.index
        self.dataset = self.dataset_list[index]


def get_dimensions_by_order(dims_in, dataset):
    if isinstance(dims_in, int):
        dims_in = [dims_in]
    dims_out = []
    for item in dims_in:
        if isinstance(item, int):
            if item in dataset._axes:
                dims_out.append([item, dataset._axes[item]])
    return dims_out


def get_dimensions_by_type(dims_in, dataset):
    if isinstance(dims_in, (str, sidpy.DimensionTypes)):
        dims_in = [dims_in]
    for i in range(len(dims_in)):
        if isinstance(dims_in[i], str):
            dims_in[i] = sidpy.DimensionTypes[dims_in[i].upper()]
    dims_out = []
    for dim, axis in dataset._axes.items():
        if axis.dimension_type in dims_in:
            dims_out.append([dim, dataset._axes[dim]])
    return dims_out


def make_dummy_dataset(value_type):
    assert isinstance(value_type, sidpy.DataTypes)
    if type == sidpy.DataTypes.SPECTRUM:
        dataset = sidpy.Dataset.from_array(np.arange(100))
        dataset.data_type = 'spectrum'
        dataset.units = 'counts'
        dataset.quantity = 'intensity'

        dataset.set_dimension(0, sidpy.Dimension(np.arange(dataset.shape[0]) + 70, name='energy_scale'))
        dataset.dim_0.dimension_type = 'spectral'
        dataset.dim_0.units = 'eV'
        dataset.dim_0.quantity = 'energy loss'
    else:
        raise NotImplementedError('not implemented')
    return dataset


def plot(dataset):
    dataset.plot()


def get_image_dims(dataset):
    image_dims = []
    for dim, axis in dataset._axes.items():
        if axis.dimension_type == sidpy.DimensionTypes.SPATIAL:
            image_dims.append(dim)
    return image_dims


def get_extent(dataset):
    image_dims = get_image_dims(dataset)
    return dataset.get_extent(image_dims)
