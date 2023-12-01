# with open('2023may23_flatGGpuUnc_lepFixed_full_combined_tuh.txt','r') as f_tuh:
#     l_tuh = f_tuh.readlines()
# f_tuh.close()
# print("loaded tuh datacard")

# with open('2023may23_flatGGpuUnc_lepFixed_full_combined_tch.txt','r') as f_tch:
#     l_tch = f_tch.readlines()
# f_tch.close()
# print("loaded tch datacard")

# f_tuh_out = open('edited_2023may23_flatGGpuUnc_lepFixedCorr_full_combined_tuh.txt', 'w')
# f_tch_out = open('edited_2023may23_flatGGpuUnc_lepFixedCorr_full_combined_tch.txt', 'w')

with open('2023sep6_full_combined_tuh.txt','r') as f_tuh:
    l_tuh = f_tuh.readlines()
f_tuh.close()
print("loaded tuh datacard")

with open('2023sep6_full_combined_tch.txt','r') as f_tch:
    l_tch = f_tch.readlines()
f_tch.close()
print("loaded tch datacard")

f_tuh_out = open('edited_2023sep6_full_combined_tuh.txt', 'w')
f_tch_out = open('edited_2023sep6_full_combined_tch.txt', 'w')

correlations = {
    "lumi_13TeV_Uncorrelated_2016" : "CMS_lumi_uncorr_2016",
    "lumi_13TeV_Uncorrelated_2017" : "CMS_lumi_uncorr_2017",
    "lumi_13TeV_Uncorrelated_2018" : "CMS_lumi_uncorr_2018",
    "lumi_uncorr_16" : "CMS_lumi_uncorr_2016",
    "lumi_uncorr_17" : "CMS_lumi_uncorr_2017",
    "lumi_uncorr_18" : "CMS_lumi_uncorr_2018",
    "lumi_corr_161718" : "CMS_lumi_corr_161718",
    "lumi_corr_1718" : "CMS_lumi_corr_1718",
    "PU" : "CMS_pu",
    # "jes_16" : "CMS_scale_j_2016",
    # "jes_17" : "CMS_scale_j_2017",
    # "jes_18" : "CMS_scale_j_2018",
    "CMS_scale_j_2016" : "CMS_scale_j",
    "CMS_scale_j_2017" : "CMS_scale_j",
    "CMS_scale_j_2018" : "CMS_scale_j",
    "jes" : "CMS_scale_j",
    # "pdfShp" : "CMS_pdf",
    "scShp" : "CMS_scale",
    "sigTh_tt" : "norm_fcnc",
    "sigTh_st" : "norm_fcnc",
    # "CMS_2016_jec" : "CMS_scale_j_2016",
    "CMS_2016_jec" : "CMS_scale_j",
    "CMS_2016_jer" : "CMS_res_j_2016",
    "CMS_2017_jer" : "CMS_res_j_2017",
    "CMS_2018_jer" : "CMS_res_j_2018",
    "_all_shapes.root" : "_all_shapes_EDITED.root",
    "CMS_hgg_ElectronIDWeight_2016" : "CMS_lepton",
    "CMS_hgg_ElectronIDWeight_2017" : "CMS_lepton",
    "CMS_hgg_ElectronIDWeight_2018" : "CMS_lepton",
    "CMS_hgg_ElectronRecoWeight_2016" : "CMS_lepton",
    "CMS_hgg_ElectronRecoWeight_2017" : "CMS_lepton",
    "CMS_hgg_ElectronRecoWeight_2018" : "CMS_lepton",
    "CMS_hgg_MuonIDWeight_2016" : "CMS_lepton",
    "CMS_hgg_MuonIDWeight_2017" : "CMS_lepton",
    "CMS_hgg_MuonIDWeight_2018" : "CMS_lepton",
    "CMS_hgg_MuonIsoWeight_2016" : "CMS_lepton",
    "CMS_hgg_MuonIsoWeight_2017" : "CMS_lepton",
    "CMS_hgg_MuonIsoWeight_2018" : "CMS_lepton",
    # "EleSF_16" : "CMS_lepton",
    # "EleSF_17" : "CMS_lepton",
    # "EleSF_18" : "CMS_lepton",
    # "MuSF_16" : "CMS_lepton",
    # "MuSF_17" : "CMS_lepton",
    # "MuSF_18" : "CMS_lepton",
    "EleSF" : "CMS_lepton",
    "MuSF" : "CMS_lepton",
}

for r_tuh in l_tuh:
    containsKey = False
    for key in correlations:
        if r_tuh.find(key) != -1 and r_tuh.find(correlations[key])==-1:
            containsKey = True
    # if containsKey: print(containsKey, r_tuh)
    if containsKey == False:
        f_tuh_out.write(r_tuh)
    else:
        r_tuh_new = ""
        for key in correlations:
            if r_tuh.find(key) != -1:
                # print(key)
                if "sigTh_" in key:
                    oldString = key
                    newString = correlations[key]+"_hut_"+key[-2:]
                    # print(oldString, newString)
                    if len(oldString)>len(newString):
                        spacestoadd = len(oldString)-len(newString)
                        newString = newString + (" "*spacestoadd)
                    if len(newString)>len(oldString):
                        spacestoadd = len(newString)-len(oldString)
                        oldString = oldString + (" "*spacestoadd)
                    r_tuh_new = r_tuh
                    r_tuh_new = r_tuh_new.replace(oldString,newString)
                elif ".root" in key:
                    oldString = key
                    newString = correlations[key]
                    r_tuh_new = r_tuh
                    r_tuh_new = r_tuh_new.replace(oldString,newString)
                else:
                    oldString = key
                    newString = correlations[key]
                    # print(oldString, newString)
                    if len(oldString)>len(newString):
                        spacestoadd = len(oldString)-len(newString)
                        newString = newString + (" "*spacestoadd)
                    if len(newString)>len(oldString):
                        spacestoadd = len(newString)-len(oldString)
                        oldString = oldString + (" "*spacestoadd)
                    r_tuh_new = r_tuh
                    r_tuh_new = r_tuh_new.replace(oldString,newString)
        # print(r_tuh_new)
        f_tuh_out.write(r_tuh_new)

for r_tch in l_tch:
    containsKey = False
    for key in correlations:
        if r_tch.find(key) != -1 and r_tch.find(correlations[key])==-1:
            containsKey = True
    if containsKey == False:
        f_tch_out.write(r_tch)
    else:
        r_tch_new = ""
        for key in correlations:
            if r_tch.find(key) != -1:
                if "sigTh_" in key:
                    oldString = key
                    newString = correlations[key]+"_hct_"+key[-2:]
                    if len(oldString)>len(newString):
                        spacestoadd = len(oldString)-len(newString)
                        newString = newString + (" "*spacestoadd)
                    if len(newString)>len(oldString):
                        spacestoadd = len(newString)-len(oldString)
                        oldString = oldString + (" "*spacestoadd)
                    r_tch_new = r_tch
                    r_tch_new = r_tch_new.replace(oldString,newString)
                elif ".root" in key:
                    oldString = key
                    newString = correlations[key]
                    r_tch_new = r_tch
                    r_tch_new = r_tch_new.replace(oldString,newString)
                else:
                    oldString = key
                    newString = correlations[key]
                    if len(oldString)>len(newString):
                        spacestoadd = len(oldString)-len(newString)
                        newString = newString + (" "*spacestoadd)
                    if len(newString)>len(oldString):
                        spacestoadd = len(newString)-len(oldString)
                        oldString = oldString + (" "*spacestoadd)
                    r_tch_new = r_tch
                    r_tch_new = r_tch_new.replace(oldString,newString)
        f_tch_out.write(r_tch_new)

