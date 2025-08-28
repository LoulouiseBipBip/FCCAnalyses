# README – Prompt/Non-Prompt Lepton BDT at FCC-hh

This folder contains the workflow to train and apply a **BDT** for distinguishing prompt vs non-prompt object, here leptons in the **ttZ analysis**. It can be adapted to be trained on different objects.

---

## 📂 Files
- **`analysis_stage1_BDT.py`**  
  FCCAnalyses stage that reads the ROOT samples and writes out per-object variables (`D0sig`, `Z0sig`, `iso`, etc.) and the event weights (important if running Q-binned samples). This produces flat ntuples for later training.  

- **`BDT.py`**  
  Python script that:
  1. Loads the flat ntuples,
  2. Builds prompt/non-prompt datasets for muons and electrons,
  3. Trains an **XGBoost classifier**,
  4. Saves the trained models to `.json` 

You can adapt it as you wish depending on what you want to classify.
---

##  Workflow

### 1. Produce flat ntuples (stage 1 analysis)
Run the stage 1 FCCAnalyses script to extract lepton-level variables:  
```bash
fccanalysis run analysis_stage1_BDT.py
```

This writes ROOT files with the branches containing your BDT features like:
- `D0_sig_prompt_muons`, `Z0_sig_prompt_muons`, `pTjet_prompt_muons`
- `D0_sig_non_prompt_muons`, ...
- `weight` (event weight)

---

### 2. Train the BDT
Use the training script to build and fit classifiers:  
```bash
python BDT.py
```

This will:
- Read in the variables,
- Split into train/validation (here 50/50) sets,
- Train `XGBClassifier` models for muons and electrons,
- Save them as:
  - `bdt_muon.json`
  - `bdt_electron.json`
- Produce score histograms and ROC curve
You can use the argument `--process-individual` to choose to run the BDT on each Q-binned sample separatly : you will end up with a ROC curve for each Q-bin range on the same plot. 
If no argument, the Q-bins samples will be merged according to the weight.
⚠️ Event weights are broadcast per object before training → every object inherits its event’s statistical weight (necessary for no mismatch between array lengths in BDT).
---

### 3. Apply the BDT
You need to modify `BDTScorer.cxx` to match your BDT definition (add more features...).
You then need to compile it to create an external libray using :
```bash
cd /path/to/BDT
g++ -shared -fPIC -std=c++20 -o libBDTScorer.so BDTScorer.cxx \
    -I$(root-config --incdir) \
    -I/cvmfs/sw.hsf.org/key4hep/releases/2024-10-03/x86_64-almalinux9-gcc14.2.0-opt/xgboost/2.1.1-xijqyj/include \
    -L/cvmfs/sw.hsf.org/key4hep/releases/2024-10-03/x86_64-almalinux9-gcc14.2.0-opt/xgboost/2.1.1-xijqyj/lib -lxgboost \
    -Wl,-rpath,/cvmfs/sw.hsf.org/key4hep/releases/2024-10-03/x86_64-almalinux9-gcc14.2.0-opt/xgboost/2.1.1-xijqyj/lib \
    $(root-config --libs)
```
⚠️ For now, I have not find a better solution than to manually add the XGBoost path, meaning if a new version of key4hep releases you will probably need to adapt this.

This will:
- Create the shared library `libBDTScorer.so` that your hismaker will use to apply the BDT model.
- Create the function `computeBDTScores` that can be used in `histmaker.py`.
---

### 4. Plotting & performance checks
You can now:
- Apply the BDT score optimal cut in `histmaker.py` using `computeBDTScores`.
- Run `histmaker.py` with your newly defined objects.
⚠️ You also need to manually add the XGBoost path in key4hep in the `histmaker.py`, same as before check your the release you use.
---
