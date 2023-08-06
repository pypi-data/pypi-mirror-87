# test on compton module
import pytest
import numpy as np
import astropy.units as u
from astropy.constants import h, m_e, c, M_sun
from astropy.coordinates import Distance
from pathlib import Path
from agnpy.emission_regions import Blob
from agnpy.synchrotron import Synchrotron
from agnpy.targets import PointSourceBehindJet, SSDisk, SphericalShellBLR, RingDustTorus
from agnpy.compton import SynchrotronSelfCompton, ExternalCompton
from .utils import make_comparison_plot, extract_columns_sample_file, check_deviation
from agnpy.utils.math import trapz_loglog


agnpy_dir = Path(__file__).parent.parent
# where to read sampled files
data_dir = agnpy_dir / "data"
# where to save figures
figures_dir = agnpy_dir.parent / "crosschecks/figures/compton"
figures_dir.mkdir(parents=True, exist_ok=True)

# variables with _test are global and meant to be used in all tests
pwl_spectrum_norm_test = 1e48 * u.Unit("erg")
pwl_dict_test = {
    "type": "PowerLaw",
    "parameters": {"p": 2.8, "gamma_min": 1e2, "gamma_max": 1e5},
}
bpwl_spectrum_norm_test = 6e42 * u.Unit("erg")
bpwl_dict_test = {
    "type": "BrokenPowerLaw",
    "parameters": {
        "p1": 2.0,
        "p2": 3.5,
        "gamma_b": 1e4,
        "gamma_min": 20,
        "gamma_max": 5e7,
    },
}
# blob reproducing Figure 7.4 of Dermer Menon 2009
pwl_blob_test = Blob(
    1e16 * u.cm,
    Distance(1e27, unit=u.cm).z,
    10,
    10,
    1 * u.G,
    pwl_spectrum_norm_test,
    pwl_dict_test,
)
# blob reproducing the EC scenarios in Finke 2016
bpwl_blob_test = Blob(
    1e16 * u.cm, 1, 40, 40, 0.56 * u.G, bpwl_spectrum_norm_test, bpwl_dict_test,
)
bpwl_blob_test.set_gamma_size(350)
# global disk
M_BH = 1.2 * 1e9 * M_sun.cgs
L_disk = 2e46 * u.Unit("erg s-1")
eta = 1 / 12
R_in = 6
R_out = 200
disk_test = SSDisk(M_BH, L_disk, eta, R_in, R_out, R_g_units=True)
# global blr
xi_line = 0.024
R_line = 1e17 * u.cm
blr_test = SphericalShellBLR(L_disk, xi_line, "Lyalpha", R_line)
# global dt
T_dt = 1e3 * u.K
csi_dt = 0.1
dt_test = RingDustTorus(L_disk, csi_dt, T_dt)


class TestSynchrotronSelfCompton:
    """class grouping all tests related to the Synchrotron Slef Compton class"""

    def test_ssc_reference_sed(self):
        """test agnpy SSC SED against the one in Figure 7.4 of Dermer Menon"""
        # reference SED
        nu_ref, sed_ref = extract_columns_sample_file(
            f"{data_dir}/sampled_seds/ssc_figure_7_4_dermer_menon_2009.txt",
            "Hz",
            "erg cm-2 s-1",
        )
        # recompute the SED at the same ordinates where the figure was sampled
        ssc = SynchrotronSelfCompton(pwl_blob_test)
        sed_agnpy = ssc.sed_flux(nu_ref)
        # sed comparison plot
        make_comparison_plot(
            nu_ref,
            sed_ref,
            sed_agnpy,
            "Figure 7.4, Dermer and Menon (2009)",
            "agnpy",
            "Synchrotron Self Compton",
            f"{figures_dir}/ssc_comparison_figure_7_4_dermer_menon_2009.png",
            "sed",
        )
        # requires that the SED points deviate less than 15% from the figure
        assert check_deviation(nu_ref, sed_ref, sed_agnpy, 0, 0.15)

    def test_ssc_integration_methods(self):
        """test SSC SED for different integration methods against each other
        """
        nu = np.logspace(15, 28) * u.Hz
        ssc_trapz = SynchrotronSelfCompton(pwl_blob_test, integrator=np.trapz)
        ssc_trapz_loglog = SynchrotronSelfCompton(
            pwl_blob_test, integrator=trapz_loglog
        )
        sed_ssc_trapz = ssc_trapz.sed_flux(nu)
        sed_ssc_trapz_loglog = ssc_trapz_loglog.sed_flux(nu)
        # check in a restricted frequency range
        nu_range = [1e15, 1e26] * u.Hz
        make_comparison_plot(
            nu,
            sed_ssc_trapz,
            sed_ssc_trapz_loglog,
            "trapezoidal integration",
            "trapezoidal log-log integration",
            "Synchrotron Self Compton",
            f"{figures_dir}/ssc_comparison_integration_methods.png",
            "sed",
            comparison_range=nu_range.to_value("Hz"),
        )
        # requires that the SED points deviate less than 20%
        assert check_deviation(
            nu, sed_ssc_trapz, sed_ssc_trapz_loglog, 0, 0.2, nu_range
        )


class TestExternalCompton:
    """class grouping all tests related to the Synchrotron Slef Compton class"""

    # tests for EC on SSDisk
    def test_ec_disk_reference_sed(self):
        """test agnpy SED for EC on Disk against the one in Figure 8 of Finke 2016"""
        # reference SED
        nu_ref, sed_ref = extract_columns_sample_file(
            f"{data_dir}/sampled_seds/ec_disk_figure_8_finke_2016.txt",
            "Hz",
            "erg cm-2 s-1",
        )
        # recompute the SED at the same ordinates where the figure was sampled
        r = 1e17 * u.cm
        ec_disk = ExternalCompton(bpwl_blob_test, disk_test, r)
        sed_agnpy = ec_disk.sed_flux(nu_ref)
        # check in a restricted energy range
        nu_range = [1e18, 1e28] * u.Hz
        make_comparison_plot(
            nu_ref,
            sed_ref,
            sed_agnpy,
            "Figure 8, Finke (2016)",
            "agnpy",
            "External Compton on Shakura Sunyaev Disk",
            f"{figures_dir}/ec_disk_comparison_figure_8_finke_2016.png",
            "sed",
            comparison_range=nu_range.to_value("Hz"),
        )
        # requires that the SED points deviate less than 30% from the figure
        assert check_deviation(nu_ref, sed_ref, sed_agnpy, 0, 0.3, nu_range)

    def test_ec_disk_integration_methods(self):
        """test EC on Disk SED for different integration methods against each other
        """
        nu = np.logspace(15, 28) * u.Hz
        r = 1e18 * u.cm
        ec_disk_trapz = ExternalCompton(
            bpwl_blob_test, disk_test, r, integrator=np.trapz
        )
        ec_disk_trapz_loglog = ExternalCompton(
            bpwl_blob_test, disk_test, r, integrator=trapz_loglog
        )
        sed_ec_disk_trapz = ec_disk_trapz.sed_flux(nu)
        sed_ec_disk_trapz_loglog = ec_disk_trapz_loglog.sed_flux(nu)
        make_comparison_plot(
            nu,
            sed_ec_disk_trapz,
            sed_ec_disk_trapz_loglog,
            "trapezoidal integration",
            "trapezoidal log-log integration",
            "External Compton on Shakura Sunyaev Disk",
            f"{figures_dir}/ec_disk_comparison_integration_methods.png",
            "sed",
        )
        # requires that the SED points deviate less than 20%
        assert check_deviation(nu, sed_ec_disk_trapz, sed_ec_disk_trapz_loglog, 0, 0.2)

    # tests for EC on BLR
    def test_ec_blr_reference_sed(self):
        """test agnpy SED for EC on BLR against the one in Figure 10 of Finke 2016"""
        # reference SED
        nu_ref, sed_ref = extract_columns_sample_file(
            f"{data_dir}/sampled_seds/ec_blr_figure_10_finke_2016.txt",
            "Hz",
            "erg cm-2 s-1",
        )
        # recompute the SED at the same ordinates where the figure was sampled
        r = 1e18 * u.cm
        ec_blr = ExternalCompton(bpwl_blob_test, blr_test, r)
        sed_agnpy = ec_blr.sed_flux(nu_ref)
        # sed comparison plot
        make_comparison_plot(
            nu_ref,
            sed_ref,
            sed_agnpy,
            "Figure 10, Finke (2016)",
            "agnpy",
            "External Compton on Spherical Shell Broad Line Region",
            f"{figures_dir}/ec_blr_comparison_figure_10_finke_2016.png",
            "sed",
        )
        # requires that the SED points deviate less than 30% from the figure
        assert check_deviation(nu_ref, sed_ref, sed_agnpy, 0, 0.3)

    def test_ec_blr_integration_methods(self):
        """test EC on BLR SED for different integration methods
        """
        nu = np.logspace(15, 28) * u.Hz
        r = 1e18 * u.cm
        ec_blr_trapz = ExternalCompton(bpwl_blob_test, blr_test, r, integrator=np.trapz)
        ec_blr_trapz_loglog = ExternalCompton(
            bpwl_blob_test, blr_test, r, integrator=trapz_loglog
        )
        sed_ec_blr_trapz = ec_blr_trapz.sed_flux(nu)
        sed_ec_blr_trapz_loglog = ec_blr_trapz_loglog.sed_flux(nu)
        # check in a restricted energy range
        nu_range = [1e15, 1e27] * u.Hz
        make_comparison_plot(
            nu,
            sed_ec_blr_trapz,
            sed_ec_blr_trapz_loglog,
            "trapezoidal integration",
            "trapezoidal log-log integration",
            "External Compton on Spherical Shell Broad Line Region",
            f"{figures_dir}/ec_blr_comparison_integration_methods.png",
            "sed",
            comparison_range=nu_range.to_value("Hz"),
        )
        # requires that the SED points deviate less than 30%
        assert check_deviation(
            nu, sed_ec_blr_trapz, sed_ec_blr_trapz_loglog, 0, 0.3, nu_range
        )

    # tests for EC on DT
    def test_ec_dt_reference_sed(self):
        """test agnpy SED for EC on DT against the one in Figure 11 of Finke 2016"""
        # reference SED
        nu_ref, sed_ref = extract_columns_sample_file(
            f"{data_dir}/sampled_seds/ec_dt_figure_11_finke_2016.txt",
            "Hz",
            "erg cm-2 s-1",
        )
        # correct miscalculation of the DT emissivity in Finke 2016
        sed_ref *= 2
        r = 1e20 * u.cm
        ec_dt = ExternalCompton(bpwl_blob_test, dt_test, r)
        sed_agnpy = ec_dt.sed_flux(nu_ref)
        # sed comparison plot
        make_comparison_plot(
            nu_ref,
            sed_ref,
            sed_agnpy,
            "Figure 11, Finke (2016)",
            "agnpy",
            "External Compton on Ring Dust Torus",
            f"{figures_dir}/ec_dt_comparison_figure_11_finke_2016.png",
            "sed",
        )
        # requires that the SED points deviate less than 30% from the figure
        assert check_deviation(nu_ref, sed_ref, sed_agnpy, 0, 0.3)

    def test_ec_dt_integration_methods(self):
        """test EC on DT SED for different integration methods
        """
        nu = np.logspace(15, 28) * u.Hz
        r = 1e20 * u.cm
        ec_dt_trapz = ExternalCompton(bpwl_blob_test, dt_test, r, integrator=np.trapz)
        ec_dt_trapz_loglog = ExternalCompton(
            bpwl_blob_test, dt_test, r, integrator=trapz_loglog
        )
        sed_ec_dt_trapz = ec_dt_trapz.sed_flux(nu)
        sed_ec_dt_trapz_loglog = ec_dt_trapz_loglog.sed_flux(nu)
        make_comparison_plot(
            nu,
            sed_ec_dt_trapz,
            sed_ec_dt_trapz_loglog,
            "trapezoidal integration",
            "trapezoidal log-log integration",
            "External Compton on Ring Dust Torus",
            f"{figures_dir}/ec_dt_comparison_integration_methods.png",
            "sed",
        )
        # requires that the SED points deviate less than 20%
        assert check_deviation(nu, sed_ec_dt_trapz, sed_ec_dt_trapz_loglog, 0, 0.2)

    # tests against point-like sources approximating the targets
    def test_ec_blr_vs_point_source(self):
        """check if in the limit of large distances the EC on the BLR tends to
        the one of a point-like source approximating it"""
        r = 1e22 * u.cm
        # point like source approximating the blr
        ps_blr = PointSourceBehindJet(
            blr_test.xi_line * blr_test.L_disk, blr_test.epsilon_line
        )
        # external Compton
        ec_blr = ExternalCompton(bpwl_blob_test, blr_test, r)
        ec_ps_blr = ExternalCompton(bpwl_blob_test, ps_blr, r)
        # seds
        nu = np.logspace(15, 30) * u.Hz
        sed_ec_blr = ec_blr.sed_flux(nu)
        sed_ec_ps_blr = ec_ps_blr.sed_flux(nu)
        # sed comparison plot
        make_comparison_plot(
            nu,
            sed_ec_blr,
            sed_ec_ps_blr,
            "spherical shell BLR",
            "point source approximating the BLR",
            "External Compton on Spherical Shell BLR, "
            + r"$r = 10^{22}\,{\rm cm} \gg R_{\rm line}$",
            f"{figures_dir}/ec_blr_point_source_comparison.png",
            "sed",
        )
        # requires a 20% deviation from the two SED points
        assert check_deviation(nu, sed_ec_blr, sed_ec_ps_blr, 0, 0.2)

    def test_ec_dt_vs_point_source(self):
        """check if in the limit of large distances the EC on the DT tends to
        the one of a point-like source approximating it"""
        r = 1e22 * u.cm
        # point like source approximating the dt
        ps_dt = PointSourceBehindJet(dt_test.xi_dt * dt_test.L_disk, dt_test.epsilon_dt)
        # external Compton
        ec_dt = ExternalCompton(bpwl_blob_test, dt_test, r)
        ec_ps_dt = ExternalCompton(bpwl_blob_test, ps_dt, r)
        # seds
        nu = np.logspace(15, 28) * u.Hz
        sed_ec_dt = ec_dt.sed_flux(nu)
        sed_ec_ps_dt = ec_ps_dt.sed_flux(nu)
        make_comparison_plot(
            nu,
            sed_ec_dt,
            sed_ec_ps_dt,
            "ring dust torus",
            "point source approximating the DT",
            "External Compton on Ring Dust Torus, "
            + r"$r = 10^{22}\,{\rm cm} \gg R_{\rm dt}$",
            f"{figures_dir}/ec_dt_point_source_comparison.png",
            "sed",
        )
        # requires a 20% deviation from the two SED points
        assert check_deviation(nu, sed_ec_dt, sed_ec_ps_dt, 0, 0.2)
