import pandas as pd


def load_comparison(data_dir):
    #Some comparisons for the unitary Fermi gas, mostly discretized plots.
    compare = {
        # Original (from authors).
        'lw_enss_kk0_ttf' : pd.read_csv(data_dir + 'lw_enss_compressibility.dat', sep=',', header=1), # Enss
        'lw_enss_cc0_ttf' : pd.read_csv(data_dir + 'lw_enss_spinSusceptibility.dat', sep=',', header=1), # Enss
        'lw_enss_cv_ttf' : pd.read_csv(data_dir + 'lw_enss_specificheat.txt', sep=',', header=5), # Enss
        'bdmc_density' : pd.read_csv(data_dir + 'bdmc_vanHoucke_density.dat', sep=',', header=1), # Drut
        'dhmc_drut_density' : pd.read_csv(data_dir + 'dhmc_drut_density.txt', sep=',', header=1), # Drut
        'lw_frank_thermo' : pd.read_csv(data_dir + 'lw_frank_td_uni_pol.txt', sep='\s+', header=0), # Frank
        'lw_frank_phase_hom' : pd.read_csv(data_dir + 'lw_frank_uni_crit_hom.txt', sep='\s+', header=0), # Frank
        'lw_frank_phase_fflo' : pd.read_csv(data_dir + 'lw_frank_uni_crit_FFLO.txt', sep='\s+', header=0), # Frank


        # Digitized.
        'mit_ttfu_p' : pd.read_csv(data_dir + 'exp_MIT_PD.dat', sep=',', header=1), # Digitized
        'mit_transition': pd.read_csv(data_dir + 'exp_MIT_transition.dat', sep=',', header=1), # Zwierlein
        'mit_nn0_bmu' : pd.read_csv(data_dir + 'exp_MIT_density.dat', sep=',', header=1), # Zwierlein
        'mit_pp0_bmu' : pd.read_csv(data_dir + 'exp_MIT_pressure.dat', sep=',', header=1), # Digitized
        'mit_ee0_ttf' : pd.read_csv(data_dir + 'exp_MIT_energy.dat', sep=',', header=1), # Zwierlein
        'mit_kk0_pp0' : pd.read_csv(data_dir + 'exp_MIT_compressibility_pp0.dat', sep=',', header=1), # Digitized
        'mit_kk0_ttf' : pd.read_csv(data_dir + 'exp_MIT_compressibility_ttf.dat', sep=',', header=1), # Digitized
        'mit_cvn_ttf' : pd.read_csv(data_dir + 'exp_MIT_specificHeat.dat', sep=',', header=1), # Digitized
        'mit_cc0_ttf' : pd.read_csv(data_dir + 'exp_MIT_spinSusceptibility.dat', sep=',', header=1), # Digitized
        'ens_ee0_ttf' : pd.read_csv(data_dir + 'exp_ENS_energy.dat', sep=',', header=1), # Digitized

        'dhmc_drut_energy' : pd.read_csv(data_dir + 'dhmc_drut_energy.txt', sep=',', header=1), # Digititzed
        'pimc_cc0_tff' : pd.read_csv(data_dir + 'pimc_wlazlowski_spinSusceptibility.dat', sep=',', header=1), # Digitized
        'afqmc_cc0_tff' : pd.read_csv(data_dir + 'afqmc_jensen_spinSusceptibility.dat', sep=',', header=1), # Digitized
        'afqmc_cvn_ttf' : pd.read_csv(data_dir + 'afqmc_jensen_cv80.dat', sep=',', header=4), # Jensen
        'afqmc_eefg_ttf' : pd.read_csv(data_dir + 'afqmc_jensen_energy66.dat', sep=',', header=0), # Digitized
        

        'tmatrix_pantel_kk0_ttf' : pd.read_csv(data_dir + 'tmatrix_pantel_compressibility.dat', sep=',', header=1), # Digitized
        'tmatrix_pantel_cc0_ttf' : pd.read_csv(data_dir + 'tmatrix_pantel_spinSusceptibility.dat', sep=',', header=1), # Digitized
        'tmatrix_palestini_cc0_ttf' : pd.read_csv(data_dir + 'tmatrix_palestini_spinSusceptibility.dat', sep=',', header=1), # Digitized
        'etma_kashimura_cc0_ttf' : pd.read_csv(data_dir + 'etma_kashimura_compressibility.dat', sep=',', header=1), # Digitized

    }

    compare['mit_nn0_bmu'] = compare['mit_nn0_bmu'].fillna(0)
    compare['mit_transition'] = compare['mit_transition'].fillna(0)


    # Style for those comparisons.
    cstyle = {
     'mit' : {'m' : 'o', 'c' : '#a42604', 'fc' : '#f94515'},
     'ens' : {'m' : 'o', 'c' : '#5FAD41', 'fc' : '#adda9c'},

     'dhmc' : {'m' : 'd', 'c' : '#FA9F42', 'fc' : '#fbb874'},
     'bdmc' : {'m' : 'd', 'c' : '#0d153a', 'fc' : '#20338d'},

     'tma_1' : {'m' : '>', 'c' : '#0d153a', 'fc' : '', 'ls':'-'},
     'tma_2' : {'m' : 'v', 'c' : '#0d153a', 'fc' : '', 'ls':'-'},
     'etma' : {'m' : '<', 'c' : '#0d153a', 'fc' : '', 'ls':'-'},
     'lw' : {'m' : '^', 'c' : '#5FAD41', 'fc' : '#adda9c', 'ls':''},

     've' : {'m' : '', 'c' : '#114B5F', 'fc' : '', 'ls':'--'},
    }

    return compare, cstyle
