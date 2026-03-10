def get_user_file():
    user_input = str(input("Enter the name of a file containing DNA: "))
    if (".txt" not in user_input):
        print("Not a valid file format! Please use a .txt file.")
    else:
        return user_input
    

def read_file(in_file):
    input_file = open(in_file, "r", encoding="utf-8")
    total_sequences = 0
    sequences = 0
    
    for line in input_file:
        if line[0] != "#":
            total_sequences += 1
            line = line.strip()
            dna_list = line.split("\t")
            rsid = dna_list[0]
            genotype = dna_list[3]
            result = classify_RSID(rsid)
            
            if result == "type2":
                type_two_diabetes(genotype)
            elif result == "redHair":
                red_hair(genotype)
            elif result == "lactose":
                lactose(genotype)
            elif result == "blueBrown":
                blue_brown(genotype)
            elif result == "cad":
                coronary_artery(genotype)
            elif result == "none":
                sequences += 1

    input_file.close()
    print("There were", total_sequences, "total sequences searched.")
    print(sequences, "of which were unidentified.")
    print("Read progress: COMPLETE!")


def classify_RSID(rsid):
    if rsid == "rs1333049":
        return "cad"
    elif rsid == "rs4988235":
        return "lactose"
    elif rsid == "rs7754840":
        return "type2"
    elif rsid == "rs1805007":
        return "redHair"
    elif rsid == "rs12913832":
        return "blueBrown"
    else:
        return "none"
    

def type_two_diabetes(genotype):
    if (genotype == "CC") or (genotype == "CG"):
        print("1.3x increased risk for type-2 diabetes")
    elif genotype == "GG":
        print("Normal risk for type-2 diabetes")
    else:
        print("No information on risk for type-2 diabetes")
       
       
def red_hair(genotype):
    if genotype == "CC":
        print("Normal chance of red hair")
    elif genotype == "CT":
        print("Carrier of a red hair associated variant; higher risk of melanoma")
    elif genotype == "TT":
        print("Increased response to anesthetics; 13-20x higher likelihood of red hair; increased risk of melanoma")
    else:
        print("No information on chance of red hair")


def lactose(genotype):
    if genotype == "CC":
        print("Likely to be lactose intolerant as an adult")
    elif genotype == "CT":
        print("Likely to be able to digest milk as an adult")
    elif genotype == "TT":
        print("Can digest milk")
    else:
        print("No information on lactose intolerance")


def blue_brown(genotype):
    if genotype == "AA":
        print("Brown eye color, 80% of the time")
    elif genotype == "AG":
        print("Brown eye color")
    elif genotype == "GG":
        print("Blue eye color, 99% of the time")
    else:
        print("No information on eye color")


def coronary_artery(genotype):
    if genotype == "CC":
        print("1.9x increased risk for CAD")
    elif genotype == "CG":
        print("1.5x increased risk for CAD")
    elif genotype == "GG":
        print("Normal risk for CAD")
    else:
        print("No information on CAD")


chosen_file = get_user_file()
read_file(chosen_file)