import os

if __name__ == '__main__':
    for lhe_file in os.scandir('MG5_aMCatNLO/'):
        if not lhe_file.name.endswith(".lhe"): continue
        name = lhe_file.name[:lhe_file.name.rfind("_")]
        number = int(lhe_file.name[lhe_file.name.rfind("_")+1:lhe_file.name.rfind(".lhe")])
        print(f"{f' Running detector simulation for {lhe_file.name} ':+^100}")

        with open("cards/p8_lhereader.cmd", "r") as f:
            with open("cards/p8_lhereader_run.cmd", "w") as nf:
                nf.write(f.read().replace("LHE_FILE", lhe_file.name))

        os.system(f"mkdir -p gen/{name}")

        if os.path.exists(f"gen/{name}/events_{number}.root"): 
            print(f"File gen/{name}/events_{number}.root already exists, skipping...")
            continue

        os.system(f"DelphesPythia8_EDM4HEP cards/card_IDEA.tcl cards/edm4hep_IDEA.tcl cards/p8_lhereader_run.cmd gen/{name}/events_{number}.root")
