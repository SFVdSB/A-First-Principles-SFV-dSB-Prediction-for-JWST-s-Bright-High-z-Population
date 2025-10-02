# Simple automation. Reads optional .env (exported as shell vars).
-include .env
SHELL := /bin/bash

PY ?= python
OUT ?= $(OUTDIR)
OUTDIR ?= outputs
CONFIG ?= configs/default.yaml

default: all

venv:
	python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

power:
	mkdir -p $(OUTDIR)
	$(PY) clump_sfv_rework.py \
		--v $${V_DEFAULT:-4.2e-05} --vphi $${VPHI_DEFAULT:-9.0e-05} \
		${KCUT:+--kcut $(KCUT)} \
		--outfile_csv $(OUTDIR)/power_spectrum_sfv.csv \
		--outfile_png $(OUTDIR)/power_spectrum_sfv.png

halos: power
	$(PY) halo_from_power_ST.py \
		--power_csv $(OUTDIR)/power_spectrum_sfv.csv \
		--z 15 10 \
		--outdir $(OUTDIR)

uvlf: power
	$(PY) abmatch_uvlf_from_power.py \
		--power_csv $(OUTDIR)/power_spectrum_sfv.csv \
		--z 10 \
		--Mstar -20.9 --phistar 1e-4 --alpha -2.1 \
		--outdir $(OUTDIR)

background:
	mkdir -p $(OUTDIR)
	$(PY) make_all_sfv_plots_from_background.py \
		--background_csv $${BACKGROUND_CSV:-background_profile.csv} \
		--bounce $${BOUNCE_DRIVER:-2-field_BounceDetails_v4f_v2.py} \
		--gamma_k $${GAMMA_K:-0.595} \
		--z 15 10 \
		--outdir $(OUTDIR)

all: background uvlf

clean:
	rm -rf $(OUTDIR) *.egg-info __pycache__ .pytest_cache

.PHONY: default venv power halos uvlf background all clean
