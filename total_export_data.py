#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:27:07 2018

@author: phuongpham
"""

import pandas as pd

def total_export(file):
    df = pd.read_csv(file)
    df_trade_rel = df.groupby(['location_code', 'partner_code'])[['export_value', 'import_value']].sum().reset_index()
    
    # Invert the trade relationship to capture the total export/import
    df_invert = pd.DataFrame()
    df_invert['location_code'] = df_trade_rel['partner_code']
    df_invert['partner_code'] = df_trade_rel['location_code']
    df_invert['export_value'] = df_trade_rel['import_value']
    df_invert['import_value'] = df_trade_rel['export_value']
    
    # Combine
    df_aggregate = pd.concat([df_trade_rel, df_invert], axis = 0)
    
    # Finalize
    df_final = df_aggregate.groupby(['location_code', 'partner_code'])[['export_value', 'import_value']].sum().reset_index()

    # Total export in the world
    total_export = sum(df_final['export_value'])
    total_import = sum(df_final['import_value'])
    
    print(">>> Total export == total import ...", total_export == total_import)
    
    df_final['export_portion'] = df_final['export_value']/total_export
    df_final['import_portion'] = df_final['import_value']/total_import
    
    return df_final
