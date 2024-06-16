combine -M AsymptoticLimits --run blind datacard.txt
text2workspace.py datacard.txt
combine datacard.root -M MultiDimFit -t -1 --algo grid --points 100 --setParameterRanges r=0.0,10.0
