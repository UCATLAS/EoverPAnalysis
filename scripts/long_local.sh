#!/bin/bash

# Test on a Pythia JZ0 file
xAH_run.py \
    --config src/EoverPAnalysis/scripts/xAH_EoverP.py \
    --files user.luadamek:user.luadamek.mc16_13TeV.361020.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ0W.deriv.DAOD_EOP.e3569_s3170_r10572.240319_calibhitinfo_EXT0/ \
    --inputRucio \
    --submitDir long_local_test/ \
    -f \
    --nevents 50000 \
    direct
