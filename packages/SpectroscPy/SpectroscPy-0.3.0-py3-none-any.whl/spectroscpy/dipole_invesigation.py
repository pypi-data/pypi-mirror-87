from .vib_analysis import read_mol

def symmetric_alteration(folder, mol, d):

    coords, charges, masses = read_mol(folder + mol)
    
    print(coords)
