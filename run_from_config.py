#!/usr/bin/env python3
import argparse, subprocess, sys, yaml
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())

    outdir = Path(cfg["paths"]["outdir"]); outdir.mkdir(parents=True, exist_ok=True)
    cosmo = cfg["cosmology"]; bounce = cfg["bounce"]; power = cfg["power"]; halo = cfg["halo"]; uvlf = cfg["uvlf"]

    karg = []
    if power.get("kcut_override") is not None:
        karg = ["--kcut", str(power["kcut_override"])]

    subprocess.run([sys.executable, "clump_sfv_rework.py",
                    "--v", str(bounce["v"]), "--vphi", str(bounce["vphi"]),
                    "--ns", str(cosmo["ns"]), "--sigma8", str(cosmo["sigma8"]),
                    "--Omega_m0", str(cosmo["Omega_m0"]), "--Omega_b0", str(cosmo["Omega_b0"]), "--h", str(cosmo["h"]),
                    *karg,
                    "--outfile_csv", str(outdir/"power_spectrum_sfv.csv"),
                    "--outfile_png", str(outdir/"power_spectrum_sfv.png")],
                   check=True)

    z_args = [str(z) for z in halo["z"]]
    subprocess.run([sys.executable, "halo_from_power_ST.py",
                    "--power_csv", str(outdir/"power_spectrum_sfv.csv"),
                    "--z", *z_args,
                    "--mmin", str(halo["mmin"]), "--mmax", str(halo["mmax"]), "--nm", str(halo["nm"]),
                    "--outdir", str(outdir)], check=True)

    if uvlf.get("schechter_csv"):
        subprocess.run([sys.executable, "abmatch_uvlf_from_power.py",
                        "--power_csv", str(outdir/"power_spectrum_sfv.csv"),
                        "--z", str(halo["z"][0]), "--schechter", str(uvlf["schechter_csv"]),
                        "--outdir", str(outdir)], check=True)
    else:
        subprocess.run([sys.executable, "abmatch_uvlf_from_power.py",
                        "--power_csv", str(outdir/"power_spectrum_sfv.csv"),
                        "--z", str(halo["z"][0]),
                        "--Mstar", str(uvlf["Mstar"]), "--phistar", str(uvlf["phistar"]), "--alpha", str(uvlf["alpha"]),
                        "--outdir", str(outdir)], check=True)

if __name__ == "__main__":
    main()
