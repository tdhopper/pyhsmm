from __future__ import division
from IPython.parallel import Client
from IPython.parallel.util import interactive

# the ipcluster should be set up before this file is imported
c = Client()
dv = c.direct_view()
dv.execute('import pyhsmm')
lbv = c.load_balanced_view()

# these dicts need to be populated by hand before calling build_states*,
# both locally (in this module) and in the ipython top-level module on every
# engine
# the second dict only needs to be used when calling build_states_changepoints
alldata = None
allchangepoints = None

# these functions function are run on the engines, and expects the alldata (and
# allchangepoints) global(s) as well as the current model hsmm_subhmms_model to be
# present in the ipython global frame
@lbv.parallel(block=True)
@interactive
def build_states(data_id):
    global hsmm_subhmms_model
    global alldata

    # adding the data to the pushed global model will build a substates object
    # and resample the states given the parameters in the model
    hsmm_subhmms_model.add_data(alldata[data_id])
    hsmm_subhmms_model.states_list[-1].data_id = data_id

    # return the relevant tuple of
    # (data_id, superstateseq, [substateseq1, substateseq2, ... ])
    return (data_id,
            hsmm_subhmms_model.states_list[-1].get_states())

@lbv.parallel(block=True)
@interactive
def build_states_changepoints(data_id):
    global hsmm_subhmms_model
    global alldata, allchangepoints

    hsmm_subhmms_model.add_data(alldata[data_id],allchangepoints[data_id])
    hsmm_subhmms_model.states_list[-1].data_id = data_id

    return (data_id,
            hsmm_subhmms_model.states_list[-1].get_states())
