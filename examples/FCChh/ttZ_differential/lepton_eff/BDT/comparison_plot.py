import pandas as pd
import matplotlib.pyplot as plt

# Load the data from CSV files
low_score_df = pd.read_csv('/eos/user/l/lberiet/ttZ_diff_results/BDT/non_prompt_low_score.csv')
high_score_df = pd.read_csv('/eos/user/l/lberiet/ttZ_diff_results/BDT/non_prompt_leptons_high_score.csv')

# Plot pT distributions
plt.hist(low_score_df['D0sig'], bins=50, histtype='step', density=True, label='Non-prompt Low Score (< 0.1)', color='blue')
plt.hist(high_score_df['D0sig'], bins=50, histtype='step', density=True, label='Non-prompt High Score (> 0.9)', color='red')

# Customize the plot
plt.xlabel('D0')
plt.ylabel('Normalized Frequency')
plt.title('D0 Distribution of Non-prompt Leptons')
plt.yscale('log')
plt.legend()

# Save the plot
plt.savefig('/eos/user/l/lberiet/ttZ_diff_results/BDT/comparison/non_prompt_D0sig_comparison.png')
plt.close()
print('Plot saved as /eos/user/l/lberiet/ttZ_diff_results/BDT/comparison/non_prompt_D0sig_comparison.png')
