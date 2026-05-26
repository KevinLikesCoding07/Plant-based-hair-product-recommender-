def get_hair_type():


    print("Plant-based hair product recommender")


    choice = input("Enter your hair type (Straight, Wavy, Curly, Coily): ").capitalize().strip()


    valid_types = ["Straight", "Wavy", "Curly", "Coily"]


    


    if choice in valid_types:


        return choice


    else: 


        print("Invalid Hair type. Try again.")


        return get_hair_type()


















def get_scalp_condition():


    choice2 = input("Enter scalp type(Oily, Balanced, Dry, Combination): ").capitalize().strip()


    valid_types2 = ["Oily", "Balanced", "Dry", "Combination"]


    


    if choice2 in valid_types2:


        return choice2 


    else:


        print("Invalid Scalp Type. Try again.")


        return get_scalp_condition()


        


def get_hair_thickness():


    choice3 = input("Enter Hair Thickness(Thin, Fine, Medium, Thick): ").capitalize().strip()


    valid_types3 = ["Thin", "Fine", "Medium", "Thick"]


    


    if choice3 in valid_types3:


        return choice3


    else:


        print("Invalid Hair Thickness. Try again")


        return get_hair_thickness()


        


def get_hair_porosity():


    choice4 = input("Enter Hair porosity(Low, Medium, High):").capitalize().strip()


    valid_type4 = {"Low", "Medium", "High"}


    


    if choice4 in valid_type4:


        return choice4


    else:


        print("Invalid Hair porosity. Try again.")


        return get_hair_porosity


    


user_hair = get_hair_type()


print(f"You Chose: {user_hair}")






user_scalp = get_scalp_condition()


print(f"You Chose: {user_scalp}")






user_thickness = get_hair_thickness()


print(f"You Chose: {user_thickness}")






user_porosity = get_hair_porosity()


print(f"You Chose: {user_porosity}")






def get_recommendation(hair, scalp, thickness, porosity):


    


    scores = {"Murumuru Butter": 0, "Ouai Wave spray": 0, "Tea Tree oil": 0, "Coconut Oil": 0, "shea butter": 0, "aloe vera": 0, "Surface Awaken Shampoo & Conditioner": 0, "Argan Oil": 0,}


    if hair in ["curly", "coily"]:


        scores["Murumuru Butter"] +=3


    if hair in ["wavy"]:


        scores["Ouai Wave spray"] +=3


    if scalp == "Oily":


       scores["Tea Tree oil"] +=5


    if scalp == "dry":


       scores["Coconut Oil"] +=5


    if porosity == "high":


       scores["Shea Butter"] +=5


    if porosity == "low":


       scores["aloe vera"] +=5


    if thickness == "thin":


       scores["Surface Awaken Shampoo & Conditioner"] +=5


    if hair in ["Straight"]:


       scores["Argan Oil"] +=5


       


    max_score = max(scores.values())
    best_match = max(scores, key=scores.get)


    return best_match


    


final_recommendation = get_recommendation(user_hair, user_scalp, user_thickness, user_porosity)


print(f"Based on your hair profile, the best product for you is: {final_recommendation}")






print("DISCLAIMER: This tool is just for educational purposes, it's best to always test a product before using to make sure there is no sensitivity or allergic reactions")






print("Thank you for doing this test")
