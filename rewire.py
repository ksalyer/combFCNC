import os, sys
import re
import ROOT

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

txt_name = "Datacard_Hut.txt"
ws_name = "Datacard_fcnc_hutv5.11_25Apr2021_unblind_FCNC.root"

txt_out = "Datacard_fcnc_hutv5.11_25Apr2021_unblind_FCNC_rewired.txt"
ws_out = "Datacard_fcnc_hutv5.11_25Apr2021_unblind_FCNC_rewired.inputs.root"


fWS = ROOT.TFile.Open(ws_name)
w = fWS.Get("w")

txt = open(txt_name,"r")
out = open(txt_out,"w")
wout = ROOT.RooWorkspace("w2","w2")
def Import(w,o):
    getattr(w,'import')(o,ROOT.RooFit.RecycleConflictNodes())
    # print(getattr(w,'import'))
    # print(getattr(o,ROOT.RooFit.RecycleConflictNodes()))

data_obs=w.data("data_obs")
chan = w.obj("CMS_channel")
## build map chan -> index
chan_map={}
for i in range(0,chan.numTypes() ):
    chan.setIndex(i)
    chan_map[chan.getLabel()]=i

# I don't remember why I have to do this
data = ROOT.RooDataSet("data_obs_unbinned","",ROOT.RooArgSet(data_obs.get()));
for idat in range(0,data_obs.numEntries()):
    dset = data_obs.get(idat)
    nent = int(data_obs.weight())
    for ient in range(0,nent):
        data.add(dset);

## Get observable. Could be done generic, but it is not worth the effort since all of them use the same
x=w.var("CMS_hgg_mass")

#channels = []
for line in txt:
    l = re.sub('\n','',line)

    if re.match('shapes',l) and not re.search('data_obs',l):
        parts=l.split()
        proc = parts[1]
        chn = parts[2]
        f = parts[3]
        name = parts[4].split(":")[-1]
        #channels.append(chn)

        #'shapeBkg_ggh_2017_hgg_FCNCHadronicTag_0'
        done = False
        for s in ['Bkg','Sig']:
            pdf_name =  'shape'+s+"_"+proc + '_' + chn
            pdf = w.pdf(pdf_name)
            norm= w.function(pdf_name + "__norm")
            if pdf and norm and not done:
                done=True
                pdf.SetName(name)
                norm.SetName(name +"_norm")

                Import(wout,pdf)
                Import(wout,norm)
                l = '   '.join(['shapes',proc,chn,ws_out,wout.GetName()+':'+name])
        if not done:
            print "Unable to find proc for line:",l

    if re.match('shapes',l) and re.search('data_obs',l):
        parts=l.split()
        proc = parts[1]
        chn = parts[2]
        f = parts[3]
        name = parts[4].split(":")[-1]

        icat = chan_map[chn] if chn in chan_map else None

        catdata = data.reduce("CMS_channel==CMS_channel::%d"%icat);
        bc=ROOT.RooDataHist(name,name,ROOT.RooArgSet(x))
        for idat in range(0,catdata.numEntries()):
            dset = catdata.get(idat)
            nent = int(catdata.weight())
            for ient in range(0,nent):
                bc.add(dset);
        Import(wout,bc)
        l = '   '.join(['shapes',proc,chn,ws_out,wout.GetName()+':'+name])
    # else:
    #     print("not a shapes line: ", l)
    ##
    print >>out,l

wout.writeToFile(ws_out)
print " -- DONE --"
del wout
