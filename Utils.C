void no_xlabel_xtitle(TH1 *histo1)
{
  histo1->GetXaxis()->SetLabelColor(0);
  histo1->GetXaxis()->SetTitleColor(0);
}

void large_label_title(TH1 *histo1)
{
  histo1->GetXaxis()->SetLabelSize(33);
  histo1->GetXaxis()->SetTitleSize(0.06);
  histo1->GetYaxis()->SetTitleSize(0.06);
  histo1->GetXaxis()->SetTickLength(0.03);
  histo1->GetYaxis()->SetLabelSize(33);
  histo1->GetYaxis()->SetTitleSize(35);
  histo1->GetYaxis()->SetTickLength(0.03);
  histo1->GetYaxis()->SetNdivisions(507);
}

void Large_label_title_bot(TH1 *histo1)
{
  histo1->GetXaxis()->SetLabelSize(33);
  histo1->GetXaxis()->SetTitleSize(0.12);
  histo1->GetYaxis()->SetTitleSize(0.12);
  histo1->GetXaxis()->SetTickLength(0.05);
  histo1->GetYaxis()->SetTickLength(0.05);
  histo1->GetXaxis()->SetLabelSize(0.12);
  histo1->GetYaxis()->SetLabelSize(0.12);
  histo1->GetYaxis()->SetTitleOffset(0.45);
  histo1->GetYaxis()->SetNdivisions(507);
  histo1->SetLineWidth(2);

}


void Large_label_title_top(TH1 *histo1)
{
  histo1->GetXaxis()->SetLabelSize(33);
  histo1->GetXaxis()->SetTitleSize(0.065);
  histo1->GetYaxis()->SetTitleSize(0.065);
  histo1->GetXaxis()->SetTickLength(0.04);
  histo1->GetYaxis()->SetTickLength(0.04);
  histo1->GetXaxis()->SetLabelSize(0.065);
  histo1->GetYaxis()->SetLabelSize(0.065);
  histo1->GetYaxis()->SetNdivisions(507);
  histo1->GetYaxis()->SetTitleOffset(0.62*1.37);
  histo1->SetLineWidth(2);

}


void myText(Double_t x,Double_t y,Color_t color,char *text) {

  //Double_t tsize=0.05;
  TLatex l; //l.SetTextAlign(12); l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
}
 

 void myBoxText(Double_t x, Double_t y,Double_t boxsize,Int_t mcolor,char *text) {

  Double_t tsize=0.06;

  TLatex l; l.SetTextAlign(12); //l.SetTextSize(tsize); 
  l.SetNDC();
  l.DrawLatex(x,y,text);

  Double_t y1=y-0.25*tsize;
  Double_t y2=y+0.25*tsize;
  Double_t x2=x-0.3*tsize;
  Double_t x1=x2-boxsize;

  printf("x1= %f x2= %f y1= %f y2= %f \n",x1,x2,y1,y2);

  TPave *mbox= new TPave(x1,y1,x2,y2,0,"NDC");

  mbox->SetFillColor(mcolor);
  mbox->SetFillStyle(1001);
  mbox->Draw();

  TLine mline;
  mline.SetLineWidth(4);
  mline.SetLineColor(1);
  mline.SetLineStyle(1);
  Double_t y=(y1+y2)/2.;
  mline.DrawLineNDC(x1,y,x2,y);

}


void myMarkerText(Double_t x,Double_t y,Int_t color,Int_t mstyle,char *text) {

  //  printf("**myMarker: text= %s\ m ",text);

  Double_t tsize=0.06;
  TMarker *marker = new TMarker(x-(0.4*tsize),y,8);
  marker->SetMarkerColor(color);  marker->SetNDC();
  marker->SetMarkerStyle(mstyle);
  marker->SetMarkerSize(2.0);
  marker->Draw();

  TLatex l; l.SetTextAlign(12); //l.SetTextSize(tsize); 
  l.SetNDC();
  l.DrawLatex(x,y,text);
}

void myLineText(Double_t x, Double_t y,Double_t boxsize,Int_t lstyle,Int_t lcolor, char *text) {

  Double_t tsize=0.055;
  Double_t ttsize=33;
  TLatex l; l.SetTextAlign(12); 
  l.SetTextSize(ttsize); 

  l.SetNDC();
  l.DrawLatex(x,y,text);

  Double_t y1=y-0.25*tsize;
  Double_t y2=y+0.25*tsize;
  Double_t x2=x-0.3*tsize;
  Double_t x1=x2-boxsize;

  TLine mline;
  mline.SetLineWidth(3);
  mline.SetLineColor(lcolor);
  mline.SetLineStyle(lstyle);
  Double_t y=(y1+y2)/2.;
  mline.DrawLineNDC(x1,y,x2,y);

}

void no_TPad_BottomMargin(TPad* somepad)
{
  somepad->SetBottomMargin(0.0);

}
void no_TPad_TopMargin(TPad* somepad)
{
  somepad->SetTopMargin(0.0);
  somepad->SetBottomMargin(0.12/0.46);
}

void TPad_BottomMargin(TPad* somepad)
{
  somepad->SetBottomMargin(0.12/0.86);
}
