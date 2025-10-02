# SFV/dSB Bounce → Power → Halos → UVLF (JWST)  

This repository contains a **first-principles** pipeline that maps **two‑field bounce** parameters in the **SFV/dSB** model to:
1) a modified linear **matter power spectrum**,
2) high‑z **halo abundances** (Sheth–Tormen), and
3) a predicted **UV luminosity function** via **abundance matching**.

It directly anchors the enhancement to large‑scale power in terms of bounce outputs:
- amplitude **A_sfv = (v_phi / v)^4**,
- scale placement **k_cut = γ_k / R0** with **R0** (and optional effective wall width **w_eff**) read from the background profile.

> For an overview and figures, see the paper draft in this repo: `A_First_Principles_SFV_dSB_Prediction_for_JWST_s_Bright_High_z_Population.pdf`.

---

## Repository layout

```
.
├── clump_sfv_rework.py                  # power spectrum from bounce params
├── halo_from_power_ST.py                # halo mass function + plots
├── abmatch_uvlf_from_power.py           # abundance matching to UVLF
├── extract_bounce_defaults.py           # parse v, vphi, R0, w from bounce driver
├── make_all_sfv_plots.py                # convenience pipeline
├── make_all_sfv_plots_from_background.py# pipeline anchored to background_profile.csv (R0→k_cut)
├── configs/
│   └── default.yaml                     # central config (cosmology, bounce, halo, UVLF)
├── .env.example                         # environment variables (paths/overrides)
├── requirements.txt / environment.yml   # Python environment
├── Makefile                             # common tasks (power, halos, uvlf, all)
├── .github/workflows/ci.yml             # lint + smoke run
├── .editorconfig, .ruff.toml, .gitignore
├── KEYWORDS.md                          # searchable keywords for this repo
└── A_First_Principles_SFV_dSB_Prediction_for_JWST_s_Bright_High_z_Population.pdf
```

---

## Quick start

### 1) Create Python env
```bash
# Using pip
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Or conda
conda env create -f environment.yml
conda activate sfv-dsb
```

### 2) Put your bounce outputs in place
- Bounce driver (used to read `v`, `vphi`, optionally `R0`, `w`): `2-field_BounceDetails_v4f_v2.py`
- Background profile CSV from your run: `background_profile.csv`

Place them anywhere and point to them via `.env` or CLI flags below.

### 3) One‑shot (background‑anchored) run
```bash
python make_all_sfv_plots_from_background.py   --background_csv background_profile.csv   --bounce 2-field_BounceDetails_v4f_v2.py   --gamma_k 0.595   --z 15 10   --outdir ./outputs
```

### 4) Step‑by‑step (manual)
```bash
# Power spectrum (amplitude from vphi/v; k_cut override optional)
python clump_sfv_rework.py --v 4.2e-05 --vphi 9.0e-05   --kcut 0.11898   --outfile_csv outputs/power_spectrum_sfv.csv   --outfile_png outputs/power_spectrum_sfv.png

# Halos (Sheth–Tormen) at chosen redshifts
python halo_from_power_ST.py --power_csv outputs/power_spectrum_sfv.csv   --z 15 10 --outdir outputs

# (Optional) UVLF abundance matching at z=10
python abmatch_uvlf_from_power.py --power_csv outputs/power_spectrum_sfv.csv   --z 10 --Mstar -20.9 --phistar 1e-4 --alpha -2.1 --outdir outputs
```

> See `to run.txt` for the exact commands we used during development.

---

## Configuration

### Option A — YAML
Edit **`configs/default.yaml`** (example below), then run:
```bash
python run_from_config.py --config configs/default.yaml
```

### Option B — Environment (.env)
Copy **`.env.example`** to `.env` and adjust paths/values. The `Makefile` reads these.

---

## Outputs
- **power_spectrum_sfv.csv/png** — ΛCDM baseline, SFV contribution, and total P(k)
- **cumulative_halo_abundance.png** — n(>M) vs M at requested z
- **abundance_ratio.png** — SFV/ΛCDM cumulative abundance ratio
- **halo_abundance_SFV_vs_LCDM.csv** — table of dn/dM, n(>M), ratios
- **uvlf_pred_* / uvlf_*_ratio.png** — optional UVLF predictions via abundance matching
- **wall_estimate_from_background.png** — diagnostic R0, w_eff estimate from profile

---

## Reproducibility
- The paper draft and all figures were generated with the scripts in this repository.
- Scripts are pure Python with NumPy/Pandas/SciPy/Matplotlib; no external cosmology packages required.

---

## Citing / provenance
If you use this code or figures, please cite the repo and the included draft. Also cite the original methods used for transfer functions & halo mass functions (see the draft’s bibliography).

---

## Support
Open an issue with a description, error log, your `configs/default.yaml` (sanitized), and environment info (`pip freeze`).
