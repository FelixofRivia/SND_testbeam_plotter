import csv
import os
import random
import datetime
import ROOT

def read_csv_file(file_path):
    """Read the contents of a CSV file and return the data as a list of lists."""
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        run_data = [row for row in csvreader]
    return run_data

def return_GeV(run_data, run_n):    
    for row in run_data:
        if (row[0] == str(run_n)):
            return int(row[2])
    return -1

def return_Walls(run_data, run_n):    
    for row in run_data:
        if (row[0] == str(run_n)):
            return int(row[1])
    return -1

def generate_csv(file_path, folder_path, run_data):
    # Define header
    header = ["GeV", "Walls", "Run_number", "Date", "Output_file"]

    # Get a list of files in the specified folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Generate data for each file
    data = []
    for file_name in files:
        # Find the index of the underscore and period
        underscore_index = file_name.rfind("_")
        period_index = file_name.rfind(".")

        # Extract the text between the underscore and period
        run = int(file_name[underscore_index + 1 : period_index])

        # root_file = ROOT.TFile.Open("output_analysis/" + file_name)
        # num_no_cut = root_file.Get("NoCut_ShowerStart_with_clusters").GetEntries()
        # num_cut = root_file.Get("Cut_ShowerStart_with_clusters").GetEntries()
        # root_file.Close()

        modification_time = os.path.getmtime("output_analysis/" + file_name)
        formatted_modification_time = datetime.datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M')

        row = [           
            return_GeV(run_data, run),      # GeV
            return_Walls(run_data, run),    #Walls
            run,  # Run_number
            formatted_modification_time,  # Date
            file_name  # Output_file
        ]
        data.append(row)
    # Sort based on energy
    data = sorted(data, key=lambda x: x[0])
    # Write to CSV file
    with open(file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerows(data)

def plot_shower_start(folder_path, run_data):
    start_dict = {
    1: 'Skip',
    2: 'No_shower',
    5: 'Station_2',
    6: 'Station_3',
    7: 'Station_4'
    }
    energies = [100,140,180,240,300]
    counters_3w = [0,0,0,0,0]
    counters_1w = [0,0,0,0,0]
    colors = [ROOT.kRed,ROOT.kGreen,ROOT.kBlue,ROOT.kMagenta,ROOT.kCyan,ROOT.kOrange,ROOT.kSpring,ROOT.kTeal,ROOT.kViolet,ROOT.kYellow]
    # Create 5 canvases
    num_canvases = len(energies)
    canvases_3w = [ROOT.TCanvas(f"{energies[i]}_GeV_3W_BOCut", f"{energies[i]}_GeV_3W_BOCut") for i in range(num_canvases)] + [ROOT.TCanvas(f"{energies[i]}_GeV_3W_GuilCut", f"{energies[i]}_GeV_3W_GuilCut") for i in range(num_canvases)]
    canvases_full_3w = [ROOT.TCanvas(f"{energies[i]}_GeV_3W_full_BOCut", f"{energies[i]}_GeV_3W_full_BOCut") for i in range(num_canvases)] + [ROOT.TCanvas(f"{energies[i]}_GeV_3W_full_GuilCut", f"{energies[i]}_GeV_3W_full") for i in range(num_canvases)]
    canvases_1w = [ROOT.TCanvas(f"{energies[i]}_GeV_1W_BOCut", f"{energies[i]}_GeV_1W_BOCut") for i in range(num_canvases)] + [ROOT.TCanvas(f"{energies[i]}_GeV_1W_GuilCut", f"{energies[i]}_GeV_1W_GuilCut") for i in range(num_canvases)]
    canvases_full_1w = [ROOT.TCanvas(f"{energies[i]}_GeV_1W_full_BOCut", f"{energies[i]}_GeV_1W_full_BOCut") for i in range(num_canvases)] + [ROOT.TCanvas(f"{energies[i]}_GeV_1W_full_GuilCut", f"{energies[i]}_GeV_1W_full") for i in range(num_canvases)]
    legends_3w = [ROOT.TLegend(0.1, 0.7, 0.3, 0.9) for i in range(num_canvases)]
    legends_1w = [ROOT.TLegend(0.1, 0.7, 0.3, 0.9) for i in range(num_canvases)]

    for i in range(2*num_canvases):
        canvases_3w[i].Divide(3,1)
        canvases_full_3w[i].Divide(3,1)

    # Get a list of files in the specified folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    d2_canvases = [ROOT.TCanvas(file_name, file_name) for file_name in files]
    comp_canvases = [ROOT.TCanvas("comp_" + file_name,"comp_" + file_name) for file_name in files]

    for i in range(len(d2_canvases)):
        d2_canvases[i].Divide(3,1)

    for file_name in files:
        # Find the index of the underscore and period
        underscore_index = file_name.rfind("_")
        period_index = file_name.rfind(".")

        # Extract the text between the underscore and period
        run = int(file_name[underscore_index + 1 : period_index])
        gev = return_GeV(run_data, run)
        wall = return_Walls(run_data, run)
        index = energies.index(gev)

        if (wall == 3):

            root_file = ROOT.TFile.Open("output_analysis/" + file_name)
            root_file.cd()

            h1_f = root_file.Get("Cut_ShowerStart_with_clusters")
            h1_f.Scale(1.0 / h1_f.Integral())
            h1_f.SetLineColor(colors[counters_3w[index]%len(colors)])
            h1_f.GetYaxis().SetTitle("Fraction of showers")
            legends_3w[index].AddEntry(h1_f, f"r_{run}", "f")
            legends_3w[index].SetFillStyle(0)
            legends_3w[index].SetBorderSize(0)
            legends_3w[index].SetTextSize(0.015)

            h2_f = root_file.Get("Cut_ShowerStart_with_density")
            h2_f.Scale(1.0 / h2_f.Integral())
            h2_f.SetLineColor(colors[counters_3w[index]%len(colors)])
            h2_f.GetYaxis().SetTitle("Fraction of showers")
            
            h3_f = root_file.Get("Cut_ShowerStart_with_F")
            h3_f.Scale(1.0 / h3_f.Integral())
            h3_f.SetLineColor(colors[counters_3w[index]%len(colors)])
            h3_f.GetYaxis().SetTitle("Fraction of showers")

            option = "hist colz NOSTATS" if counters_3w[index] == 0 else "hist colz same NOSTATS"
            canvases_full_3w[index].cd(1)
            h1_f.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()
            canvases_full_3w[index].cd(2)
            h2_f.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()
            canvases_full_3w[index].cd(3)
            h3_f.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()

            h1 = h1_f
            h1.SetAxisRange(0.5,4.5,"X")
            h1.Scale(1.0 / h1.Integral())
            h1.SetLineColor(colors[counters_3w[index]%len(colors)])
            h1.GetYaxis().SetTitle("Fraction of showers")

            h2 = h2_f
            h2.SetAxisRange(0.5,4.5,"X")
            h2.Scale(1.0 / h2.Integral())
            h2.SetLineColor(colors[counters_3w[index]%len(colors)])
            h2.GetYaxis().SetTitle("Fraction of showers")

            h3 = h3_f
            h3.SetAxisRange(0.5,4.5,"X")
            h3.Scale(1.0 / h3.Integral())
            h3.SetLineColor(colors[counters_3w[index]%len(colors)])
            h3.GetYaxis().SetTitle("Fraction of showers")

            canvases_3w[index].cd(1)
            h1.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()
            canvases_3w[index].cd(2)
            h2.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()
            canvases_3w[index].cd(3)
            h3.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()

            ROOT.gPad.Modified()
            ROOT.gPad.Update()

            h4_f = root_file.Get("GuilCut_ShowerStart_with_clusters")
            h4_f.Scale(1.0 / h4_f.Integral())
            h4_f.SetLineColor(colors[counters_3w[index]%len(colors)])
            h4_f.GetYaxis().SetTitle("Fraction of showers")

            h5_f = root_file.Get("GuilCut_ShowerStart_with_density")
            h5_f.Scale(1.0 / h5_f.Integral())
            h5_f.SetLineColor(colors[counters_3w[index]%len(colors)])
            h5_f.GetYaxis().SetTitle("Fraction of showers")
            
            h6_f = root_file.Get("GuilCut_ShowerStart_with_F")
            h6_f.Scale(1.0 / h6_f.Integral())
            h6_f.SetLineColor(colors[counters_3w[index]%len(colors)])
            h6_f.GetYaxis().SetTitle("Fraction of showers")

            option = "hist colz NOSTATS" if counters_3w[index] == 0 else "hist colz same NOSTATS"
            canvases_full_3w[index + num_canvases].cd(1)
            h4_f.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()
            canvases_full_3w[index + num_canvases].cd(2)
            h5_f.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()
            canvases_full_3w[index + num_canvases].cd(3)
            h6_f.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()

            h4 = h4_f
            h4.SetAxisRange(0.5,4.5,"X")
            h4.Scale(1.0 / h4.Integral())
            h4.SetLineColor(colors[counters_3w[index]%len(colors)])
            h4.GetYaxis().SetTitle("Fraction of showers")

            h5 = h5_f
            h5.SetAxisRange(0.5,4.5,"X")
            h5.Scale(1.0 / h5.Integral())
            h5.SetLineColor(colors[counters_3w[index]%len(colors)])
            h5.GetYaxis().SetTitle("Fraction of showers")

            h6 = h6_f
            h6.SetAxisRange(0.5,4.5,"X")
            h6.Scale(1.0 / h6.Integral())
            h6.SetLineColor(colors[counters_3w[index]%len(colors)])
            h6.GetYaxis().SetTitle("Fraction of showers")

            canvases_3w[index + num_canvases].cd(1)
            h4.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()
            canvases_3w[index + num_canvases].cd(2)
            h5.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()
            canvases_3w[index + num_canvases].cd(3)
            h6.DrawCopy(option)
            if counters_3w[index] == 0: legends_3w[index].Draw()

            ROOT.gPad.Modified()
            ROOT.gPad.Update()

            root_file.Close()
            counters_3w[index] += 1

        elif (wall == 1):

            root_file = ROOT.TFile.Open("output_analysis/" + file_name)
            root_file.cd()

            h1_f = root_file.Get("Cut_ShowerStart_with_clusters")
            h1_f.Scale(1.0 / h1_f.Integral())
            h1_f.SetLineColor(colors[counters_1w[index]%len(colors)])
            h1_f.GetYaxis().SetTitle("Fraction of showers")
            legends_1w[index].AddEntry(h1_f, f"r_{run}", "f")
            legends_1w[index].SetFillStyle(0)
            legends_1w[index].SetBorderSize(0)
            legends_1w[index].SetTextSize(0.015)

            h2_f = root_file.Get("Cut_ShowerStart_with_density")
            h2_f.Scale(1.0 / h2_f.Integral())
            h2_f.SetLineColor(colors[counters_1w[index]%len(colors)])
            h2_f.GetYaxis().SetTitle("Fraction of showers")
            
            h3_f = root_file.Get("Cut_ShowerStart_with_F")
            h3_f.Scale(1.0 / h3_f.Integral())
            h3_f.SetLineColor(colors[counters_1w[index]%len(colors)])
            h3_f.GetYaxis().SetTitle("Fraction of showers")

            option = "hist colz NOSTATS" if counters_1w[index] == 0 else "hist colz same NOSTATS"
            canvases_full_1w[index].cd(1)
            h1_f.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()
            canvases_full_1w[index].cd(2)
            h2_f.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()
            canvases_full_1w[index].cd(3)
            h3_f.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()

            h1 = h1_f
            h1.SetAxisRange(0.5,4.5,"X")
            h1.Scale(1.0 / h1.Integral())
            h1.SetLineColor(colors[counters_1w[index]%len(colors)])
            h1.GetYaxis().SetTitle("Fraction of showers")

            h2 = h2_f
            h2.SetAxisRange(0.5,4.5,"X")
            h2.Scale(1.0 / h2.Integral())
            h2.SetLineColor(colors[counters_1w[index]%len(colors)])
            h2.GetYaxis().SetTitle("Fraction of showers")

            h3 = h3_f
            h3.SetAxisRange(0.5,4.5,"X")
            h3.Scale(1.0 / h3.Integral())
            h3.SetLineColor(colors[counters_1w[index]%len(colors)])
            h3.GetYaxis().SetTitle("Fraction of showers")

            canvases_1w[index].cd(1)
            h1.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()
            canvases_1w[index].cd(2)
            h2.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()
            canvases_1w[index].cd(3)
            h3.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()

            ROOT.gPad.Modified()
            ROOT.gPad.Update()

            h4_f = root_file.Get("GuilCut_ShowerStart_with_clusters")
            h4_f.Scale(1.0 / h4_f.Integral())
            h4_f.SetLineColor(colors[counters_1w[index]%len(colors)])
            h4_f.GetYaxis().SetTitle("Fraction of showers")

            h5_f = root_file.Get("GuilCut_ShowerStart_with_density")
            h5_f.Scale(1.0 / h5_f.Integral())
            h5_f.SetLineColor(colors[counters_1w[index]%len(colors)])
            h5_f.GetYaxis().SetTitle("Fraction of showers")
            
            h6_f = root_file.Get("GuilCut_ShowerStart_with_F")
            h6_f.Scale(1.0 / h6_f.Integral())
            h6_f.SetLineColor(colors[counters_1w[index]%len(colors)])
            h6_f.GetYaxis().SetTitle("Fraction of showers")

            option = "hist colz NOSTATS" if counters_1w[index] == 0 else "hist colz same NOSTATS"
            canvases_full_1w[index + num_canvases].cd(1)
            h4_f.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()
            canvases_full_1w[index + num_canvases].cd(2)
            h5_f.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()
            canvases_full_1w[index + num_canvases].cd(3)
            h6_f.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()

            h4 = h4_f
            h4.SetAxisRange(0.5,4.5,"X")
            h4.Scale(1.0 / h4.Integral())
            h4.SetLineColor(colors[counters_1w[index]%len(colors)])
            h4.GetYaxis().SetTitle("Fraction of showers")

            h5 = h5_f
            h5.SetAxisRange(0.5,4.5,"X")
            h5.Scale(1.0 / h5.Integral())
            h5.SetLineColor(colors[counters_1w[index]%len(colors)])
            h5.GetYaxis().SetTitle("Fraction of showers")

            h6 = h6_f
            h6.SetAxisRange(0.5,4.5,"X")
            h6.Scale(1.0 / h6.Integral())
            h6.SetLineColor(colors[counters_1w[index]%len(colors)])
            h6.GetYaxis().SetTitle("Fraction of showers")

            canvases_1w[index + num_canvases].cd(1)
            h4.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()
            canvases_1w[index + num_canvases].cd(2)
            h5.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()
            canvases_1w[index + num_canvases].cd(3)
            h6.DrawCopy(option)
            if counters_1w[index] == 0: legends_1w[index].Draw()

            ROOT.gPad.Modified()
            ROOT.gPad.Update()

            root_file.Close()
            counters_1w[index] += 1

    output_file = ROOT.TFile("start_of_shower.root", "RECREATE")

    for n in range(2*num_canvases):
        ROOT.gPad.Modified()
        ROOT.gPad.Update()
        canvases_full_3w[n].cd(0)
        canvases_full_3w[n].Write()
        canvases_3w[n].cd(0)
        canvases_3w[n].Write()
        canvases_full_1w[n].cd(0)
        canvases_full_1w[n].Write()
        canvases_1w[n].cd(0)
        canvases_1w[n].Write()
        
    for n,file_name in enumerate(files):
        # Find the index of the underscore and period
        underscore_index = file_name.rfind("_")
        period_index = file_name.rfind(".")

        # Extract the text between the underscore and period
        run = int(file_name[underscore_index + 1 : period_index])
        gev = return_GeV(run_data, run)

        h_cluster = ROOT.TH2F(f"Clusters_{run}_{gev}_GeV", f"Clusters_{run}_{gev}_GeV; BO_cut; Guil_cut", 5, 0, 5, 5, 0, 5)
        for i, (key, value) in enumerate(start_dict.items()):
            h_cluster.GetXaxis().SetBinLabel(i+1, value)
            h_cluster.GetYaxis().SetBinLabel(i+1, value)

        h_density = ROOT.TH2F(f"Density_{run}_{gev}_GeV", f"Density_{run}_{gev}_GeV; BO_cut; Guil_cut", 5, 0, 5, 5, 0, 5)
        for i, (key, value) in enumerate(start_dict.items()):
            h_density.GetXaxis().SetBinLabel(i+1, value)
            h_density.GetYaxis().SetBinLabel(i+1, value)

        h_F = ROOT.TH2F(f"F_{run}_{gev}_GeV", f"F_{run}_{gev}_GeV; BO_cut; Guil_cut", 5, 0, 5, 5, 0, 5)
        for i, (key, value) in enumerate(start_dict.items()):
            h_F.GetXaxis().SetBinLabel(i+1, value)
            h_F.GetYaxis().SetBinLabel(i+1, value)

        h_comp = ROOT.TH2F(f"Guil_cut_{run}_{gev}_GeV", f"Guil_cut_{run}_{gev}_GeV; Density; F", 5, 0, 5, 5, 0, 5)
        for i, (key, value) in enumerate(start_dict.items()):
            h_comp.GetXaxis().SetBinLabel(i+1, value)
            h_comp.GetYaxis().SetBinLabel(i+1, value)

        root_file = ROOT.TFile.Open("output_analysis/" + file_name)
        root_file.cd()

        h_dummy = root_file.Get("Cut_clusters_vs_GuilCut_clusters")
        for i in range(1, h_dummy.GetNbinsX() + 1):
            for j in range(1, h_dummy.GetNbinsY() + 1):
                if (i in start_dict and j in start_dict):
                    bin_content = h_dummy.GetBinContent(i, j)
                    h_cluster.Fill(start_dict[i],start_dict[j],bin_content)

        h_dummy = root_file.Get("Cut_density_vs_GuilCut_density")
        for i in range(1, h_dummy.GetNbinsX() + 1):
            for j in range(1, h_dummy.GetNbinsY() + 1):
                if (i in start_dict and j in start_dict):
                    bin_content = h_dummy.GetBinContent(i, j)
                    h_density.Fill(start_dict[i],start_dict[j],bin_content)

        h_dummy = root_file.Get("Cut_F_vs_GuilCut_F")
        for i in range(1, h_dummy.GetNbinsX() + 1):
            for j in range(1, h_dummy.GetNbinsY() + 1):
                if (i in start_dict and j in start_dict):
                    bin_content = h_dummy.GetBinContent(i, j)
                    h_F.Fill(start_dict[i],start_dict[j],bin_content)

        h_dummy = root_file.Get("GuilCut_density_vs_GuilCut_F")
        for i in range(1, h_dummy.GetNbinsX() + 1):
            for j in range(1, h_dummy.GetNbinsY() + 1):
                if (i in start_dict and j in start_dict):
                    bin_content = h_dummy.GetBinContent(i, j)
                    h_comp.Fill(start_dict[i],start_dict[j],bin_content)

        option = "colz NOSTATS"
        d2_canvases[n].cd(1)
        h_cluster.SetMinimum(1)
        h_cluster.DrawCopy(option)
        ROOT.gPad.SetLogz()
        d2_canvases[n].cd(2)
        h_density.SetMinimum(1)
        h_density.DrawCopy(option)
        ROOT.gPad.SetLogz()
        d2_canvases[n].cd(3)
        h_F.SetMinimum(1)
        h_F.DrawCopy(option)
        ROOT.gPad.SetLogz()
        comp_canvases[n].cd()
        h_comp.SetMinimum(1)
        h_comp.DrawCopy(option)
        ROOT.gPad.SetLogz()

        ROOT.gPad.Modified()
        ROOT.gPad.Update()

        root_file.Close()

    output_file.cd()

    for n in range(len(d2_canvases)):
        ROOT.gPad.Modified()
        ROOT.gPad.Update()
        d2_canvases[n].cd(0)
        d2_canvases[n].Write()
        comp_canvases[n].Write()

    output_file.Close()


if __name__ == "__main__":
    folder_path = "output_analysis"
    output_csv_path = "data.csv"

    # Generate CSV based on files in the output_analysis folder
    generate_csv(output_csv_path, folder_path, read_csv_file("TB_runs.csv"))
    print(f"CSV file '{output_csv_path}' generated successfully.")

    # Plot superimposed histograms for start of shower
    plot_shower_start(folder_path, read_csv_file("TB_runs.csv"))
    print(f"File 'start_of_shower.root' generated successfully.")