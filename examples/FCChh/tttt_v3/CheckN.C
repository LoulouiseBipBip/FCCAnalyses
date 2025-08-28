void CheckN() {
    // Open the ROOT file
    TFile *f = TFile::Open("root://eoshome-l.cern.ch//eos/user/l/lberiet/Histmaker/tttt_v3/4l/mgp8_pp_ttz_5f_Q_0_1000_84TeV_ttzlep.root");
    if (!f || f->IsZombie()) {
       std::cout << "Error: Cannot open file!" << std::endl;
       return;
    }
 
    // Get histogram and metadata
    TH1D *h = (TH1D*)f->Get("cutFlow");
    TParameter<int> *eventsProcessed = (TParameter<int>*)f->Get("eventsProcessed");
    TParameter<float> *sumOfWeights = (TParameter<float>*)f->Get("sumOfWeights");
    TParameter<float> *crossSection = (TParameter<float>*)f->Get("crossSection");
    TParameter<float> *intLumi = (TParameter<float>*)f->Get("intLumi");
    TParameter<float> *kfactor = (TParameter<float>*)f->Get("kfactor");
    TParameter<float> *matchingEfficiency = (TParameter<float>*)f->Get("matchingEfficiency");
 
    // Check if objects exist
    if (!h) {
       std::cout << "Error: Histogram cutFlow not found!" << std::endl;
       f->Close();
       return;
    }
    if (!eventsProcessed || !sumOfWeights || !crossSection || !intLumi || !kfactor || !matchingEfficiency) {
       std::cout << "Error: Some metadata objects are missing!" << std::endl;
       f->Close();
       return;
    }
 
    // Get bin contents of cutFlow
    int nBins = 1;
    std::cout << "cutFlow Histogram: " << nBins << " bins" << std::endl;
    for (int i = 1; i <= nBins; ++i) {
       std::cout << "Bin " << i << " (" << h->GetXaxis()->GetBinLabel(i) << "): " << h->GetBinContent(i) << std::endl;
    }
    double preCutEvents = h->GetBinContent(nBins); // Events after final cut
    std::cout << "Pre cut events (First bin): " << preCutEvents << std::endl;
 
    // Get metadata values
    int nEvents = eventsProcessed->GetVal();
    float sumW = sumOfWeights->GetVal();
    float xsec = crossSection->GetVal();
    float lumi = intLumi->GetVal();
    float kf = kfactor->GetVal();
    float me = matchingEfficiency->GetVal();
 
    // Print metadata
    std::cout << "eventsProcessed: " << nEvents << std::endl;
    std::cout << "sumOfWeights: " << sumW << std::endl;
    std::cout << "crossSection: " << xsec << " pb" << std::endl;
    std::cout << "intLumi: " << lumi << " pb^-1" << std::endl;
    std::cout << "kfactor: " << kf << std::endl;
    std::cout << "matchingEfficiency: " << me << std::endl;
 
    // Calculate scale factor
    double scaled = (xsec * kf * me * lumi) ;
    std::cout << "Expected scaled events : " << scaled << std::endl;
 
    // Close file
    f->Close();
 }