/* histo plotting macro */

{
  Int_t i;

  //set axis ranges and log scale
  Int_t SETLOGY=1;
  Int_t SETXRANGE=1;
  Int_t SETYRANGE=0;
  Int_t SETYRATRANGE=1;
  Int_t SETNDIV=0;
  Int_t CENTERLAB=0;
  Double_t RX1=20;
  Double_t RX2=260;
  Double_t RY1=0x;
  Double_t RY2=0;
  Double_t RATRY1=0.0;
  Double_t RATRY2=3.0;
  bool NORMED = false;
  Double_t max_val = 0.0;
  Double_t max_val_tmp;

  // number of files to be opened
  Int_t FILES=2;
  // number of curves to be plotted
  Int_t REPNFIL=1;
  // histogram base name
  TString hist_base = "DijetMass_2jet_1";
  if (NORMED) hist_base = "Normalized_XS/" + hist_base + "_norm";

  //open files, set normalization, retrieve+scale && rebin histos
  //std::string fnames1[FILES]={"VBF_Systematics.root"};
  std::string fnames1[FILES]={"VBF_Systematics.root", "VBF_Systematics_merged_stats.root"};
  //std::string legents[REPNFIL]={"Sherpa Nominal", "Sherpa Nominal MjjFilt", "POWHEG Nominal bornsuppfact"};
  std::string legents[REPNFIL]={"Sherpa Nominal MjjFilt"};
  // Create a list of all paths so that I can just reference that list.
  //TString histpaths[REPNFIL]={"147775.Nominal_Sherpa_Background/", "129930.Nominal_Sherpa_Background_MjjFilt/", "000001.Powheg.W2jets.Nominal/"};
  TString histpaths[REPNFIL]={"129930.Nominal_Sherpa_Background_MjjFilt/"};

  TFile* fpoint1[FILES];
  for (i=0; i<FILES; i++)
    {
      fpoint1[i]= new TFile(fnames1[i].c_str(),"update");
      if (!fpoint1[i]->IsOpen()) {
	std::cout << "no file found for: " << fnames1[i] << std::endl;
	return NULL;
	gROOT->ProcessLine(".q");
      }
    }

  TH1* hvect1[REPNFIL];
  Int_t LineStyle[]={ 1 , 1, 1};
  Color_t LineColor[]={ kBlack , kRed+1, kBlue};
  Int_t LineWidth[]={ 2 , 2, 2};
  Int_t MarkerStyle[]={ 0 , 0, 0}; 
  Int_t MarkerSize[]={ 0 , 0, 0};

  for (i=0; i<REPNFIL; i++)
    {
      //std::string hist_to_get = std::string(histpaths[i])+hist_base;
      hist_to_get = histpaths[i] + hist_base;
      hvect1[i]=(TH1*)fpoint1[0]->Get(hist_to_get);
      hvect1[i]->Rebin(5); 
      max_val_tmp=hvect1[i].GetMaximum();
      if (max_val < max_val_tmp): max_val = max_val_tmp;
      hvect1[i]->SetLineStyle(LineStyle[i]);
      hvect1[i]->SetLineColor(LineColor[i]);
      hvect1[i]->SetLineWidth(LineWidth[i]);
      hvect1[i]->SetMarkerStyle(MarkerStyle[i]);
      hvect1[i]->SetMarkerSize(MarkerSize[i]);
      hvect1[i]->SetMarkerColor(LineColor[i]);
    }
    // for (i=REPNFIL; i<REPNFIL*FILES; i++)
    //   {
    //     //std::string hist_to_get = std::string(histpaths[i])+hist_base;
    //     hist_to_get = histpaths[i] + hist_base;
    //     hvect1[i]=(TH1*)fpoint1[1]->Get(hist_to_get);
    //     hvect1[i]->Rebin(5); 
    //     max_val_tmp=hvect1[i].GetMaximum();
    //     if (max_val < max_val_tmp): max_val = max_val_tmp;
    //     hvect1[i]->SetLineStyle(LineStyle[i]);
    //     hvect1[i]->SetLineColor(LineColor[i]);
    //     hvect1[i]->SetLineWidth(LineWidth[i]);
    //     hvect1[i]->SetMarkerStyle(MarkerStyle[i]);
    //     hvect1[i]->SetMarkerSize(MarkerSize[i]);
    //     hvect1[i]->SetMarkerColor(LineColor[i]);
    //   }
  
  //---------------------------------------------------------------------------------------
  // plot
  c0 = new TCanvas("c0","",50,50,865,780);
  c0->cd();

  TPad *pad1 = new TPad("pad1","top pad",0,0.40,1,1);
  TPad *pad2 = new TPad("pad2","bottom pad",0,0,1,0.40);

  pad1->SetFillStyle(0);
  pad1->SetFrameFillStyle(0);
  pad2->SetFillStyle(0);
  pad2->SetFrameFillStyle(0);

  pad1->Draw();
  pad2->Draw();

  //---------------------------------------------------------------------------------------
  no_TPad_BottomMargin(pad1); 
  if (SETLOGY == 1) pad1->SetLogy();
  pad1->cd();

  //if (SETXRANGE == 1) hvect1[0]->SetAxisRange(RX1,RX2,"x");
  //if (SETYRANGE == 1) hvect1[0]->SetAxisRange(RY1,RY2,"y");
  Large_label_title_top(hvect1[0]);
  hvect1[0]->GetYaxis()->SetTitle(hvect1[0]->GetYaxis()->GetTitle());
  if (SETNDIV==1) hvect1[0]->GetXaxis()->SetNdivisions();
  if (CENTERLAB==1) hvect1[0]->GetXaxis()->CenterLabels();

  hvect1[0]->SetMaximum(2.0*max_val);
  hvect1[0]->DrawClone("");
  for (i=0; i<REPNFIL; i++){hvect1[i]->DrawClone("same");hvect1[i]->DrawClone("samep");}

  //margins :
  Double_t lx1,ly1,lx2,ly2;
  lx1=0.60; ly1=0.9-0.10*REPNFIL; lx2=0.90; ly2=0.89;
  Double_t ptitx1,ptity1,ptitx2,ptity2;
  ptitx1=0.01; ptity1=0.91;ptitx2=lx1+0.1; ptity2=0.996;

  // legend
  leg= new TLegend(lx1,ly1,lx2,ly2);
  leg->SetFillColor(0);
  leg->SetShadowColor(0);
  leg->SetBorderSize(0);
  for (i=0; i<REPNFIL; i++) leg->AddEntry(hvect1[i],legents[i].c_str(),"pl");
  leg->Draw(); 

  // histo title
  TPaveText *ptit = new TPaveText(ptitx1,ptity1,ptitx2,ptity2,"NDC");
  ptit->SetBorderSize(0.);
  ptit->SetFillColor(0.);
  ptit->SetTextFont(62);
  ptit->SetMargin(0.01);
  ptit->AddText(hvect1[0]->GetTitle());
  ptit->Draw("same");

  //---------------------------------------------------------------------------------------
  no_TPad_TopMargin(pad2);
  pad2->cd();

  for (i=1; i<REPNFIL; i++) hvect1[i]->Divide(hvect1[0]);
  hvect1[0]->Divide(hvect1[0]);  
   
  if (SETYRATRANGE == 1)  hvect1[0]->SetAxisRange(RATRY1,RATRY2,"y");
  //hvect1[0]->GetXaxis()->SetTitle("pt[GeV]");
  hvect1[0]->GetYaxis()->SetTitle("Filt/NoFilt");
  hvect1[0]->SetFillStyle(3004);
  hvect1[0]->SetFillColor(LineColor[0]);
  Large_label_title_bot(hvect1[0]);
  hvect1[0]->DrawClone("E2");

  for (i=1; i<REPNFIL; i++) {hvect1[i]->DrawClone("same");hvect1[i]->DrawClone("samep");}
 
  //---------------------------------------------------------------------------------------
  if (!NORMED): c0->SaveAs("Distribution.pdf");
  if (NORMED): c0->SaveAs("Normalized.pdf");

  gROOT->ProcessLine(".q");
}
