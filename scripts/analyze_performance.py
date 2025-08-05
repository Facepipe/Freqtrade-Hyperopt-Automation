#!/usr/bin/env python3
"""
Quick performance analysis of hyperopt results
"""
import pandas as pd
import os
from pathlib import Path

def analyze_results():
    """Analyze hyperopt summary results"""
    summary_files = list(Path('output').glob('**/hyperopt_summary.csv'))
    
    if not summary_files:
        print("❌ No summary files found in output directory")
        return
    
    print(f"📊 Found {len(summary_files)} summary file(s)")
    
    for summary_file in summary_files:
        print(f"\n📈 Analyzing: {summary_file}")
        
        try:
            df = pd.read_csv(summary_file)
            
            if len(df) == 0:
                print("   ⚠️  Empty summary file")
                continue
                
            print(f"   📋 Total runs: {len(df)}")
            print(f"   🏆 Best strategy: {df.loc[df['total_profit'].idxmax(), 'strategy']}")
            print(f"   💰 Best profit: {df['total_profit'].max():.4f}")
            print(f"   📊 Average profit: {df['total_profit'].mean():.4f}")
            print(f"   🎯 Win rate range: {df['win_ratio'].min():.2%} - {df['win_ratio'].max():.2%}")
            
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")

if __name__ == "__main__":
    analyze_results()
