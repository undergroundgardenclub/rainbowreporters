# 🌈 RAINBOW REPORTERS 🌈

- database of proteins (should i care about doing collections)
  - some portion will have PDB atomic coordinates. but many will exist just as amino acids
  - how do i handle states? separate records? when you have variations
  - to make life simple just gonna grab the first 1k from FPBase
- viewer of colorpicker
  - color picker RGB <> nm wavelength. gives a sorted list by closeness
  - picking gives you structure w/ analysis charts
- with trained network, output if there's a fluorescence at certain wavelength/brightness


pipelines (going to use same db for local/prod. don't want to bother w/ multiple envs):
- FPBase JSON into supabase
- loop through DB, download PDB files and put into Tigris, then update respective rows with the S3 URL to file







- agg	
- doi	
- genbank	
- ipg_id	
- name
- pdb (ids)
- pdb.0 (ids)
- seq (amino acids)
- slug
- states.0.brightness	states.0.em_max	states.0.ex_max	states.0.ext_coeff	states.0.lifetime	states.0.maturation	states.0.name	states.0.pka	states.0.qy	states.0.slug
- states.1.brightness	states.1.em_max	states.1.ex_max	states.1.ext_coeff	states.1.lifetime	states.1.maturation	states.1.name	states.1.pka	states.1.qy	states.1.slug
- states.2.brightness	states.2.em_max	states.2.ex_max	states.2.ext_coeff	states.2.lifetime	states.2.maturation	states.2.name	states.2.pka	states.2.qy	states.2.slug
- switch_type
- transitions.0.from_state	transitions.0.to_state	transitions.0.trans_wave	transitions.1.from_state	transitions.1.to_state	transitions.1.trans_wave
- uniprot	uuid


