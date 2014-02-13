void SetThesisStyle ()
{
  std::cout << "\n LM : apply costum style. \n" << std::endl ;
  TStyle* thesisStyle = ThesisStyle();
  gROOT->SetStyle("THESIS");
  gROOT->ForceStyle();
}


TStyle* ThesisStyle() 
{
  TStyle *thesisStyle = new TStyle("THESIS","Thesis style");
  TGaxis::SetMaxDigits(2);
  Int_t icol=0; // WHITE
  thesisStyle->SetFrameBorderMode(icol);
  thesisStyle->SetFrameFillColor(icol);
  thesisStyle->SetCanvasBorderMode(icol);
  thesisStyle->SetCanvasColor(icol);
  thesisStyle->SetPadBorderMode(icol);
  thesisStyle->SetPadColor(icol);
  thesisStyle->SetStatColor(icol);

  thesisStyle->SetGridColor(kGray);
  thesisStyle->SetGridStyle(1);
  
  /*
  // leaving these out ... 

  // set the paper & margin sizes
  thesisStyle->SetPaperSize(20,26);

  */

  // set margin sizes
  thesisStyle->SetPadTopMargin(0.1);
  thesisStyle->SetPadRightMargin(0.05);
  thesisStyle->SetPadBottomMargin(0.13);
  thesisStyle->SetPadLeftMargin(0.12);

  // set title offsets (for axis label)
  thesisStyle->SetTitleXOffset(1.0);
  thesisStyle->SetTitleYOffset(1.0);

  //thesisStyle->SetFillStyle(0);
  //thesisStyle->SetFrameFillStyle(0);  

  thesisStyle->SetOptTitle(0);
  thesisStyle->SetOptStat(0);

  //----------------------------------------
  thesisStyle->SetMarkerSize(1.0);

  Int_t font(42);
  thesisStyle->SetTextFont(font);
  thesisStyle->SetTitleFont(font);
  thesisStyle->SetLabelFont(font,"x");
  thesisStyle->SetTitleFont(font,"x");
  thesisStyle->SetLabelFont(font,"y");
  thesisStyle->SetTitleFont(font,"y");

  Double_t tsize=0.06;
  thesisStyle->SetTextSize(tsize);
  thesisStyle->SetLabelSize(tsize,"x");
  thesisStyle->SetTitleSize(tsize,"x");
  thesisStyle->SetLabelSize(tsize,"y");
  thesisStyle->SetTitleSize(tsize,"y");

  //thesisStyle->SetTitleOffset(0.9,"x");
  //thesisStyle->SetTitleOffset(0.9,"y");
  //----------------------------------------

  return thesisStyle;
}


/*

Int_t setstlyle(TH1 *h1,TH1 *h2)
{

 gStyle->SetPadBottomMargin(0.12);
 gStyle->SetPadLeftMargin(0.14);

  h1->GetXaxis()->SetLabelSize(0.055);
  h2->GetXaxis()->SetLabelSize(0.055); 
  h1->GetYaxis()->SetLabelSize(0.055);
  h2->GetYaxis()->SetLabelSize(0.055); 
  h1->GetXaxis()->SetLabelFont(42);
  h2->GetXaxis()->SetLabelFont(42); 
  h1->GetYaxis()->SetLabelFont(42);
  h2->GetYaxis()->SetLabelFont(42); 
  h1->GetXaxis()->SetTitleSize(0.055);
  h2->GetXaxis()->SetTitleSize(0.055); 
  h1->GetYaxis()->SetTitleSize(0.055);
  h2->GetYaxis()->SetTitleSize(0.055); 
  h1->GetXaxis()->SetTitleFont(42);
  h2->GetXaxis()->SetTitleFont(42); 
  h1->GetYaxis()->SetTitleFont(42);
  h2->GetYaxis()->SetTitleFont(42); 
  h1->SetTitleFont(42);
  h2->SetTitleFont(42);
  h1->SetLineStyle(1);
  h2->SetLineStyle(1);
  h2->SetFillStyle(3004);
  h2->SetFillColor(kBlack);
  h1->GetYaxis()->SetTitleOffset(1.3);
  h2->GetYaxis()->SetTitleOffset(1.3);

  gStyle->SetTitleFont(42);

 return 0;

}
*/

Int_t setstlyle(TH1 *h1,TH1 *h2)
{
  return 0;
}

Int_t setstlyle1(TH1 *h1,TH1 *h2)
{
  //gStyle->SetPadBottomMargin(0.05);
  h1->GetYaxis()->SetTitleSize(0.065);
  h2->GetYaxis()->SetTitleSize(0.065); 
 return 0;
}


