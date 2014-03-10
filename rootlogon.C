void rootlogon()
{
  gROOT->LoadMacro("Style.C");
  gROOT->ProcessLine(".L Utils.C");
  //SetThesisStyle();
}
