#!/bin/zsh

baselines=("challenge-aido_LF-baseline-IL-logs-tensorflow"  \
    "challenge-aido_LF-baseline-IL-sim-tensorflow" \
    "challenge-aido_LF-baseline-RL-sim-pytorch"\
    "challenge-aido_LF-baseline-duckietown"\
    "challenge-aido_LF-minimal-agent"\
    "challenge-aido_LF-minimal-agent-full"\
       "challenge-aido_LF-template-pytorch" \
    "challenge-aido_LF-template-random"\
    "challenge-aido_LF-template-ros"\
    "challenge-aido_LF-template-tensorflow" \
    "challenge-aido_LF-baseline-JBR")


for a in ${baselines}; do
    D=${DT_ENV_DEVELOPER}/aido/${a}
    d=${D}/.circleci
    mkdir -p $d
    cp templates/baselines/config.yml $d/config.yml
    git -C ${D} add .circleci

done
