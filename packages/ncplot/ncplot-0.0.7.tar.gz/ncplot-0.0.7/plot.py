fom .runthis import run_this

import pandas as pd, numpy as np
import hvplot.pandas
import hvplot.xarray
import subprocess
import nctoolkit as nc



def plot(ff, log = False, vars = None, panel = False):
    """
    Autoplotting method

    Parameters
    -------------
    ff: str
        File
    log: boolean
        Do you want a plotted data to be logged?
    vars: str or list
        A string or list of the variables to plot
    panel: boolean
        Do you want a panel plot, if avaiable?
    """


    if type(ff) is not str:
        raise TypeError("Not a file path!")

    cdo_result = subprocess.run("cdo ngrids " + ff, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    n_grids = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    if n_grids > 1:
        raise ValueError("Autoplot cannot work with multiple grids")

    cdo_result = subprocess.run("cdo nlevel " + ff, shell = True,stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    n_levels = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    cdo_result = subprocess.run("cdo ntime " + ff, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    n_times = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    cdo_result = subprocess.run("cdo ngridpoints " + ff, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    n_points = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    if vars is None:
        vars = self.variables

    if type(vars) is list:
        if len(vars) == 1:
            vars = vars[0]


    # Case when all you can plot is a time series, but more than one variable

    if n_times > 1 and n_points < 2 and n_levels <= 1 and type(vars) is str:

        out = subprocess.run("cdo griddes " + ff, shell = True, stdout=subprocess.PIPE, stderr =subprocess.PIPE)
        lon_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x][0].split(" ")[-1]
        lat_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x][0].split(" ")[-1]
        data = self.to_xarray()
        data = data.squeeze([lon_name, lat_name])
        data = data.rename({vars: "x"})
        return data.x.hvplot()

    if n_times > 1 and n_points < 2 and n_levels <= 1 and type(vars) is list:

        df = self.to_xarray()

        dim_dict = dict(df.dims)
        to_go = []
        for kk in dim_dict.keys():
            if dim_dict[kk] == 1:
                df = df.squeeze(kk)
                to_go.append(kk)

        df = df.to_dataframe()
        df = df.drop(columns = to_go)

        if panel:
            return df.reset_index().set_index("time").loc[:, vars].reset_index().melt("time").set_index("time").hvplot(by = "variable", logy = log, subplots = True, shared_axes = False)
        else:
            return df.reset_index().set_index("time").loc[:, vars].reset_index().melt("time").set_index("time").hvplot(groupby = "variable", logy = log, dynamic = True)

    if n_points > 1 and type(vars) is str:
        out = subprocess.run("cdo griddes " + ff, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
        lon_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x][-1].split(" ")[-1]
        lat_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x][-1].split(" ")[-1]

        self_max = self.to_xarray().rename({vars: "x"}).x.max()
        self_min = self.to_xarray().rename({vars: "x"}).x.min()
        v_max = max(self_max.values, -self_min.values)
        if self_max.values > 0 and self_min.values < 0:
            return self.to_xarray().hvplot.image(lon_name, lat_name, vars, dynamic = True,  logz = log, cmap = "seismic").redim.range(**{vars:(-v_max, v_max)})
        else:
            return self.to_xarray().hvplot.image(lon_name, lat_name, vars, dynamic = True,  logz = log, cmap = "viridis").redim.range(**{vars:(-self_min.values, v_max)})

    if n_points > 1 and n_levels <=1  and type(vars) is list:
        out = subprocess.run("cdo griddes " + ff, shell = True, stdout=subprocess.PIPE, stderr =subprocess.PIPE)
        lon_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x][-1].split(" ")[-1]
        lat_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x][-1].split(" ")[-1]

        return self.to_xarray().hvplot.image(lon_name, lat_name, vars, dynamic = True, cmap = "viridis", logz = log)



    # Throw an error if case has not plotting method available yet

    raise ValueError("Autoplot method for this type of data is not yet available!")



