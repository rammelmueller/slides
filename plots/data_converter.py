import h5py as hdf
import pandas as pd
import re


class DataConverter(object):
    """ A containter that converts a HDF5 file to a pandas dataframe. The groups
        are ordered hierarchically, such as

            /a_1/b_2/d_3/variable_1
            /a_1/b_2/d_3/variable_2

        which will result in a pandas dataframe with entries like

            a     b    d    variable_1        variable_2
            1     2    3    variable_1[...]   variable_2[...]

        One row in the dataframe is created per leaf in the hierarchial tree and
        all datasets are further columns.

        What the converter does:
            - find the structure of the resulting pandas.DataFrame. This means
              that we are looking for all possible parameters, even if they are
              heterogeneous - missing values will be filled with None.
            - the dataframe is filled with all datasets that meet that structure.

    """
    def __init__(self, hdf5_file, skip=1):
        # Find the columns and variables for the Dataframe. For safety, it is
        # important to create sorted lists from the generated sets.
        self.skip = skip
        self.cols, self.variables = set(), set()
        hdf5_file.visititems(self._find_structure)
        self.cols, self.variables = sorted(list(self.cols)), sorted(list(self.variables))

        # Produce an empty dataframe & fill it up.
        self.data = pd.DataFrame([], columns=self.cols+self.variables)
        hdf5_file.visititems(self._extract)


    def _param_from_group(self, grp):
        """ Splits a path of a h5py.DataSet into it's parameters and returns a dictionary.
        """
        return dict([('_'.join(pair.split('_')[:-1]), pair.split('_')[-1]) for pair in list(filter(None, re.split('/', str(grp))[self.skip:]))[:-1]])


    def _find_structure(self, name, node):
        """ Whenever a h5py.DataSet is encountered, the columns and variables are
            updated sucht that in the end a full, heterogeneous dataset can be
            mapped.
        """
        if isinstance(node, hdf.Dataset):
            self.cols.update(self._param_from_group(name).keys())
            self.variables.update(map(str, node.parent.keys()))
        return None


    def _extract(self, name, node):
        """ Is mapped on the hdf5 file. When a hdf.DataSet is found, the values
            are transfered to the pandas.DataFrame.
        """
        if isinstance(node, hdf.Dataset):
            # First, read the parameter values into a dictionary.
            vals = self._param_from_group(name)

            # Get the current variable's value.
            variable = str(name).replace(str(node.parent.name[1:]), "")[1:]
            var_vals = {v : None for v in self.variables}
            var_vals[variable] = node[...]

            # Now produce the row in the pandas.DataFrame. Try to convert values to float,
            # if not possible, use the string. If the parameter does not exist, we should
            # append None, as then it is possible to deal with heterogeneous data.
            row_data = []
            for col in self.cols:
                try:
                    row_data.append(float(vals[col]))
                except ValueError:
                    row_data.append(str(vals[col]))
                except KeyError:
                    row_data.append(None)
            row_data += [var_vals[v] for v in self.variables]
            row = pd.DataFrame([row_data], columns=self.cols+self.variables)

            # Add to the list of extracted values.
            self.data = pd.concat([row, self.data], ignore_index=True)

        return None
