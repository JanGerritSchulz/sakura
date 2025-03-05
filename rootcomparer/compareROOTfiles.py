# import packages
import uproot
import numpy as np

# ------------------------------------------------------------------------------------------
# main function for comparing two root files
# ------------------------------------------------------------------------------------------

def compareROOTfiles(ROOTfile1, ROOTfile2, folder=None, tolerance=1e-5):
    """
    Compare two ROOT files and returns which histograms differ.
    
    :param ROOTfile1: Path to first ROOT file
    :param ROOTfile2: Path to second ROOT file
    :param tolerance: tolerance for the comparison
    """
    with uproot.open(ROOTfile1) as f1, uproot.open(ROOTfile2) as f2:
        keys1 = set(f1.keys())
        keys2 = set(f2.keys())

        keys1 = {t for t in keys1 if ("=" not in t)}
        keys2 = {t for t in keys2 if ("=" not in t)}
        
        # Check the structures
        if keys1 != keys2:
            print("\n\nWARNING: Different structures in the files!")
            print("  -> only in file 1:", keys1 - keys2)
            print("  -> only in file 2:", keys2 - keys1)
            print("\nIgnore those paths in comparison...")
        
        differing_histos = []
        
        commonKeys = keys1.intersection(keys2)
        if folder is not None:
            commonKeys = {t for t in commonKeys if (folder in t)}

        NTH1compared = [0,0]
        NTH2compared = [0,0]
        NProfilecompared = [0,0]
        for key in commonKeys:
            obj1 = f1[key]
            obj2 = f2[key]
            
            if isinstance(obj1, uproot.behaviors.TH1.TH1) and isinstance(obj2, uproot.behaviors.TH1.TH1):
                bins1 = obj1.to_numpy()
                bins2 = obj2.to_numpy()
                
                if not np.allclose(bins1[0], bins2[0], atol=tolerance):
                    differing_histos.append(key)
                else:
                    NTH1compared[0] += 1
                
                NTH1compared[1] += 1
            
            elif isinstance(obj1, uproot.behaviors.TH2.TH2) and isinstance(obj2, uproot.behaviors.TH2.TH2):
                bins1 = obj1.to_numpy()
                bins2 = obj2.to_numpy()
                
                if not np.allclose(bins1[0], bins2[0], atol=tolerance):
                    differing_histos.append(key)
                else:
                    NTH2compared[0] += 1
                
                NTH2compared[1] += 1
            
            elif isinstance(obj1, uproot.behaviors.TProfile.TProfile) and isinstance(obj2, uproot.behaviors.TProfile.TProfile):
                bins1 = obj1.values()
                bins2 = obj2.values()
                err1 = obj1.errors()
                err2 = obj2.errors()
                
                if not np.allclose(bins1, bins2, atol=tolerance) or not np.allclose(err1, err2, atol=tolerance):
                    differing_histos.append(key)
                else:
                    NProfilecompared[0] += 1
                
                NProfilecompared[1] += 1
        

        if differing_histos:
            print("\n\nThe following histograms differ:")
            for histo in differing_histos:
                print(" ->", histo)
            test = "FAILED"
        else:
            print("\n\nAll histograms identical.")
            test = "PASSED"
        
        print("\n /************************************************/")
        print(  " /*  %4i / %4i compared TH1 histograms passed  */" % tuple(NTH1compared))
        print(  " /*  %4i / %4i compared TH2 histograms passed  */" % tuple(NTH2compared))
        print(  " /*  %4i / %4i compared TProfiles passed       */" % tuple(NProfilecompared))
        print(  " /*                                              */")
        print(  " /*                 TEST %s                  */" % test)
        print(  " /************************************************/\n")
    

# ------------------------------------------------------------------------------------------

#########################################################################################
# For usage from command line
#########################################################################################

import argparse
parser = argparse.ArgumentParser(description="Produce cut distribution plots for SimDoublets including total and passing doublets + cut value.")
parser.add_argument("DQMfile1", type=str, help="Path to the first ROOT DQM input file")
parser.add_argument("DQMfile2", type=str, help="Path to the second ROOT DQM input file")
parser.add_argument("-f", "--folder", default="DQMData/Run 1/Tracking/Run summary/TrackingMCTruth/SimDoublets", type=str, help="Folder to check (default is SimDoublets folder)")
parser.add_argument("-t", "--tolerance", default=1e-5, type=float, help="Tolerance for comparison of values (default is 1e-5)")
def main():
    print("="*30)
    print("  Start compareROOTfiles()")
    print("="*30)

    args = parser.parse_args()

    print("Compare the following two ROOT files:")
    print(" * DQM file 1:", args.DQMfile1)
    print(" * DQM file 2:", args.DQMfile2)
    print("\nAdditional settings:")
    print(" * folder to be compared:", args.folder)
    print(" * accepted tolerance when comparing:", args.tolerance)
   
    # produce the plots
    compareROOTfiles(args.DQMfile1, args.DQMfile2, folder=args.folder, tolerance=args.tolerance)

    print("="*30)
    print("  End compareROOTfiles()")
    print("="*30)

if __name__ == "__main__":
    main()