import json
import math
import os
import pandas as pd
import requests
import matplotlib.pyplot as plt


# Schema for Proteins Dataframe:
# - name
# - seq
# - pdb_id
# - brightness
# - em_max
# - ex_max
# - states
# - tags (ex: ['fluorescentprotein', 'chromoprotein'])


# %%
# Fetch Datasets (starting from FPBase collection)
# --- collection csv
local_data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
local_data_fps_csv = f"{local_data_dir}/fluorescent_proteins.csv"
fpbase_fp_collection_csv_url = "https://www.fpbase.org/collection/2811/?format=csv"

if not os.path.exists(local_data_fps_csv):
  fps_df = pd.read_csv(fpbase_fp_collection_csv_url)
  # transform data to match schema (ex: states are a list of columns as states.0.name, states.0.brightness, etc.)
  for index, row in fps_df.iterrows():
    states = []
    for i in range(8):
      col_idx = str(i)
      # if there are no critical values like em_max, skip
      if isinstance(row.get(f"states.{col_idx}.em_max"), float) and not math.isnan(row.get(f"states.{col_idx}.em_max")):
        state = {}
        state['pbd_id'] = row['pdb.' + col_idx]
        state['name'] = row["states." + col_idx + '.name']
        state['brightness'] = row["states." + col_idx + '.brightness']
        state['em_max'] = row["states." + col_idx + '.em_max']
        state['ex_max'] = row["states." + col_idx + '.ex_max']
        state['ext_coeff'] = row["states." + col_idx + '.ext_coeff']
        state['lifetime'] = row["states." + col_idx + '.lifetime']
        state['maturation'] = row["states." + col_idx + '.maturation']
        state['pka'] = row["states." + col_idx + '.pka']
        state['qy'] = row["states." + col_idx + '.qy']
        states.append(state)
        if i == 0:
          fps_df.at[index, 'pdb_id'] = row['pdb.' + col_idx]
          fps_df.at[index, 'brightness'] = row["states." + col_idx + '.brightness']
          fps_df.at[index, 'em_max'] = row["states." + col_idx + '.em_max']
          fps_df.at[index, 'ex_max'] = row["states." + col_idx + '.ex_max']
    fps_df.at[index, 'states'] = json.dumps(states)
    fps_df.at[index, 'tags'] = json.dumps(['fluorescentprotein'])
    fps_df.at[index, 'name'] = row['slug']
  fps_df.drop(columns=["agg", "doi", "genbank", "ipg_id", "pdb", "slug", "switch_type", "uniprot", "uuid"], inplace=True)
  fps_df.drop(columns=[col for col in fps_df.columns if col.startswith('pdb.')], inplace=True)
  fps_df.drop(columns=[col for col in fps_df.columns if col.startswith('states.')], inplace=True)
  fps_df.drop(columns=[col for col in fps_df.columns if col.startswith('transitions.')], inplace=True)
  fps_df.to_csv(local_data_fps_csv, index=False)
else:
  fps_df = pd.read_csv(local_data_fps_csv)

# --- spectra csv (doing it in two parts bc the URL is too long)
local_data_fps_spectra_csv = f"{local_data_dir}/fluorescent_proteins_spectra.csv"

if not os.path.exists(local_data_fps_spectra_csv):
  # ... download in two parts bc of long URL
  fpbase_fp_collection_spectra_csv_part_1_url = "https://www.fpbase.org/spectra_csv/?q=1992,7857,6059,6060,6061,6062,6063,6064,6065,6066,6067,6068,7610,7611,2000,2001,2002,2003,7841,7381,7383,7384,1307,1308,6902,6901,6903,7854,7910,7911,7842,7843,7844,7870,7871,7872,7873,2,1,7909,1597,1598,7858,7859,7860,1561,1562,1570,6071,6072,6075,6079,6076,6073,6074,6077,6078,6475,6476,1595,1596,7677,7678,6481,6482,7379,7380,6485,6486,7145,7146,2259,2260,7407,7408,6292,6290,6291,6293,6294,6295,149,150,7402,2066,2067,5716,5717,7879,6635,3,160,4,6503,6504,7845,147,148,7949,7187,6752,6753,7147,7148,5,6,7945,7,8,6812,6813,2187,2188,1557,1558,1559,1560,2149,2150,2151,2153,2152,2154,1648,1649,1885,1884,1915,1914,7018,7017,1856,1857,1855,1844,1845,6917,6918,6916,9,10,7345,179,1980,1981,1591,1592,1594,1593,7364,7365,1809,1810,6905,6904,6906,1589,1590,7153,7154,192,1807,1808,1320,1319,12,1588,11,189,183,13,14,177,15,16,163,7840,6914,6915,6913,7855,7856,17,18,173,7670,7078,7077,7669,7080,7081,7368,7369,1586,1587,190,1862,1863,187,49,50,20,19,6128,7620,7621,7357,7358,21,22,7951,6930,6931,167,169,1646,1647,5865,5866,7846,6496,6497,6498,7861,6666,6665,6494,6495,6492,6493,6818,6501,6502,6500,7880,5960,5959,6477,6478,2060,2061,2053,2054,7878,1584,1585,7227,7228,7231,7232,7249,7250,7251,7252,7263,7264,7283,7284,7287,7288,7281,7282,7209,7210,7257,7258,7225,7226,7219,7220,7203,7204,7289,7290,7213,7214,7235,7236,7205,7206,7265,7266,7259,7260,7295,7296,7197,7198,7201,7202,7221,7222,7269,7270,7271,7272,7285,7286,7291,7292,7207,7208,7215,7216,7245,7246,7247,7248,7253,7254,7255,7256,7261,7262,7267,7268,7293,7294,7217,7218,7319,7320,7299,7300,7301,7302,7325,7326,7311,7312,7317,7318,7323,7324,7305,7306,7313,7314,7335,7336,7309,7310,7327,7328,7329,7330,7333,7334,7303,7304,7308,7307,7321,7322,7315,7316,7331,7332,7275,7276,7243,7244,7199,7200,7242,7241,7237,7238,7277,7278,7273,7274,7279,7280,7229,7230,7223,7224,7234,7233,7239,7240,7211,7212,7351,7352,51,52,53,54,55,56,7499,59,60,61,62,63,64,65,66,7500,6302,6303,6304,6305,6306,6307,1924,1925,6314,6315,6316,6318,6319,6317,5847,6281,6282,6283,6278,6279,6280,1917,1919,1916,1918,161,1864,1865,1922,1923,6919,6921,6920,1936,1935,6296,6297,6298,6299,6300,6301,1910,1911,1912,1913,1982,1983,1984,1978,1979,23,24,1846,1847,7347,7353,7627,7628,5799,5800,7349,7354,6660,6661,1509,1510,1342,1343,7190,7136,7137,6814,6815,67,68,164,7946,69,70,1838,1839,7679,7680,6069,6070,71,72,7164,178,73,74,7640,7641,7642,7647,7648,7650,7649,7191,7495,7494,180,1834,1835,75,76,7950,7534,1537,1538,2072,162,2062,2063,5714,5715,7184,79,80,158,1451,1450,6995,6994,171,1340,1341,81,82,6132,6133,2185,2186,6127,1565,1566,1567,6910,6911,6912,7847,1554,1555,1556,6908,6909,6907,83"
  fpbase_fp_collection_spectra_csv_part_2_url = "https://www.fpbase.org/spectra_csv/?q=84,1652,1653,1654,1651,1656,1655,1657,1658,139,140,141,142,1773,1774,1771,1772,1777,1775,1778,1779,6542,6543,6544,6545,2280,2281,2282,1300,1301,2301,2049,2050,2051,2052,6337,6338,6339,191,1870,1871,6366,6367,86,85,25,26,6758,6759,7155,7156,7157,7158,7159,7160,1996,1997,2039,2040,2041,1612,1613,7374,7375,1604,1606,7370,7371,2086,2087,7150,7151,7152,7366,7367,1610,1611,1607,1609,7372,7373,1676,1677,184,90,89,193,91,92,93,94,159,1826,1827,5706,5707,6539,6540,6541,6538,95,96,2045,2046,2047,2048,6255,6256,6253,6254,1908,1909,1906,1907,1988,1989,1990,97,98,87,88,7188,168,1874,1875,1672,1673,1674,1675,1666,1667,1664,1665,1661,1663,1659,1660,1434,1435,6126,99,100,101,102,6900,103,104,170,5734,5736,1539,1540,7355,7356,1886,1880,1881,77,78,157,105,106,7189,1832,1833,1681,1682,1680,1679,1858,1859,1670,1671,1668,1669,107,108,175,109,110,182,114,113,188,58,57,2156,111,112,6324,6325,6322,6323,6320,6321,7900,7902,7901,7903,7904,7905,7906,7907,7908,115,116,117,118,7340,1303,1304,6988,6989,6987,6990,119,120,6896,7460,7462,7463,7464,7465,7466,7467,7468,7469,7453,7454,7455,121,122,123,124,6898,7471,7472,7470,7456,7457,7458,7473,7474,7475,1324,1321,7686,7685,7684,7682,125,1578,126,1338,1339,7943,131,165,132,155,185,127,128,1699,1698,1746,1745,6551,7185,1685,1686,133,134,1601,1602,135,156,136,186,1872,1873,1879,1878,6284,6285,6286,6287,6288,6289,1836,1837,1860,1861,2065,2064,1568,1569,1887,1888,1573,1571,1572,1889,1890,1891,5840,5841,5843,5842,1933,1934,6546,6547,6548,6550,7161,7162,6670,6775,2073,2074,7536,7537,7538,7539,7540,7541,7542,7543,7545,7544,7546,7549,7547,7548,7550,7551,7129,7128,2140,2141,6479,6480,1927,1928,7297,7298,1930,1929,1931,1932,2120,2121,2118,2119,7623,7624,6260,6261,1830,1831,6308,6309,6310,6311,6312,6313,6266,6267,6268,6269,6270,6271,6272,6273,6274,6275,6276,6277,2127,2128,2125,2126,1822,1823,1824,1825,1842,1843,2076,2077,2081,2080,2079,2078,1816,1817,1814,1815,1818,1819,7866,7867,7868,1464,1465,29,30,1577,7948,7947,1688,1687,7479,7480,7886,7887,1976,1977,7919,7920,7921,7922,1466,1467,1968,1969,1691,1692,1693,1694,1689,1690,145,146,1792,1793,1998,1999,2006,2007,7501,7851,1852,1853,1854,6682,6683,7083,7084,7574,7575,7848,1306,1305,7944,6899,2183,2182,6924,6925,6926,1991,1995,1994,1985,1986,1987,6777,6778,28,27,176,1734,1733,33,34,1920,1921,174,35,36,37,38,166,43,44,6675,6676,6658,6659,39,40,45,46,6669,6667,6668,181,143,144,137,172,138,1882,1883,47,48,7070,7071,32,31,6720,6721,2285,2286,7849,1840,1841,1683,1684,151,152,7401,1848,1849,1850,1851,1876,1877,41,42,1309,1310,1902,1903"
  spectra_df1 = pd.read_csv(fpbase_fp_collection_spectra_csv_part_1_url)
  spectra_df2 = pd.read_csv(fpbase_fp_collection_spectra_csv_part_2_url)
  # ... combine
  spectra_df = pd.concat([spectra_df1, spectra_df2])
  spectra_df.to_csv(local_data_fps_spectra_csv, index=False)
else:
  spectra_df = pd.read_csv(local_data_fps_spectra_csv)


# %%
# Quick Observations
# ... emission ranges/frequency across all proteins
plt.hist(fps_df['em_max'], bins=32, color='blue', label='All Fluorescent Proteins')
# ... emission ranges/frequency across all proteins we have protein structures for
plt.hist(fps_df[fps_df['pdb_id'].notnull()]['em_max'], bins=32, color='orange', label='Fluorescent Proteins with PDB')
plt.xlabel('em_max')
plt.ylabel('Frequency')
plt.title('Histogram of em_max values')
plt.legend()
plt.show()

print(f"Total Fluorescent Proteins: {len(fps_df)}")
print(f"% with Crystal Structures: {round(len(fps_df[fps_df['pdb_id'].notnull()]) / len(fps_df) * 100, 2)}%")

# ... plot the highest brightness value for each wavelength histogram bucket, to see where highs/lows are in em_max spectrum
em_max_buckets = [i for i in range(400, 701, 10)]
max_brightness_values = []
for em_max_bucket in em_max_buckets:
  max_brightness_values.append(fps_df[fps_df['em_max'] == em_max_bucket]['brightness'].max())
plt.bar(em_max_buckets, max_brightness_values, width=10, color='blue')
plt.xlabel('em_max')
plt.ylabel('Max Brightness')
plt.title('Max Brightness for each em_max bucket')
plt.show()

# ... plot distribution of brightness values, and which have crystal structures
plt.hist(fps_df['brightness'], bins=32, color='blue', label='All Fluorescent Proteins')
plt.hist(fps_df[fps_df['pdb_id'].notnull()]['brightness'], bins=32, color='orange', label='Fluorescent Proteins with PDB')
plt.xlabel('Brightness')
plt.ylabel('Frequency')
plt.title('Histogram of Brightness values')
plt.legend()
plt.show()


# %%
# Fetch PDB files available and save to disk
pdb_dir = f"{local_data_dir}/pdbs"
pdb_col_names = list(filter(lambda n: n.startswith("pdb"),fps_df.columns.values)) # ex: pdb, pdb.1, pdb.2, ...
pdb_ids = set()

# --- compile ids
for index, fp in fps_df.iterrows():
  pdb_ids.add(fp['pdb_id'])
  # for col_name in pdb_col_names:
  #   pdb_id = fp[col_name]
  #   if pdb_id:
  #     pdb_ids.add(pdb_id)

# --- download (if doesn't already exist)
os.makedirs(pdb_dir, exist_ok=True)
for pdb_id in pdb_ids:
  pdb_file_path = f"{pdb_dir}/{pdb_id}.pdb"
  # ... if we haven't downloaded
  if not os.path.exists(pdb_file_path):
    pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(pdb_url)
    with open(pdb_file_path, 'wb') as file:
      file.write(response.content)


# %%
# Calculate extra visiblity data
# ... nm wavelength => HEX or RGB or LAB (LAB seems its used in physics/optics more? maybe do both LAB/RGB)
