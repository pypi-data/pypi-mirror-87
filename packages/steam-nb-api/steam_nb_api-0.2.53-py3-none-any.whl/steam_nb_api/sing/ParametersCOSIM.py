import os
import json
import pandas as pd
import numpy as np
import shutil

from steam_nb_api.resources.ResourceReader import ResourceReader
from steam_nb_api.utils.misc import makeCopyFile
from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET

class ParametersCOSIM:
    '''
        Class of COSIM parameters to generate automatically the COSIM folder and file structure
    '''

    def __init__(self, nameFolderCosimModel: str, nameCircuit: str = "", nameMagnet: str = ""):
        '''

        :param nameFolderCosimModel: String defining the name of the folder where the COSIM model will be saved
        :type nameFolderCosimModel: str
        :param nameCircuit: string defining the circuit name; at the moment, this is just a label
        :type nameCircuit: str

        '''

        self.nameFolderCosimModel = nameFolderCosimModel
        if nameCircuit == "":
            print("No Circuit-Name defined. Setting to _0")
            self.circuitName = "_0"
        if nameMagnet == "":
            print("No Magnet-Name defined. Setting to _0")
            self.nameMagnet = "_0"
        self.circuitName = nameCircuit
        self.nameMagnet = nameMagnet

        # Load and set the default config files (using ResourceReader allows reading from a "hidden" resource folder)
        self.nameTemplateConfigFileCosim = ResourceReader.getResourcePath(os.path.join('sing', 'STEAMConfig.json'))
        self.nameTemplateConfigFilePSpice = ResourceReader.getResourcePath(os.path.join('sing', 'PSpiceConfig.json'))
        self.nameTemplateConfigFileLedet = ResourceReader.getResourcePath(os.path.join('sing', 'LedetConfig.json'))

    def makeAllFolders(self, N_LEDET = 1):
        '''
            **Makes a COSIM folder with the required PSPICE and LEDET subfolders**

            Function to generate all the required subfolders and files for a COSIM model

            :return: None
        '''

        nameFolderCosimModel = self.nameFolderCosimModel

        # Make COSIM folder
        if not os.path.exists(nameFolderCosimModel):
            os.makedirs(nameFolderCosimModel)

        # Make SPICE model folder
        pathFolderPSpice = os.path.join(nameFolderCosimModel, 'PSpice')
        if not os.path.exists(pathFolderPSpice):
            os.makedirs(pathFolderPSpice)

        # Make LEDET model folder and sub-folders
        if N_LEDET == 1:
            nameFolderLedetModel = os.path.join(nameFolderCosimModel, 'LEDET')
            if not os.path.isdir(nameFolderLedetModel):
                os.mkdir(nameFolderLedetModel)
            if not os.path.isdir(os.path.join(nameFolderLedetModel, 'LEDET')):
                os.mkdir(os.path.join(nameFolderLedetModel, 'LEDET'))
            if not os.path.isdir(os.path.join(nameFolderLedetModel, 'LEDET//'+ self.nameMagnet+"//")):
                os.mkdir(os.path.join(nameFolderLedetModel, 'LEDET//'+ self.nameMagnet+"//"))
            if not os.path.isdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet + "//Input//"):
                os.mkdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet + "//Input//")
            if not os.path.isdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet + "//Input//Initialize variables//"):
                os.mkdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet + "//Input//Initialize variables//")
            if not os.path.isdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet + "//Input//Control current input//"):
                os.mkdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet + "//Input//Control current input//")
            if not os.path.isdir(nameFolderLedetModel + "//Field maps//"):
                os.mkdir(nameFolderLedetModel + "//Field maps//")
            if not os.path.isdir(nameFolderLedetModel + "//Field maps//" + self.nameMagnet):
                os.mkdir(nameFolderLedetModel + "//Field maps//" + self.nameMagnet)
            if not os.path.isdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet + "//Output//"):
                os.mkdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet + "//Output//")

        if N_LEDET > 1:
            for i in range(1, N_LEDET+1):
                # Make LEDET model folder and sub-folders
                nameFolderLedetModel = os.path.join(nameFolderCosimModel, 'LEDET_'+ str(i))
                if not os.path.isdir(nameFolderLedetModel):
                    os.mkdir(nameFolderLedetModel)
                if not os.path.isdir(os.path.join(nameFolderLedetModel, 'LEDET')):
                    os.mkdir(os.path.join(nameFolderLedetModel, 'LEDET'))
                if not os.path.isdir(os.path.join(nameFolderLedetModel, 'LEDET//' + self.nameMagnet[i-1] + "//")):
                    os.mkdir(os.path.join(nameFolderLedetModel, 'LEDET//' + self.nameMagnet[i-1] + "//"))
                if not os.path.isdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet[i-1] + "//Input//"):
                    os.mkdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet[i-1] + "//Input//")
                if not os.path.isdir(
                        nameFolderLedetModel + "//LEDET//" + self.nameMagnet[i-1] + "//Input//Initialize variables//"):
                    os.mkdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet[i-1] + "//Input//Initialize variables//")
                if not os.path.isdir(
                        nameFolderLedetModel + "//LEDET//" + self.nameMagnet[i-1] + "//Input//Control current input//"):
                    os.mkdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet[i-1] + "//Input//Control current input//")
                if not os.path.isdir(nameFolderLedetModel + "//Field maps//"):
                    os.mkdir(nameFolderLedetModel + "//Field maps//")
                if not os.path.isdir(nameFolderLedetModel + "//Field maps//" + self.nameMagnet[i-1]):
                    os.mkdir(nameFolderLedetModel + "//Field maps//" + self.nameMagnet[i-1])
                if not os.path.isdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet[i-1] + "//Output//"):
                    os.mkdir(nameFolderLedetModel + "//LEDET//" + self.nameMagnet[i-1] + "//Output//")

    def copyConfigFiles(self, N_LEDET = 1):
        '''
            **Makes the configuration files required to run a COSIM model with one PSPICE and one LEDET models **

            Function to generate the configuration files for COSIM, one PSPICE, and one LEDET models

            :return: None
        '''

        nameFolderCosimModel = self.nameFolderCosimModel
        nameTemplateConfigFileCosim = self.nameTemplateConfigFileCosim
        nameTemplateConfigFilePSpice = self.nameTemplateConfigFilePSpice
        nameTemplateConfigFileLedet = self.nameTemplateConfigFileLedet

        # Check that the folder exists; if not, generate all required folders and subfolders
        if not os.path.exists(nameFolderCosimModel):
            self.makeAllFolders(N_LEDET = N_LEDET)

        # Copy template COSIM config file
        makeCopyFile(nameTemplateConfigFileCosim, os.path.join(nameFolderCosimModel, 'STEAMConfig.json'))

        # Copy template PSpice config file
        makeCopyFile(nameTemplateConfigFilePSpice, os.path.join(nameFolderCosimModel, 'PSpice', 'PSpiceConfig.json'))

        if N_LEDET == 1:
            # Copy template LEDET config file
            makeCopyFile(nameTemplateConfigFileLedet, os.path.join(nameFolderCosimModel, 'LEDET', 'LedetConfig.json'))
        else:
            for i in range(1, N_LEDET+1):
                makeCopyFile(nameTemplateConfigFileLedet,
                             os.path.join(nameFolderCosimModel, 'LEDET_'+ str(i), 'LedetConfig.json'))

    def copyIOPortFiles(self, fileName_IOPortDefinition: str, fileName_complementaryIOPortDefinition: str, N_LEDET = 1):
        '''
            **Copies the input/output port files required to run a COSIM model with one PSPICE and one LEDET models **

            Function to copy the I/O Port files in the correct subfolders

            :return: None
        '''

        nameFolderCosimModel = self.nameFolderCosimModel

        # Check that the required input files exist
        if not os.path.isfile(fileName_IOPortDefinition):
            raise Exception('Input file fileName_IOPortDefinition = {} not found!'.format(fileName_IOPortDefinition))
        if not os.path.isfile(fileName_complementaryIOPortDefinition):
            raise Exception(
                'Input file fileName_IOPortDefinition = {} not found!'.format(fileName_complementaryIOPortDefinition))

        # Check that the folder exists; if not, generate all required folders and subfolders
        if not os.path.exists(nameFolderCosimModel):
            self.makeAllFolders()

        # Copy PSPICE IOPort file
        makeCopyFile(fileName_IOPortDefinition,
                     os.path.join(nameFolderCosimModel, 'PSpice', 'PspiceInputOutputPortDefinition.json'))

        # Copy LEDET IOPort file
        if N_LEDET == 1:
            makeCopyFile(fileName_complementaryIOPortDefinition,
                         os.path.join(nameFolderCosimModel, 'LEDET', 'LedetInputOutputPortDefinition.json'))
        else:
            for i in range(N_LEDET):
                makeCopyFile(fileName_complementaryIOPortDefinition,
                             os.path.join(nameFolderCosimModel, 'LEDET'+str(i), 'LedetInputOutputPortDefinition.json'))

    def makeGenericIOPortFiles(self, CoilSections, CurrentFolder, CoSimFolder: str, PSpiceExecutable: str, LEDETExecutable: str,
                               t_0 = [0, 2e-5], t_end = [2e-5, 0.5], t_step_max = [[1e-5, 1e-5], [1e-5, 1e-5]],
                               relTolerance = [1e-4, None], absTolerance = [1, None], executionOrder = [1, 2],
                               executeCleanRun = [True, True], N_LEDET = 1, QuenchMagnet = 0, SimulationNumber = [0], DistinctMagnets = 1, PSPICEinitialConditions = []):

        # Components which are used in the Ports
        Components = ["L", "CoilSections"]  # [0] = PSpice, [1]=LEDET
        # Setting the Coilsections
        CSections = []
        LSections = []
        for i in range(len(CoilSections)):
            CSectionsPerPort = []
            for j in range(len(CoilSections[i])):
                CSectionsPerPort.append(Components[1] + "_" + str(CoilSections[i][j]))
            CSections.append(CSectionsPerPort)
            LSections.append(Components[0] + "_" + str(i+1))

        # Variables used for convergence, for now its the first magnet current and the LEDET Voltages
        if N_LEDET == 1:
            convergenceVariables = ["I(x_mag_1." + Components[0] + "_1)", "U_inductive_dynamic_" + Components[1]+"_1"]
        else:
            convergenceVariables = ["I(x_mag_1." + Components[0] + "_1)", "U_inductive_dynamic_" + Components[1]+"_1"]
            for i in range(2,N_LEDET+1):
                convergenceVariables.append("U_inductive_dynamic_" + Components[1]+"_1")

        # couplingParameterLedet/PS- [x] = WholePort, ..[x][i] = in/out incl. Name and type, ...[x][i][0]=name,...[x][i][1]=type
        couplingParameterLedet = [[["I", ["TH", "EM"]]], [["R", ["TH"]], ["U", ["EM"]]]]
        couplingParameterPSpice = [[[["R", ["TH"]], ["U", ["EM"]]], [["I", ["TH", "EM"]]]],
                                    [[["U", ["EM"]]], [["U", ["EM"]]]]]

        # Building STEAM.config
        PSpiceFolder = CurrentFolder + "\\cosim_model_" + self.circuitName + "\\PSpice\\"
        if N_LEDET == 1:
            LedetFolder = CurrentFolder + "\\cosim_model_" + self.circuitName + "\\LEDET\\"
        else:
            LedetFolder = CurrentFolder + "\\cosim_model_" + self.circuitName + "\\LEDET_" + str(1)+ "\\"

        filename = self.nameFolderCosimModel + '//STEAMConfig.json'
        try:
            os.remove(filename)
        except:
            # print('Already cleaned')
            pass
        data = {"coSimulationDir": CoSimFolder}
        data["coSimulationModelSolvers"] = ["PSPICE", "LEDET"]
        data["coSimulationModelDirs"] = [PSpiceFolder, LedetFolder]
        data["coSimulationModelConfigs"] = ["PSpiceConfig.json", "LedetConfig.json"]
        data["coSimulationPortDefinitions"] = ["PSpiceInputOutputPortDefinition.json",
                                               "LedetInputOutputPortDefinition.json"]
        data["convergenceVariables"] = convergenceVariables
        data["t_0"] = t_0
        data["t_end"] = t_end
        data["t_step_max"] = t_step_max
        data["relTolerance"] = relTolerance
        data["absTolerance"] = absTolerance
        data["executionOrder"] = executionOrder
        data["executeCleanRun"] = executeCleanRun
        if N_LEDET >1:
            for i in range(2, N_LEDET+1):
                data["coSimulationModelSolvers"].append("LEDET")
                LedetFolder = CurrentFolder + "\\cosim_model_" + self.circuitName + "\\LEDET_" + str(i)+ "\\"
                data["coSimulationModelDirs"].append(LedetFolder)
                data["coSimulationModelConfigs"].append("LedetConfig.json")
                data["coSimulationPortDefinitions"].append("LedetInputOutputPortDefinition.json")

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        # Building PSpiceConfig
        filename = self.nameFolderCosimModel + '/PSpice/PSpiceConfig.json'
        with open(filename, 'r') as f:
            data = json.load(f)
            data["solverPath"] = PSpiceExecutable
            data["initialConditions"] = PSPICEinitialConditions

        try:
            os.remove(filename)
        except:
            #print('Already cleaned')
            pass
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        # Building LEDETConfig
        if N_LEDET == 1:
            filename = self.nameFolderCosimModel + '/LEDET/LedetConfig.json'
            with open(filename, 'r') as f:
                data = json.load(f)
                data["solverPath"] = LEDETExecutable
                data["modelName"] = self.nameMagnet
                data["simulationNumber"] = str(SimulationNumber[0])
            try:
                os.remove(filename)
            except:
                # print('Already cleaned')
                pass
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            if len(SimulationNumber) != N_LEDET:
                SimulationNumber = [0]*N_LEDET
                print("Simulation Number 0 is used for all LEDET models")
            for i in range(1,N_LEDET+1):
                filename = self.nameFolderCosimModel + '/LEDET_'+str(i)+'/LedetConfig.json'
                with open(filename, 'r') as f:
                    data = json.load(f)
                    if executionOrder.count(2) > 1:
                        idxLEDET = LEDETExecutable.find('LEDET')
                        data["solverPath"] = LEDETExecutable[0:idxLEDET + 5] + "_"+str(i) + LEDETExecutable[idxLEDET + 5:]
                        print('LEDET parallel solving, performed from: ', data["solverPath"])
                    else: data["solverPath"] = LEDETExecutable
                    data["modelName"] = self.nameMagnet[i-1]
                    data["simulationNumber"] = str(SimulationNumber[i-1])
                try:
                    os.remove(filename)
                except:
                    # print('Already cleaned')
                    pass
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)

        # LEDETInputPortDefinitions
        if N_LEDET == 1:
            filename = self.nameFolderCosimModel + '/LEDET/LedetInputOutputPortDefinition.json'
            try:
                os.remove(filename)
            except:
                # print('Already cleaned')
                pass

            struct_total = []
            for i in range(len(CoilSections)):  # Number of Ports
                struct = {}
                struct["name"] = "Port_" + str(i+1) + "_" + str(0)
                struct["components"] = []
                for n in range(len(CSections[i])):  # All Coilsections
                    struct["components"].append(CSections[i][n])
                struct["inputs"] = []
                for j in range(len(couplingParameterLedet[0])):  # Number of In's per respective Port
                    substruct_in = {}
                    substruct_in["couplingParameter"] = couplingParameterLedet[0][j][0]
                    substruct_in["labels"] = []
                    for n in range(len(CSections[i])):  # Append all Coilsections as Labels to Input
                        substruct_in["labels"].append(couplingParameterLedet[0][j][0] +"_" +  CSections[i][n])
                    substruct_in["types"] = couplingParameterLedet[0][j][1]
                    struct["inputs"].append(substruct_in)

                struct["outputs"] = []
                for k in range(len(couplingParameterLedet[1])):  # Number of Out's per respective Port
                    substruct_out = {}
                    substruct_out["couplingParameter"] = couplingParameterLedet[1][k][0]
                    substruct_out["labels"] = []
                    for n in range(len(CSections[i])):  # Append all Coilsections as Labels to Output
                        if (couplingParameterLedet[1][k][0] == "U"):  # If Output is U
                            substruct_out["labels"].append("U_inductive_dynamic" +"_" +  CSections[i][n])
                        else:  # If output is I or R
                            substruct_out["labels"].append(couplingParameterLedet[1][k][0] +"_" +  CSections[i][n])
                    substruct_out["types"] = couplingParameterLedet[1][k][1]
                    struct["outputs"].append(substruct_out)

                struct_total.append(struct)

            with open(filename, 'w') as f:
                for i in range(len(struct_total)):
                    json.dump(struct_total[i], f, indent=4)
                    f.write('\n')
        else:
            for l in range(0,N_LEDET):
                filename = self.nameFolderCosimModel + '/LEDET_'+str(l+1)+'/LedetInputOutputPortDefinition.json'
                try:
                    os.remove(filename)
                except:
                    # print('Already cleaned')
                    pass

                struct_total = []
                for i in range(len(CoilSections)):  # Number of Ports
                    struct = {}
                    struct["name"] = "Port_" + str(i+l*len(CoilSections)+1) + "_" + str(0)
                    struct["components"] = []
                    for n in range(len(CSections[i])):  # All Coilsections
                        struct["components"].append(CSections[i][n])
                    struct["inputs"] = []
                    for j in range(len(couplingParameterLedet[0])):  # Number of In's per respective Port
                        substruct_in = {}
                        substruct_in["couplingParameter"] = couplingParameterLedet[0][j][0]
                        substruct_in["labels"] = []
                        for n in range(len(CSections[i])):  # Append all Coilsections as Labels to Input
                            substruct_in["labels"].append(couplingParameterLedet[0][j][0] + "_" + CSections[i][n])
                        substruct_in["types"] = couplingParameterLedet[0][j][1]
                        struct["inputs"].append(substruct_in)

                    struct["outputs"] = []
                    for k in range(len(couplingParameterLedet[1])):  # Number of Out's per respective Port
                        substruct_out = {}
                        substruct_out["couplingParameter"] = couplingParameterLedet[1][k][0]
                        substruct_out["labels"] = []
                        for n in range(len(CSections[i])):  # Append all Coilsections as Labels to Output
                            if (couplingParameterLedet[1][k][0] == "U"):  # If Output is U
                                substruct_out["labels"].append("U_inductive_dynamic" + "_" + CSections[i][n])
                            else:  # If output is I or R
                                substruct_out["labels"].append(couplingParameterLedet[1][k][0] + "_" + CSections[i][n])
                        substruct_out["types"] = couplingParameterLedet[1][k][1]
                        struct["outputs"].append(substruct_out)

                    struct_total.append(struct)

                with open(filename, 'w') as f:
                    for i in range(len(struct_total)):
                        json.dump(struct_total[i], f, indent=4)
                        f.write('\n')

        # PSpice
        filename = self.nameFolderCosimModel + '/PSpice/PSpiceInputOutputPortDefinition.json'
        try:
            os.remove(filename)
        except:
            # print('Already cleaned')
            pass

        struct_total = []
        for n in range(0, N_LEDET):
            if n+1== QuenchMagnet and QuenchMagnet != 0:
                quench = '_Quench'
            else:
                quench = ''
            if DistinctMagnets != 1:
                DM = n+1
                M_add = "M"+str(DM)+'_'
            elif n == QuenchMagnet and QuenchMagnet != 0:
                DM = 1+QuenchMagnet
                M_add = ''
            else:
                DM = 1
                M_add = ''
            for i in range(len(CoilSections)):  # Number of Ports
                for j in range(2):  # 2Ports in PSpice
                    struct = {}
                    struct["name"] = "Port_" + str(i+n*len(CoilSections)+1) + "_" + str(j)
                    struct["components"] = [LSections[i]]
                    struct["inputs"] = []
                    for l in range(len(couplingParameterPSpice[j][0])):  # Number of In's
                        substruct_in = {}
                        substruct_in["couplingParameter"] = couplingParameterPSpice[j][0][l][0]
                        if (j == 0):  # Second Port in PSpice is U/U, check on that here
                            if (couplingParameterPSpice[j][0][l][0] == "U"):
                                cPPSpice = "V"
                            else:
                                cPPSpice = couplingParameterPSpice[j][0][l][0]
                            substruct_in["labels"] = [cPPSpice + "_field_"+M_add + str(i+1) + "_stim"+quench]  # First Port for Field
                        else:  # Second Port with circuit
                            substruct_in["labels"] = ["V_circuit_" +M_add+ str(i+1) + "_stim"+quench]
                        substruct_in["types"] = couplingParameterPSpice[j][0][l][1]
                        struct["inputs"].append(substruct_in)

                    struct["outputs"] = []
                    for k in range(len(couplingParameterPSpice[j][1])):  # Number of Out's
                        substruct_out = {}
                        substruct_out["couplingParameter"] = couplingParameterPSpice[j][1][k][0]
                        if (j == 0):  # Check again for outputs for which of the 2Ports for Pspice one is in
                            if (couplingParameterPSpice[j][1][k][0] == "U"):
                                cPPSpice = "V"
                            else:
                                cPPSpice = couplingParameterPSpice[j][1][k][0]
                            substruct_out["labels"] = [
                                cPPSpice + "(x_mag_" + str(DM)+ "." + Components[0] + "_" + str(i+1) + ")"]
                        else:
                            substruct_out["labels"] = ["V(x_mag_" + str(DM)+ "." + str(i+1) + "_v_l_diff)"]
                        substruct_out["types"] = couplingParameterPSpice[j][1][k][1]
                        struct["outputs"].append(substruct_out)

                    struct_total.append(struct)

        with open(filename, 'w') as f:
            for i in range(len(struct_total)):
                json.dump(struct_total[i], f, indent=4)
                f.write('\n')

    def FindLibPath(self, File):
        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        for i in range(5):
            if os.path.isdir(os.path.join(path,"steam-pspice-library")):
               return  os.path.join(path,File)
            else:
                path =  os.path.abspath(os.path.join(path, os.pardir))
        print("Could not find PSPICE library. Please add manually.")
        return False

    def copyCOSIMfiles(self, nameFileSING, StimulusFile, nameMagnet, N_LEDET=1, ManuallyStimulusFile = ''):

        LEDETFiles = os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)),os.pardir))
        LEDETFiles = os.path.join(LEDETFiles, "steam-ledet-input")
        nameFolderCosimModel = self.nameFolderCosimModel

        # Copy PSPICE model file
        if len(ManuallyStimulusFile) == 0:
            StimulusFile = self.FindLibPath(StimulusFile)
            if StimulusFile == False: return
        else:
            StimulusFile = ManuallyStimulusFile
        nameFolderPSpiceModel = os.path.join(nameFolderCosimModel, 'PSpice')
        if not os.path.isdir(nameFolderPSpiceModel):
            os.mkdir(nameFolderPSpiceModel)
        makeCopyFile(nameFileSING, os.path.join(nameFolderPSpiceModel, 'Circuit.cir'))
        makeCopyFile(StimulusFile, os.path.join(nameFolderPSpiceModel, 'ExternalStimulus.stl'))

        LEDET_Fs = []
        for i in range(N_LEDET):
            if N_LEDET > 1:
                nameFolderLedetModel = os.path.join(nameFolderCosimModel, 'LEDET_'+str(i+1))
                if len(nameMagnet)>1:
                    sourcedir = os.path.join(LEDETFiles, nameMagnet[i])
                    nM = nameMagnet[i]
                else:
                    sourcedir = os.path.join(LEDETFiles, nameMagnet)
                    nM = nameMagnet
            else:
                sourcedir = os.path.join(LEDETFiles, nameMagnet)
                nameFolderLedetModel = os.path.join(nameFolderCosimModel, 'LEDET')
                nM = nameMagnet
            sourcefiles = os.listdir(sourcedir)
            if not os.path.isdir(nameFolderLedetModel):
                os.mkdir(nameFolderLedetModel)
            destinationpath_field = nameFolderLedetModel + "//Field maps//" + nM
            destinationpath_para = nameFolderLedetModel + "//LEDET//" + nM + "//Input//"
            for file in sourcefiles:
                if file.endswith('.map2d') and not file.startswith(".sys"):
                    makeCopyFile(os.path.join(sourcedir, file), os.path.join(destinationpath_field, file))
                if file.endswith('.xlsx') and not file.startswith(".sys") and file.startswith(str(nM)):
                    shutil.copy(os.path.join(sourcedir, file), os.path.join(destinationpath_para, file))
                    LEDET_Fs.append(os.path.join(destinationpath_para, file))
                if file.endswith('_selfMutualInductanceMatrix.csv'):
                    shutil.copy(os.path.join(sourcedir, file), os.path.join(destinationpath_para, file))
        return LEDET_Fs

    def prepareLEDETFiles(self, files, N_PAR=1):
        TurnNumber = 0

        if type(files) == list:
            for i in range(len(files)):
                file = files[i]
                Tnew = self.prepareSingleLEDETFile(file)
                TurnNumber = TurnNumber + Tnew
            TurnNumber = int(TurnNumber / len(files))
        else:
            TurnNumber= self.prepareSingleLEDETFile(files)

        ## Do some kind of check
        TurnNumber_All = TurnNumber*N_PAR

        print(TurnNumber_All,' Turns will be simulated in parallel.')
        if TurnNumber_All >= 10000:
            print("You are trying to simulate ",str(TurnNumber_All),"in parallel mode. \n")
            maxN_PAR = np.floor(10000/TurnNumber)
            print("Consider not to user more than ", str(maxN_PAR)," parallel Simulations.")

    def prepareSingleLEDETFile(self, file):
        a = ParametersLEDET()
        a.readLEDETExcel(file)
        a.Options.flag_useExternalInitialization = 1
        a.Options.flag_generateReport = 0
        a.Options.flag_saveMatFile = 0
        a.writeFileLEDET(file)
        TurnNumber = max(a.Inputs.HalfTurnToInductanceBlock)
        return TurnNumber
