import ROOT
import json
import copy
import numpy

import tdrStyle
tdrStyle.setTDRStyle()

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--limits", help = "path to json with limits", type=str, default="./kappaCalculationOutputs/combLimits.json")
parser.add_argument("--tag", help = "tag", type=str, default = "test")
parser.add_argument("--blinding", help = "blind boolean, blind =1", type=str, default = "True")
args = parser.parse_args()

isBlind = 1
if args.blinding.lower() == "false": isBlind = 0
print("isblind: ", isBlind)

ROOT.gStyle.SetPaintTextFormat("4.3f")

gamma_t = 1.32158
gamma_hqt = 0.1904
def limit_to_coupling(limit):
    return numpy.sqrt((limit/100.) * (gamma_t / gamma_hqt)) # factor of 100 since limits are in %

with open(args.limits, "r") as f_in:
    results = json.load(f_in)

def interpolate(limit_hut, limit_hct, n_interp = 10000):
    """
    Assume the following equation:
    BR_Hct^interp / BR_Hct^1d + BR_Hut^interp / BR_Hut^1d = 1
    return arrays for limit_hut and limit_hct
    """
    limit_interp_hut = numpy.linspace(0, limit_hut, n_interp)
    limit_interp_hct = numpy.zeros(n_interp)
    for i in range(len(limit_interp_hut)):
        limit_interp_hct[i] = limit_hct * ( 1 - (limit_interp_hut[i] / limit_hut) )

    return limit_interp_hut, limit_interp_hct

options = {
    "bf" : {
        "xlabel" :  "Branching Ratio (t #rightarrow Hu) (%)",
        "ylabel" :  "Branching Ratio (t #rightarrow Hc) (%)",
        "ymax" : 0.1,
        "xmax" : 0.12,
    },
    "coupling" : {
        "xlabel" : "#kappa_{Hut}",
        "ylabel" : "#kappa_{Hct}",
        "ymax" : 0.1,
        "xmax" : 0.1,
    }
} 

results_bf = {}
results_coupling = {}
for limit, val in results["Hut"]["Run2"].items():
    if limit == "input":
        continue
    bf_hut, bf_hct = interpolate(val, results["Hct"]["Run2"][limit])
    coupling_hut = limit_to_coupling(bf_hut)
    coupling_hct = limit_to_coupling(bf_hct)

    results_bf[limit] = { "Hut" : bf_hut, "Hct" : bf_hct }
    results_coupling[limit] = { "Hut" : coupling_hut, "Hct" : coupling_hct }

options["bf"]["results"] = results_bf
options["coupling"]["results"] = results_coupling

def create_shade_boxes(limit_down1sigma_x, limit_down1sigma_y, limit_up1sigma_x, limit_up1sigma_y):
    boxes = []
    for i in range(len(limit_down1sigma_x)):
        diff_x = limit_up1sigma_x[i] - limit_down1sigma_x[i]
        diff_y = limit_up1sigma_y[i] - limit_down1sigma_y[i]
        #if diff_x <= 0.0001:
        #    diff_x = 0.0001
        #if diff_y == 0.0001:
        #    diff_y = 0.0001
        box = ROOT.TBox(limit_down1sigma_x[i], limit_down1sigma_y[i], limit_down1sigma_x[i] + diff_x, limit_down1sigma_y[i] + diff_y)
        boxes.append(box)
    return boxes

for plot_type in options.keys():
    c1 = ROOT.TCanvas("c1", "c1", 800, 800)

    limit_exp_hut = options[plot_type]["results"]["exp"]["Hut"]
    limit_exp_hct = options[plot_type]["results"]["exp"]["Hct"]
    limit_bb_hut = options[plot_type]["results"]["bb"]["Hut"]
    limit_bb_hct = options[plot_type]["results"]["bb"]["Hct"]
    limit_gg_hut = options[plot_type]["results"]["gg"]["Hut"]
    limit_gg_hct = options[plot_type]["results"]["gg"]["Hct"]
    limit_ss_hut = options[plot_type]["results"]["ss"]["Hut"]
    limit_ss_hct = options[plot_type]["results"]["ss"]["Hct"]
    limit_bb_hut_exp = options[plot_type]["results"]["bb_exp"]["Hut"]
    limit_bb_hct_exp = options[plot_type]["results"]["bb_exp"]["Hct"]
    limit_gg_hut_exp = options[plot_type]["results"]["gg_exp"]["Hut"]
    limit_gg_hct_exp = options[plot_type]["results"]["gg_exp"]["Hct"]
    limit_ss_hut_exp = options[plot_type]["results"]["ss_exp"]["Hut"]
    limit_ss_hct_exp = options[plot_type]["results"]["ss_exp"]["Hct"]
    # limit_bbgg_hut = options[plot_type]["results"]["gg+bb"]["Hut"]
    # limit_bbgg_hct = options[plot_type]["results"]["gg+bb"]["Hct"]
    # limit_ggss_hut = options[plot_type]["results"]["gg+ss"]["Hut"]
    # limit_ggss_hct = options[plot_type]["results"]["gg+ss"]["Hct"]
    # limit_bbss_hut = options[plot_type]["results"]["bb+ss"]["Hut"]
    # limit_bbss_hct = options[plot_type]["results"]["bb+ss"]["Hct"]

    if not isBlind:
        limit_obs_hut = options[plot_type]["results"]["obs"]["Hut"]
        limit_obs_hct = options[plot_type]["results"]["obs"]["Hct"]
    limit_p1sigma_hut = options[plot_type]["results"]["+1sigma"]["Hut"] 
    limit_p1sigma_hct = options[plot_type]["results"]["+1sigma"]["Hct"]
    limit_p2sigma_hut = options[plot_type]["results"]["+2sigma"]["Hut"]
    limit_p2sigma_hct = options[plot_type]["results"]["+2sigma"]["Hct"]
    limit_m1sigma_hut = options[plot_type]["results"]["-1sigma"]["Hut"]
    limit_m1sigma_hct = options[plot_type]["results"]["-1sigma"]["Hct"]
    limit_m2sigma_hut = options[plot_type]["results"]["-2sigma"]["Hut"]
    limit_m2sigma_hct = options[plot_type]["results"]["-2sigma"]["Hct"]

    n = len(limit_exp_hut)

    boxes_2sigma = create_shade_boxes(limit_m2sigma_hut, limit_m2sigma_hct, limit_p2sigma_hut, limit_p2sigma_hct)
    for box in boxes_2sigma:
        box.SetLineWidth(0)
        box.SetFillColor(5)

    boxes_1sigma = create_shade_boxes(limit_m1sigma_hut, limit_m1sigma_hct, limit_p1sigma_hut, limit_p1sigma_hct)
    for box in boxes_1sigma:
        box.SetLineWidth(0)
        box.SetFillColor(3) 
 
    g_exp = ROOT.TGraph(n, limit_exp_hut, limit_exp_hct)
    if not isBlind:
        g_obs = ROOT.TGraph(n, limit_obs_hut, limit_obs_hct)

    g_bb = ROOT.TGraph(n, limit_bb_hut, limit_bb_hct)
    g_gg = ROOT.TGraph(n, limit_gg_hut, limit_gg_hct)
    g_ss = ROOT.TGraph(n, limit_ss_hut, limit_ss_hct)

    g_bb_exp = ROOT.TGraph(n, limit_bb_hut_exp, limit_bb_hct_exp)
    g_gg_exp = ROOT.TGraph(n, limit_gg_hut_exp, limit_gg_hct_exp)
    g_ss_exp = ROOT.TGraph(n, limit_ss_hut_exp, limit_ss_hct_exp)

    # g_bbgg = ROOT.TGraph(n, limit_bbgg_hut, limit_bbgg_hct)
    # g_ggss = ROOT.TGraph(n, limit_ggss_hut, limit_ggss_hct)
    # g_bbss = ROOT.TGraph(n, limit_bbss_hut, limit_bbss_hct)


    g_exp.SetLineStyle(3)
    g_exp.SetLineWidth(3)
    if not isBlind:
        g_obs.SetLineStyle(0)
        g_obs.SetLineWidth(3)

    g_bb.SetLineStyle(0)
    g_bb.SetLineWidth(3)
    g_bb.SetLineColor(225)
    g_gg.SetLineStyle(0)
    g_gg.SetLineWidth(3)
    g_gg.SetLineColor(2)
    g_ss.SetLineStyle(0)
    g_ss.SetLineWidth(3)
    g_ss.SetLineColor(4)

    g_bb_exp.SetLineStyle(3)
    g_bb_exp.SetLineWidth(3)
    g_bb_exp.SetLineColor(225)
    g_gg_exp.SetLineStyle(3)
    g_gg_exp.SetLineWidth(3)
    g_gg_exp.SetLineColor(2)
    g_ss_exp.SetLineStyle(3)
    g_ss_exp.SetLineWidth(3)
    g_ss_exp.SetLineColor(4)

    # g_bbgg.SetLineStyle(0)
    # g_bbgg.SetLineWidth(3)
    # g_bbgg.SetLineColor(225)
    # g_ggss.SetLineStyle(0)
    # g_ggss.SetLineWidth(3)
    # g_ggss.SetLineColor(94)
    # g_bbss.SetLineStyle(0)
    # g_bbss.SetLineWidth(3)
    # g_bbss.SetLineColor(9)

    g_exp.Draw()
    g_exp.SetMinimum(0)
    g_exp.SetMaximum(options[plot_type]["ymax"])
    for box in boxes_2sigma:
        box.Draw("SAME")
    for box in boxes_1sigma:
        box.Draw("SAME")
    g_exp.Draw("SAME")
    if not isBlind:
        g_obs.Draw("SAME")
    g_bb.Draw("SAME")
    g_gg.Draw("SAME")
    g_ss.Draw("SAME")
    g_bb_exp.Draw("SAME")
    g_gg_exp.Draw("SAME")
    g_ss_exp.Draw("SAME")
    # g_bbgg.Draw("SAME")
    # g_ggss.Draw("SAME")
    # g_bbss.Draw("SAME")

    axis = g_exp.GetXaxis()
    axis.SetLimits(0, options[plot_type]["xmax"])
    g_exp.Draw("SAME")
    g_exp.GetYaxis().SetTitle(options[plot_type]["ylabel"])
    g_exp.GetXaxis().SetTitle(options[plot_type]["xlabel"])
    g_exp.GetYaxis().SetTitleOffset(1.23)
    g_exp.GetYaxis().SetNdivisions(5,5,0)
    g_exp.GetXaxis().SetNdivisions(5,5,0)

    ROOT.gPad.RedrawAxis()
    c1.Update()

    legend = ROOT.TLegend(0.6, 0.6, 0.9, 0.87)
    if not isBlind:
        legend.AddEntry(g_obs, "Observed", "l")
    legend.AddEntry(g_exp, "Median Expected", "l")
    legend.AddEntry(boxes_1sigma[0], "#pm 1#sigma", "f")
    legend.AddEntry(boxes_2sigma[0], "#pm 2#sigma", "f")
    legend.AddEntry(g_bb, "b#bar{b}")
    legend.AddEntry(g_bb_exp, "b#bar{b} Expected")
    legend.AddEntry(g_gg, "diphoton")
    legend.AddEntry(g_gg_exp, "diphoton Expected")
    legend.AddEntry(g_ss, "leptonic")
    legend.AddEntry(g_ss_exp, "leptonic Expected")
    # legend.AddEntry(g_bbgg, "b#bar{b} + diphoton")
    # legend.AddEntry(g_ggss, "diphoton + leptonic")
    # legend.AddEntry(g_bbss, "b#bar{b} + leptonic")
    legend.SetBorderSize(0)
    legend.Draw("SAME")

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.4*c1.GetTopMargin())
    latex.SetTextFont(42)
    latex.SetTextAlign(11)
    latex.SetTextColor(1)
    latex.DrawLatex(0.68, 0.88, "95% CL Upper Limits") 

    latex.SetTextSize(0.6*c1.GetTopMargin())
    latex.DrawLatex(0.12, 0.935, "#bf{CMS}")

    latex.SetTextSize(0.6*c1.GetTopMargin())
    # latex.DrawLatex(0.215, 0.935, "#it{Preliminary}")

    latex.DrawLatex(0.67, 0.935, "138 fb^{-1} (13 TeV)")

    c1.SaveAs("./kappaCalculationOutputs/limits2dWithInd_%s_%s.pdf" % (args.tag, plot_type)) 
