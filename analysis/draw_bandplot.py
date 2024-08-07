
#!/afs/cern.ch/work/k/kmotaama/miniforge3/envs/test/bin/python

import uproot

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.CMS)

from tools.utils import *
from collections import OrderedDict

input_folder = "/afs/cern.ch/work/k/kmotaama/public/top_exotic/analysis/combine"
GREEN = (0.,0.8,0.)
YELLOW = (1.,0.8,0.)


def draw(data):
    x = list(data.keys())
    limit_2sn = [data[m][0] for m in data]
    limit_1sn = [data[m][1] for m in data]
    limit = [data[m][2] for m in data]
    limit_1sp = [data[m][3] for m in data]
    limit_2sp = [data[m][4] for m in data]
    
    f, ax = plt.subplots()
    ax.set_xlim(min(x), max(x))
    ax.set_yscale('log')
    ax.set_ylim(1e-6, 1e-1)
    ax.set_ylabel(r"B($t \rightarrow cS$) $\times$ B($S \rightarrow b \bar b$)")
    ax.set_xlabel(r"m$_S$ [GeV]")

    limit_line, = ax.plot(x, limit, "--", c='black')
    limit_2s_poli = ax.fill_between(x, limit_2sn, limit_2sp, color=YELLOW)
    limit_1s_poli = ax.fill_between(x, limit_1sn, limit_1sp, color=GREEN)
    
    ax.legend([limit_line, limit_1s_poli, limit_2s_poli], [r"95 % CL expected limit", r"Expected $\pm$ 1 $\sigma$", r"Expected $\pm$ 2 $\sigma$"])
    f.savefig("limit.png")
    

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Plot the nll")
    parser.add_argument("--inputs", help="Path to yaml input file", required=True, nargs="+")

    args = parser.parse_args()
    
    plt_data = {}
    
    for i in args.inputs:
        config = load_yaml(i)
        mass = config['mass']
        for p in config['processes']:
            if p['type'] == 'signal': xsec = p['xsec']
            
        tagname = get_tagname(i)
        combine_file = f"{input_folder}/combine_{tagname}/higgsCombineTest.AsymptoticLimits.mH120.root"
        
        with uproot.open(combine_file) as f:
            limit = f['limit']['limit'].arrays().limit
            br_limit = get_br_lim(xsec, limit)
            plt_data[mass] = br_limit

    plt_data = OrderedDict(sorted(plt_data.items()))
    draw(plt_data)
            
            
            