############
##Baseline
############
	
# most frequent classifier
		python scripts/train.py  -m basemf  -o basemf_base_es -i "InterTASS/ES/intertass-ES-train-tagged.xml"
		python scripts/eval.py -i basemf_base_es -c "InterTASS/ES/intertass-ES-development-tagged.xml" -d "baseline most frequent"

		python scripts/train.py  -m basemf  -o basemf_base_cr -i "InterTASS/CR/intertass-CR-train-tagged.xml"
		python scripts/eval.py -i basemf_base_cr -c "InterTASS/CR/intertas	s-CR-development-tagged.xml" -d "baseline most frequent"

		python scripts/train.py  -m basemf  -o basemf_base_pe -i "InterTASS/PE/intertass-PE-train-tagged.xml"
		python scripts/eval.py -i basemf_base_pe -c "InterTASS/PE/intertass-PE-development-tagged.xml" -d "baseline most frequent"

# svn classifier 
		python scripts/train.py  -m clf -c maxent -o maxent_base_es -i "InterTASS/ES/intertass-ES-train-tagged.xml"
		python scripts/eval.py -i maxent_base_es -c "InterTASS/ES/intertass-ES-development-tagged.xml" -d "baseline maxent"

		python scripts/train.py  -m clf -c maxent -o maxent_base_cr -i "InterTASS/CR/intertass-CR-train-tagged.xml"
		python scripts/eval.py -i maxent_base_cr -c "InterTASS/CR/intertass-CR-development-tagged.xml" -d "baseline maxent"

		python scripts/train.py  -m clf  -o maxent_base_pe -i "InterTASS/PE/intertass-PE-train-tagged.xml"
		python scripts/eval.py -i maxent_base_pe -c "InterTASS/PE/intertass-PE-development-tagged.xml" -d "baseline maxent"
	
################
##NLTK Tokenizer
################

# svn classifier 
		python scripts/train.py  -m clf -c maxent -o maxent_nltktok_es -i "InterTASS/ES/intertass-ES-train-tagged.xml"
		python scripts/eval.py -i maxent_nltktok_es -c "InterTASS/ES/intertass-ES-development-tagged.xml" -d "maxent with nltk tokenizer"

		python scripts/train.py  -m clf -c maxent -o maxent_nltktok_cr -i "InterTASS/CR/intertass-CR-train-tagged.xml"
		python scripts/eval.py -i maxent_nltktok_cr -c "InterTASS/CR/intertass-CR-development-tagged.xml" -d "maxent with nltk tokenizer"

		python scripts/train.py  -m clf  -o maxent_nltktok_pe -i "InterTASS/PE/intertass-PE-train-tagged.xml"
		python scripts/eval.py -i maxent_nltktok_pe -c "InterTASS/PE/intertass-PE-development-tagged.xml" -d "maxent with nltk tokenizer"

##############
#Binary Counts
##############

#svn classifier 
		python scripts/train.py  -m clf -c maxent -o maxent_binary_es -i "InterTASS/ES/intertass-ES-train-tagged.xml"
		python scripts/eval.py -i maxent_binary_es -c "InterTASS/ES/intertass-ES-development-tagged.xml" -d "maxent binary count"

		python scripts/train.py  -m clf -c maxent -o maxent_binary_cr -i "InterTASS/CR/intertass-CR-train-tagged.xml"
		python scripts/eval.py -i maxent_binary_cr -c "InterTASS/CR/intertass-CR-development-tagged.xml" -d "maxent binary count"

		python scripts/train.py  -m clf  -o maxent_binary_pe -i "InterTASS/PE/intertass-PE-train-tagged.xml"
		python scripts/eval.py -i maxent_binary_pe -c "InterTASS/PE/intertass-PE-development-tagged.xml" -d "maxent binary count"

############
##Stop Words
############

# svn classifier 
		python scripts/train.py  -m clf -c maxent -o maxent_stop_es -i "InterTASS/ES/intertass-ES-train-tagged.xml"
		python scripts/eval.py -i maxent_stop_es -c "InterTASS/ES/intertass-ES-development-tagged.xml" -d "maxent stop words"

		python scripts/train.py  -m clf -c maxent -o maxent_stop_cr -i "InterTASS/CR/intertass-CR-train-tagged.xml"
		python scripts/eval.py -i maxent_stop_cr -c "InterTASS/CR/intertass-CR-development-tagged.xml" -d "maxent stop words"

		python scripts/train.py  -m clf  -o maxent_stop_pe -i "InterTASS/PE/intertass-PE-train-tagged.xml"
		python scripts/eval.py -i maxent_stop_pe -c "InterTASS/PE/intertass-PE-development-tagged.xml" -d "maxent stop words"


##############
#Normalization
##############

# svn classifier 
		python scripts/train.py  -m clf -c maxent -o maxent_norm_es -i "InterTASS/ES/intertass-ES-train-tagged.xml"
		python scripts/eval.py -i maxent_norm_es -c "InterTASS/ES/intertass-ES-development-tagged.xml" -d "maxent normalization"

		python scripts/train.py  -m clf -c maxent -o maxent_norm_cr -i "InterTASS/CR/intertass-CR-train-tagged.xml"
		python scripts/eval.py -i maxent_norm_cr -c "InterTASS/CR/intertass-CR-development-tagged.xml" -d "maxent normalization"

		python scripts/train.py  -m clf  -o maxent_norm_pe -i "InterTASS/PE/intertass-PE-train-tagged.xml"
		python scripts/eval.py -i maxent_norm_pe -c "InterTASS/PE/intertass-PE-development-tagged.xml" -d "maxent normalization"

#####
##ALL
#####

# svn classifier 
		python scripts/train.py  -m clf -c maxent -o maxent_all_es -i "InterTASS/ES/intertass-ES-train-tagged.xml"
		python scripts/eval.py -i maxent_all_es -c "InterTASS/ES/intertass-ES-development-tagged.xml" -d "maxent nltk-binary-stop-norm"

		python scripts/train.py  -m clf -c maxent -o maxent_all_cr -i "InterTASS/CR/intertass-CR-train-tagged.xml"
		python scripts/eval.py -i maxent_all_cr -c "InterTASS/CR/intertass-CR-development-tagged.xml" -d "maxent nltk-binary-stop-norm"

		python scripts/train.py  -m clf  -o maxent_all_pe -i "InterTASS/PE/intertass-PE-train-tagged.xml"
		python scripts/eval.py -i maxent_all_pe -c "InterTASS/PE/intertass-PE-development-tagged.xml" -d "maxent nltk-binary-stop-norm"
