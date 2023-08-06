from steam_nb_api.ledet.ParameterSweep import *
from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
import pandas as pd
from steam_nb_api.ledet.Simulation import RunSimulations
from steam_nb_api.ledet.SimulationEvaluation import EvaluateSimulations
from steam_nb_api.ledet.SimulationEvaluation import QuenchPlanAnalysis
from steam_nb_api.ledet.AutomaticSweep import AutomaticSweep
import time

testfile1 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBRC\MBRC_0.xlsx"
testfile2 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBRB\MBRB_0.xlsx"
testfile3 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBRS\MBRS_0.xlsx"
testfile4 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBX\MBX_0.xlsx"
testfile5 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCD\MCD_0.xlsx"
testfile6 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCO\MCO_0.xlsx"
testfile7 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MO_1AP\MO_1AP_8magBB_0.xlsx"
testfile8 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXH\MCBXH_CopperWedges_ThCool_0.xlsx"
testfile9 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXV\MCBXV_CopperWedges_ThCool_0.xlsx"
testfile10 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXV\MCBXV_CopperWedges_0.xlsx"
testfile11 = "C:\cernbox\TEMP2\MCBY_1AP_CopperWedges_ThCool_29.xlsx"
testfile12 = "C:\cernbox\LEDET\LEDET\MCBY_1AP_CopperWedges_ThCool\Input\MCBY_1AP_CopperWedges_ThCool_35.xlsx"

ledetFolder = 'C:\cernbox\LEDET\\'
ledetExe = 'LEDET_v1_07_02_02_25May2020.exe'

def CompleteRun():
    start = time.time()
    a = ParametersLEDET()
    a.readLEDETExcel(testfile9)
    Sw = MinMaxSweep(a, 10)
    MagnetName = 'MCBXH_CopperWedges_ThCool'

    ##8mag
    # Sw.addParameterToSweep('l_magnet', 2.56, 4.8)
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
    ##13mag
    # Sw.addParameterToSweep('l_magnet', 4.16, 5.2)
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)

    # ##MBX/ MRBC/ MBRS/ MBRB
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3, basePoints = 3)
    # Sw.addParameterToSweep('R_c_inGroup', -6, -3, type='logarithmic', basePoints= 3)
    # Sw.addHeliumCrossSection(0, 6, basePoints= 4)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 35, 200, basePoints=6)

    ##8mag
    # Sw.addParameterToSweep('l_magnet', 0.056, 0.14)
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
    # Sw.addHeliumCrossSection(3, 6, basePoints=4)

    ## MCBXH_CopperWedges -1
    Sw.addParameterToSweep('f_ro_eff_inGroup', 0.1, 3)
    Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
    # Sw.addParameterToSweep('l_magnet', 0.056, 0.14)
    # Sw.addQuenchSweep("tStartQuench",[1,1,1,1,1,1],[-0.2, -0.21, -0.22, -0.23, -0.24, -0.25])
    # Sw.addQuenchSweep("tStartQuench", [[1, 730],[321,1050],[1, 730],[321,1050],[1, 730],[321,1050],[1, 730],[321,1050]],
    #                   [[-0.2, -0.182],[-0.2, -0.182],[-0.15, -0.132],[-0.15, -0.132],[-0.1, -0.082],[-0.2, -0.082],[-0.05, -0.032],[-0.05, -0.032]])

    ##MCBY
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)

    ## Current Sweep
    # Sw.addCurrentSweep(6650, 30)

    Sw.generatePermutations()
    end = time.time()
    print("Time:", end-start)
    start = time.time()
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP2\\",OffsetNumber=100)
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MBRC\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCD\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCO\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MO_1AP\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCBXH_CopperWedges_ThCool\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCBXV_CopperWedges_ThCool\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP2\\", OffsetNumber= 42, ROXIE_File='C:\\cernbox\\SWAN_projects\\steam-notebooks\\steam-ledet-input\\MCBXV\\MCBXV_CopperWedges_All_WithIron_WithSelfField.map2d')
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP2\\", OffsetNumber=17, ROXIE_File='C:\\cernbox\\SWAN_projects\\steam-notebooks\\steam-ledet-input\\MCBY_1AP\\MCBY_1AP_CopperWedges_ThCool_All_WithIron_WithSelfField.map2d')
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP2\\", OffsetNumber=50)


    end = time.time()
    print("Time:", end - start)
    print("Preparation done")

    # RunSimulations(ledetFolder, ledetExe, MagnetName, RunSimulations=False)
    # EvaluateSimulations("C:\\cernbox\\LEDET\\LEDET\\MCO\\Output\\Txt Files", 'MCO',
    #                     'C:\\cernbox\\Validation_MCDO\\Exp Data\\RCO.A56B1_2018-03-16_PM_I_A_AutoAlign.csv',
    #                     Sw, Mat=False, SkipAlign=True)
    # EvaluateSimulations("C:\\cernbox\\LEDET\\LEDET\\MCD\\Output\\Txt Files", 'MCD',
    #                     'C:\\cernbox\\Validation_MCDO\\Exp Data\\RCD.A56B1_2018-03-16_PM_I_A_AutoAlign.csv',
    #                     Sw, Mat=False, SkipAlign=True)
    # EvaluateSimulations('C:\cernbox\LEDET\LEDET_SimulationFiles_Quench\LEDET\MBRS\Output\Txt Files', 'MBRS',
    #                      'C:\cernbox\Validation_IPD\Validation MBRS\Exp Data\RD3.R4_20181203_135959_IA - Cut.csv',
    #                     Sw, Mat=False, SkipAlign=True)
    # EvaluateSimulations('C:\cernbox\LEDET\LEDET\MBRC\Output\Txt Files', 'MBRC',
    #                      'C:\cernbox\Validation_IPD\Validation MBRC\Exp Data\RD2.L8_20181203_131307_IA - Cut.csv',
    #                     Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MO\\Validation\\LEDET\\FullB2', 'MO_1AP', 'C:\\cernbox\\LHC-SM-API\\ROD_ROF\\ROD.A12B2_PM_I_A.csv',
    #                     Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MO\\Validation\\LEDET\\FullB1', 'MO_1AP',
    #                     'C:\\cernbox\\LHC-SM-API\\ROD_ROF\\ROD.A12B1_PM_I_A.csv',
    #                      Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MCBX_HV\\LEDET Validation\\1st Sweep-RRR_fro_tQ\\Output\\Txt Files', 'MCBXH_CopperWedges',
    #                     'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXH1.R1_2018-03-11_PM_I_ARAW.csv',
    #                      Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MCBX_HV\\LEDET Validation\\2nd Sweep-RRR_fro_tQ_THCOOL\\Output\\Txt Files',
    #                     'MCBXH_CopperWedges_ThCool', 'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXH1.R1_2018-03-11_PM_I_ARAW.csv',
    #                      Sw, Mat=False, showBestFit = 20)
    EvaluateSimulations("C:\\cernbox\\TEMP\\",
                        'MCBXV_CopperWedges_ThCool', 'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXV2.R1_2017-04-20_PM_I_ARAW.csv',
                         Sw, Mat=False)
    # EvaluateSimulations("C:\\cernbox\\TEMP2\\",
    #                     'MCBXH_CopperWedges_ThCool',
    #                     'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXH1.R1_2018-03-11_PM_I_ARAW.csv',
    #                     Sw, Mat=False)

def AutomaticRun():
    LEDETFolder = 'C:\\cernbox\LEDET\\LEDET_SimulationFiles_Quench'
    LEDETExe = 'LEDET_v1_07_01_6February2020.exe'
    MagnetName = 'MO_1AP'
    MeasFile = 'C:\cernbox\LHC-SM-API\ROD_ROF\ROD.A12B2_PM_I_A.csv'
    SetUpFile = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MO_1AP\MO_1AP_8magBB_0.xlsx"

    ASw = AutomaticSweep(8, SetUpFile, LEDETFolder, LEDETExe, MagnetName, MeasFile)
    ASw.addParameterToSweep('l_magnet', 2.56, 4.8)
    ASw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    ASw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
    #ASw.AutomaticRun(101)

    ASw.LearnAndTrainAll()
    return ASw

def testConsistencyChecks():
    a = ParametersLEDET()
    a.readLEDETExcel(testfile10)
    x = a.consistencyCheckLEDET()
    print(x)

def testvQ():
    nameFileLEDET = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\D2\D2_0.xlsx"
    a = ParametersLEDET()
    a.readLEDETExcel(nameFileLEDET)
    Sw = MinMaxSweep(a, 1)
    I00 = 12330
    Sw.addCurrentSweep(I00, 1)
    nameMagnet = "D2"
    Sw.prepareSimulation(nameMagnet, "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\D2",
                         ROXIE_File="C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\D2\D2_All_WithIron_WithSelfField.map2d")

def testQuenchPlanAnalysis(FileName_TDMS, FileName_Sim):
    a = QuenchPlanAnalysis(FileName_TDMS, FileName_Sim)
    a.QuenchPlanAnalysis()
    return a

# testConsistencyChecks()
# test_readLEDETExcel()
# test_setgetAttributes()
# test_permutations()
# test_SetUpSimulations()
# test_EvaluateSimulations()

# CompleteRun()

td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\MQXFS4b\\HCMQXSM001-CR000042__H1810111001_a001(0).tdms"
sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_5.mat"
a = testQuenchPlanAnalysis(td_data, sim_data)

# a = ParametersLEDET()
# a.readLEDETExcel(testfile7)
# Sw = MinMaxSweep(a, 3)
# MagnetName = 'MCBXH_CopperWedges'
# Sw.addParameterToSweep('l_magnet', 4.16, 5.2)
# Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
# Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
# Sw.addQuenchSweep("tStartQuench",[0,2],[-3,5])
# Sw.addQuenchSweep("tStartQuench",[[1,4],[2,5]],[[-3,5],[1,2]])
# Sw.addHeliumCrossSection(3, 6, basePoints=4)
# Sw.generatePermutations()
# Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEST-DELTE\\")

# x = AutomaticRun()
