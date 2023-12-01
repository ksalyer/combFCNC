# combFCNC
## make cards for combination
you need to be in the cms environment required by the combine tool, CMSSW_10_2_9
then run
combineCards.py dc_hbb=[HtobbAnalysisCard] dc_hgg=[HtoggAnalysisCard] dc_hleptonic=[HtoSSAnalysis] > fullCombinedCard.txt
for both signals, tch and tuh

editDatacards.py controls the correlation scheme for the combination
edit the input/output card names at the beginning of editDatatcards.py and run it to produce cards that can be run for the combination

## running the combination
run combine on the edited cards with
combine -M AsymptoticLimits -m 125.380000 [nameOfEditedCard.txt] --freezeParameters MH > [nameOfOutputFileToSaveResults]

and the results can be multiplied by 0.1441 to convert to a BR percentage (signal yield has been scaled down by factor of 100)

## making the combination plot
the combination plot can be made with the multiplechannelsPlot.py script. results can be edited inside the script starting at line 27.
