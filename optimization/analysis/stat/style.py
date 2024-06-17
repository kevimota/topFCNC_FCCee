import ROOT

def SetPlotStyle(name=''):

    if name == '': name = 'PLOT'
    
    plotStyle = PlotStyle(name);
    ROOT.gROOT.SetStyle(name)
    ROOT.gROOT.ForceStyle()
    
    return plotStyle

def PlotStyle(name):

    plotStyle = ROOT.TStyle(name, 'Plot style')
    
    plotStyle.SetErrorX(0.0001)

    icol = 0
    plotStyle.SetFrameBorderMode(icol)
    plotStyle.SetFrameFillColor(icol)
    plotStyle.SetCanvasBorderMode(icol)
    plotStyle.SetCanvasColor(icol)
    plotStyle.SetPadBorderMode(icol)
    plotStyle.SetPadColor(icol)
    plotStyle.SetStatColor(icol)

    plotStyle.SetPaperSize(20,26)

    plotStyle.SetPadTopMargin(0.07)
#    plotStyle.SetPadRightMargin(0.2)
    plotStyle.SetPadBottomMargin(0.18)
    plotStyle.SetPadLeftMargin(0.16)

    plotStyle.SetTitleXOffset(1.2)
    plotStyle.SetTitleYOffset(1.2)

    font = 42
    tsize = 0.05
    plotStyle.SetTextFont(font)

    plotStyle.SetTextSize(tsize)
    plotStyle.SetLabelFont(font,"x")
    plotStyle.SetTitleFont(font,"x")
    plotStyle.SetLabelFont(font,"y")
    plotStyle.SetTitleFont(font,"y")
    plotStyle.SetLabelFont(font,"z")
    plotStyle.SetTitleFont(font,"z")
  
    plotStyle.SetLabelSize(tsize,"x")
    plotStyle.SetTitleSize(tsize,"x")
    plotStyle.SetLabelSize(tsize,"y")
    plotStyle.SetTitleSize(tsize,"y")
    plotStyle.SetLabelSize(tsize,"z")
    plotStyle.SetTitleSize(tsize,"z")

    plotStyle.SetMarkerStyle(20)
    plotStyle.SetMarkerSize(1.2)
    plotStyle.SetHistLineWidth(2)
    plotStyle.SetLineStyleString(2,"[12 12]")

    plotStyle.SetEndErrorSize(0.)

    plotStyle.SetOptTitle(0)
    plotStyle.SetOptStat(0)
    plotStyle.SetOptFit(0)

    plotStyle.SetPadTickX(1)
    plotStyle.SetPadTickY(1)

    return plotStyle

def fcclabel():

    tex = ROOT.TLatex(0.66,0.88,"IDEA")
    tex.SetNDC()
    tex.SetTextAlign(13)
    tex.SetTextFont(61)
    tex.SetTextSize(0.073)
    tex.SetLineWidth(2)
   
    tex2 = ROOT.TLatex(0.66,0.81,"Internal")
    tex2.SetNDC()
    tex2.SetTextAlign(13)
    tex2.SetTextFont(52)
    tex2.SetTextSize(0.055)
    tex2.SetLineWidth(2)
    
    linfo = ROOT.TLatex(0.90,0.945,"#sqrt{s} = 365 GeV, 1.5 ab^{-1}")
        
    linfo.SetNDC()
    linfo.SetTextAlign(31)
    linfo.SetTextFont(42)
    linfo.SetTextSize(0.04875)
    linfo.SetLineWidth(2)

    return tex, tex2, linfo

def channel(chan):

   tex = ROOT.TLatex(0.60,0.906825,chan)
   tex.SetNDC()
   tex.SetTextAlign(13)
   tex.SetTextFont(61)
   tex.SetTextSize(0.05475)
   tex.SetLineWidth(2)
   
   return tex

