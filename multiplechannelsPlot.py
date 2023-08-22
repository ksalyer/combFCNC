import ROOT
import os
import ctypes
import copy
import shutil
from functools                      import partial
from array                          import array

# from RotTools.core.standard        import *

# from TopEFT.Tools.user              import combineReleaseLocation, analysis_results, plot_directory


# Plot style
# ROOT.gROOT.LoadMacro('$CMSSW_BASE/src/TopEFT/Tools/scripts/tdrstyle.C')
# ROOT.setTDRStyle()

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument("--testGrayscale",   action='store_true',            help="Because of  reasons...")
argParser.add_argument("--preliminary",     action='store_true',            help="Because of  reasons...")
argParser.add_argument("--model",           action='store', default='EFT',  help="Use sigma levels?")
argParser.add_argument("--out",             action='store', default='/home/users/ksalyer/public_html/')
args = argParser.parse_args()

## define all the results
results = [\
    
    {   'name': 'hbb_tuh',
        'tex': 'H#rightarrow b#bar{b}',
        'limits': {'obs': [(0.079,0.079)], 'exp': [(0.11,0.11)], '1sigma': [(0.079, 0.153)], '2sigma': [(0.060, 0.204)]}
    },
    {   'name': 'hgg_tuh',
        'tex': 'H#rightarrow #gamma #gamma',
        'limits': {'obs': [(0.019,0.019)], 'exp': [(0.031,0.031)], '1sigma': [(0.021,0.045)], '2sigma': [(0.015,0.064)]}
    },
    {   'name': 'hss_tuh',
        'tex': 'leptonic',
        'limits': {'obs': [(0.073,0.073)], 'exp': [(0.059,0.059)], '1sigma': [(0.043, 0.083)], '2sigma': [(0.032, 0.11)]}
    },
    {   'name': 'comb_tuh',
        'tex': 'combined',
        'limits': {'obs': [(0.0188,0.0188)], 'exp': [(0.0283,0.0283)], '1sigma': [(0.02, 0.0403)], '2sigma': [(0.0147, 0.05497)]}
    },
    {   'name': 'hbb_tch',
        'tex': 'H#rightarrow b#bar{b}',
        'limits': {'obs': [(0.094,0.094)], 'exp': [(0.087,0.087)], '1sigma': [(0.063, 0.122)], '2sigma': [(0.047, 0.164)]}
    },
    {   'name': 'hgg_tch',
        'tex': 'H#rightarrow #gamma #gamma',
        'limits': {'obs': [(0.073,0.073)], 'exp': [(0.051,0.051)], '1sigma': [(0.036,0.072)], '2sigma': [(0.027,0.098)]}
    },
    {   'name': 'hss_tch',
        'tex': 'leptonic',
        'limits': {'obs': [(0.041,0.041)], 'exp': [(0.060,0.060)], '1sigma': [(0.042, 0.086)], '2sigma': [(0.031, 0.121)]}
    },
    {   'name': 'comb_tch',
        'tex': 'combined',
        'limits': {'obs': [(0.037,0.037)], 'exp': [(0.035,0.035)], '1sigma': [(0.0251, 0.0491)], '2sigma': [(0.0188, 0.0658)]}
    },
]

ordering = ['2sigma', '1sigma', 'obs', 'exp']
# ordering = ['2sigma', '1sigma']

res = results
ordering = ordering

styles = {
    'obs': {'color':ROOT.kRed, 'style':1, 'width':3},
    'exp': {'color': ROOT.kBlack,   'style':3, 'width':3},
    '1sigma': {'color': 3, 'style':1, 'width':20},
    '2sigma': {'color': 5, 'style':1, 'width':20}
    }

cans = ROOT.TCanvas("cans","",10,10,700,1400)
cans.Range(-10,-1,10,1)

if args.testGrayscale:
    cans.SetGrayscale()

# draw the axis
upper = 0.45
lower = 0.0

axis = ROOT.TGaxis(-9.5,-0.85,9.5,-0.85,lower,upper,505,"")
axisUpper = ROOT.TGaxis(-9.5,0.85,9.5,0.85,lower,upper,505,"-")
axisUpper.SetLabelOffset(10)
axis.SetName("axis")
axis.SetLabelSize(0.03)
axis.Draw()
axisUpper.Draw()

# zero_point = 3.5
# zero = ROOT.TLine(zero_point,-0.85,zero_point,0.85)
# zero.SetLineStyle(1)

box1 = ROOT.TLine(-9.5, -0.85, -9.5, 0.85)
box2 = ROOT.TLine(9.5, -0.85, 9.5, 0.85)
box3 = ROOT.TLine(-9.5, 0.85, 9.5, 0.85)

sigDivdeLine = ROOT.TLine(-9.5, 0.1, 9.5, 0.1)


pads = []

pHeight = 0
### Get all the pads ###
for p in range(len(res)+1):
    y_lo = 0.9-0.8*((p+1.)/(len(res)+1))
    y_hi = 0.9-0.8*(float(p)/(len(res)+1))
    pHeight = y_hi - y_lo

    pads.append(ROOT.TPad("pad_%s"%p,"pad_%s"%p, 0.5/20, y_lo, 19.5/20, y_hi ))
    pads[-1].Range(lower,0,upper,5)
    pads[-1].SetFillColor(0)
    pads[-1].Draw()
    pads[-1].cd()
    
    if p>=len(res): continue
    # put the stuff
    graphs  = []
    res[p]['lines'] = []
    for i, o in enumerate(ordering):
        limits = res[p]['limits'][o]
        x = []
        y = []
        y_err = []
        x_plus = []
        x_minus = []
        for j,l in enumerate(limits):
            start = 4.4
            newLines = []
            if o=="obs" or o=="exp":
                newLines += [   ROOT.TLine(l[0], start-0.5+0.5,  l[0], start-0.5-0.5),
                                ROOT.TLine(l[1], start-0.5+0.5,  l[1], start-0.5-0.5)]
            else:
                newLines += [   ROOT.TLine(l[0], start-0.5,       l[1], start-0.5)]
            for k,line in enumerate(newLines):
                line.SetLineColor(styles[o]['color'])
                line.SetLineWidth(styles[o]['width'])
                line.SetLineStyle(styles[o]['style'])
            
            res[p]['lines'] += copy.deepcopy(newLines)
    
    for l in res[p]['lines']:
        l.Draw()
    cans.cd()

cans.cd()

# zero.Draw()
box1.Draw()
box2.Draw()
box3.Draw()

sigDivdeLine.Draw()

## need a legend
leg = ROOT.TLegend(0.05,0.22-0.025*(len(ordering)+1),0.95,0.22)
leg.SetFillColor(ROOT.kWhite)
leg.SetShadowColor(ROOT.kWhite)
leg.SetBorderSize(0)
leg.SetTextSize(0.04)
leg.SetNColumns(2)
leg.AddEntry(res[0]['lines'][4],  "#bf{95% CL Expected Limit}", 'l')
leg.AddEntry(res[0]['lines'][1],  "#bf{#pm1#sigma Exp. Limit}", 'l')
leg.AddEntry(res[0]['lines'][2],  "#bf{95% CL Observed Limit}", 'l')
leg.AddEntry(res[0]['lines'][0],  "#bf{#pm2#sigma Exp. limit}", 'l')

leg.Draw()


# l1 = ROOT.TLine()
# l1.SetLineColor(ROOT.kBlack)
# l1.SetLineWidth(3)
# l1.DrawLineNDC(0.063,0.823,0.063,0.837)
# l1.DrawLineNDC(0.125,0.823,0.125,0.837)

# l2 = ROOT.TLine()
# l2.SetLineColor(ROOT.kRed+1)
# l2.SetLineWidth(2)
# l2.DrawLineNDC(0.063,0.783,0.063,0.797)
# l2.DrawLineNDC(0.125,0.783,0.125,0.797)

# l3 = ROOT.TLine()
# l3.SetLineColor(ROOT.kBlue-6)
# l3.SetLineWidth(2)
# l3.DrawLineNDC(0.063,0.743,0.063,0.757)
# l3.DrawLineNDC(0.125,0.743,0.125,0.757)

# l4 = ROOT.TLine()
# l4.SetLineColor(ROOT.kOrange-2)
# l4.SetLineWidth(2)
# l4.DrawLineNDC(0.063,0.703,0.063,0.717)
# l4.DrawLineNDC(0.125,0.703,0.125,0.717)

# l5 = ROOT.TLine()
# l5.SetLineColor(ROOT.kSpring+6)
# l5.SetLineWidth(2)
# l5.DrawLineNDC(0.063,0.663,0.063,0.677)
# l5.DrawLineNDC(0.125,0.663,0.125,0.677)

# l6 = ROOT.TLine()
# l6.SetLineColor(ROOT.kBlack)
# l6.SetLineWidth(2)
# l6.DrawLineNDC(0.063,0.623,0.063,0.637)
# l6.DrawLineNDC(0.125,0.623,0.125,0.637)

## finish it off

latex1 = ROOT.TLatex()
latex1.SetNDC()
latex1.SetTextSize(0.06)
latex1.SetTextAlign(11)

if args.preliminary:
    latex1.DrawLatex(0.03,0.94,'CMS #bf{#it{Preliminary}}')
    latex1.DrawLatex(0.55, 0.94, "#bf{138 fb^{-1} (13 TeV)}")
else:
    latex1.DrawLatex(0.03,0.94,'CMS')
    latex1.DrawLatex(0.55, 0.94, "#bf{138 fb^{-1} (13 TeV)}")

latex2 = ROOT.TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.05)
latex2.SetTextAlign(11)
for i,r in enumerate(res):
    latex2.DrawLatex(0.6, 0.86-(pHeight)*(i), '#bf{%s}'%r['tex'])

latex3 = ROOT.TLatex()
latex3.SetNDC()
latex3.SetTextSize(0.06)
latex3.SetTextAlign(11)
latex3.DrawLatex(0.8, 0.85, '#bf{t #rightarrow uH}')

latex4 = ROOT.TLatex()
latex4.SetNDC()
latex4.SetTextSize(0.06)
latex4.SetTextAlign(11)
latex4.DrawLatex(0.8, 0.5, '#bf{t #rightarrow cH}')

latex5 = ROOT.TLatex()
latex5.SetNDC()
latex5.SetTextSize(0.05)
latex5.SetTextAlign(11)
latex5.DrawLatex(0.575, 0.01, '#bf{Branching Ratio (%)}')

plotDir = args.out + "/summary/"

if not os.path.isdir(plotDir):
    os.makedirs(plotDir)

postFix = '_FCNC'
if args.preliminary: postFix += '_preliminary'

if args.testGrayscale:
    postFix += '_gray'

for e in [".png",".pdf",".root"]:
    cans.Print(plotDir+"summaryResult"+postFix+e)
