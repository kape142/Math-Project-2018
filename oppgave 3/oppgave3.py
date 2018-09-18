
def krefter_g(Gkonstant, masseJorda, masseManen, posisjonJorda, posisjonManen):
    return Gkonstant*masseManen*masseJorda*((posisjonJorda-posisjonManen)/((posisjonJorda**3-posisjonManen**3)**(1/3)))
