import xlsxwriter
import pandas as pd
import numpy as np
import openpyxl as op
import itertools

def make_copy(path, filename):
        obe = op.load_workbook(path + filename)
        obe.save(path + 'OBE_' + filename)

def update_df(df1, df2, id_lst, col1, col2,id1, id2):
        # takes in 2 df and the list of ids form the happypath df 
        # as well as the name of the column that you want to update, and the column name that will be used to do the updates
        
        for id in id_lst:
                #create a df that stores all the values of that column
                df2_columnval = df2[df2[id2] == id][col2].values
                # print(df2_columnval)
                if len(df2_columnval) > 1:
                        #print(str(id) + " is duplicate garbage")
                        pass

                else:
                        #print(id)
                        row_index = df1.index[df1[id1] == id]
                        # print(row_index)
                        # using the index(or lien id), the 1st df value is replaced by the one found in the df2_columnval 
                        df1.loc[row_index, col1] = df2_columnval

def update_dups(df1, df2, id_lst, col1, col2, col3, col4, id1, id2):
        # takes in 2 df and the list of ids form the happypath df 
        # as well as the name of the columns that you want to update, and the column names that will be used to do the updates
        
        for id in id_lst:
                #create a df that stores all the values of that column
                df2_columnval_amt = df2[df2[id2] == id][col3].values
                df2_columnval_qnum = df2[df2[id2] == id][col4].values
                if df2_columnval_qnum > 5:
                        #print(str(id) + " is duplicate garbage")
                        df2_columnval_amt = 0
                        row_index = df1.index[df1[id1] == id]
                        df1.loc[row_index, col1] = df2_columnval_amt
                        df1.loc[row_index, col2] = df2_columnval_qnum
                else:
                        #print(id)
                        row_index = df1.index[df1[id1] == id]
                        #print(row_index)
                        # using the index(or lien id), the 1st df value is replaced by the one found in the df2_columnval 
                        df1.loc[row_index, col1] = df2_columnval_amt
                        df1.loc[row_index, col2] = df2_columnval_qnum



def update_label(df1,id_lst, id1, col1, str_label):
        # takes in df and updates the claimant in hp list to TRUE
        if df1.empty:
                print('yayayaya')
                pass
        else:                
                for id in id_lst:
                        row_index = df1.index[df1[id1] == id]
                        df1.loc[row_index, col1] = str_label
                return(df1)

def move_sheet(wb, from_loc = None, to_loc = None):
        sheets = wb._sheets

        # if no from_loc given, assume last sheet
        if from_loc is None:
                from_loc = len(sheets) - 1

        # if no to_loc given, assume first sheet
        if to_loc is None:
                to_loc = 0

        sheet = sheets.pop(from_loc)
        sheets.insert(to_loc, sheet)


def add_ws(path, wb, new_ws, sheetname, sheetnum):
        # Adds the updated df to the original wb. 
        # Once trusted we can remove the original df with the updated one

        writer = pd.ExcelWriter(path, engine = 'openpyxl')
        writer.book = wb
        writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
        #wb.remove(wb['CMS_Third Party Liens'])
        #wb.remove(wb['Law Firm Representation'])

        # Adds the new updated tab into workbook

        new_ws.to_excel(writer, sheet_name = sheetname, startrow = 0, startcol = 0, header = True, index = False)
        move_sheet(wb, from_loc = None, to_loc = sheetnum)
        #rename_sheet1 = wb['LF']
        #rename_sheet1.title = 'Law Firm Representa#tion'
        writer.save()
        writer.close()

def export(df1, filename, path):
        
        casename = df1.groupby('COL Case Name')
        #print(casename)
        case_list = list(casename.groups.keys())
        #print(case_list)
        i = 0
        if not case_list:
                pass
        else:
                for i in range(0, len(case_list)):
                        i_name = case_list[i]
                        hi = casename.get_group(i_name)
                        df_lf = hi[['FirstName',	'LastName',	'Claim Ref #',	'COL Claim Number',	'COL Attorney',	'COL Case Name',	'COL Payment Group',	'Claim Status',	'S3 Client Id',	'SLAM ThirdPartyId',	'SLAM CaseName',	'SLAM CaseId',	'Claimant in SLAM correctly?',	'Current Escrow',	'Claimant on CSR?',	'Escrow Analysis',	'#Problems',	'Bad List Note',	'#Prob Notes',	'Misc. Issues',	'COL SA',	'SLAM SA',	'SA Matches?',	'COL SSN',	'SLAM SSN',	'SSN Matches?',	'SSN Research',	'Final (SLAM Summary)',	'SLAM Finalized Status Id',	'Truly Final/FinalizedStatusId Issue?',	'SLAM Client Funded',	'Completed by GRG HB Report?',	'Updated SLAM Final',	'SLAM Quest Recd',	'Electronic Release Date',	'Paper Release Date',	'Updated Release Date',	'Release Returned?',	'Rules for Q2, Q4, Questionnaire, Release',	'Should we update?',	'COL Mcare',	'COL Non PLRP',	'COL Mcaid',	'COL Third Party',	'COL PLRP',	'SLAM Mcare',	'SLAM Non PLRP',	'SLAM Mcaid',	'SLAM Third Party',	'SLAM PLRP',	'Update Questions?',	'Updated Mcare',	'Updated Non PLRP',	'Updated Mcaid',	'Updated Third Party',	'Updated PLRP',	'COL HB',	'SLAM HB',	'Update HB?',	'SLAM HB/Updated HB',	'Initial_LF_Label',	'LF_Label']]
                        df_lf_dedupe = pd.DataFrame.drop_duplicates(df_lf)
                        df_cms = hi[['COL LienId',	'COL LienType',	'COL Question #',	'COL Status',	'COL Amount',	'COL Lienholder',	'COL Id',	'COL Claim number',	'COL CaseName',	'ThirdPartyId',	'SLAM LienId',	'SLAM LienType',	'SLAM Question #',	'SLAM Status',	'SLAM Amount',	'SLAM Lienholder',	'ThirdPartyId_Match?',	'Null_Liens',	'Status_Check',	'LienType_Check',	'LienId_Check',	'Amount_Check',	'Question_#_Check',	'Lienholder_Check',	'InSLAM_Check',	'Initial_CMS_Label',	'CMS_Label']]
                        with pd.ExcelWriter(path + filename + i_name + ".xlsx") as writer:
                                df_lf_dedupe.to_excel(writer, sheet_name = 'LF', index = False)
                                df_cms.to_excel(writer, sheet_name = 'CMS', index = False)


def t_export(df1, filename, path):
        
        casename = df1.groupby('COL Case Name')
        #print(casename)
        case_list = list(casename.groups.keys())
        #print(case_list)
        i = 0
        if not case_list:
                pass
        else:
                for i in range(0, len(case_list)):
                        i_name = case_list[i]
                        hi = casename.get_group(i_name)
                        hi.to_excel(path + filename + i_name + ".xlsx", sheet_name = 'Analysis', header = True, index = False)

def add_liens(cms, version, addliens):
        orig_cn = version.iloc[0]['Firm']
        #print(orig_cn)
        newliens = addliens[addliens['COL CaseName'] == str(orig_cn)] 
        newliens.head()
        newliens_df = newliens.rename(columns = {"Claim Ref #": "Claim Ref #", "SLAM Status": "Status", "SLAM Amount": "Amount", "SLAM LienType": "Lien type", "SLAM Lienholder":"Lien holder", "SLAM Question #": "Question number", "SLAM LienId": "Lien Id"})
        #print(newliens_df)
        full_added_df = pd.concat([cms, newliens_df], sort=False, ignore_index=True)
        final_cms_df = full_added_df.drop(columns = ['Unnamed: 0','FirstName','LastName','COL Claim Number','COL Attorney','COL Case Name','COL CaseName','COL Payment Group',	'Claim Status',	'S3 Client Id',	'SLAM ThirdPartyId','SLAM CaseName','SLAM CaseId','Claimant in SLAM correctly?','Current Escrow','Claimant on CSR?','Escrow Analysis','#Problems','Bad List Note','#Prob Notes','Misc. Issues',	'COL SA','SLAM SA','SA Matches?','COL SSN','SLAM SSN','SSN Matches?','SSN Research','Final (SLAM Summary)','SLAM Finalized Status Id','Truly Final/FinalizedStatusId Issue?',	'SLAM Client Funded',	'Completed by GRG HB Report?',	'Updated SLAM Final',	'SLAM Quest Recd','Electronic Release Date','Paper Release Date',	'Updated Release Date',	'Release Returned?',	'Rules for Q2, Q4, Questionnaire, Release',	'Should we update?',	'COL Mcare',	'COL Non PLRP',	'COL Mcaid',	'COL Third Party',	'COL PLRP',	'SLAM Mcare',	'SLAM Non PLRP',	'SLAM Mcaid',	'SLAM Third Party',	'SLAM PLRP',	'Update Questions?',	'Updated Mcare',	'Updated Non PLRP',	'Updated Mcaid',	'Updated Third Party',	'Updated PLRP',	'COL HB',	'SLAM HB',	'Update HB?',	'SLAM HB/Updated HB',	'LF_Label','COL LienId','COL LienType',	'COL Question #','COL Status','COL Amount','COL Lienholder','COL Id','COL Claim number','ThirdPartyId',	'ThirdPartyId_Match?','Null_Liens','Status_Check','LienType_Check','LienId_Check','Amount_Check','Question_#_Check','Lienholder_Check',	'InSLAM_Check',	'CMS_Label',
        ])
        return(final_cms_df)