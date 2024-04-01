import numpy as np
from typing import Counter, List, Optional
import os


class User:
    def __init__(
        self,
        age: str,
        workclass,
        fnlwgt,
        education: str,
        education_num,
        marital_status: str,
        occupation: str,
        relationship,
        race: str,
        sex,
        capital_gain,
        capital_loss,
        hours_per_week,
        native_country,
        salary,
        e=None,
    ):
        self.age = age
        self.workclass = workclass
        self.fnlwgt = fnlwgt
        self.education = education
        self.education_num = education_num
        self.marital_status = marital_status
        self.occupation = occupation
        self.relationship = relationship
        self.race = race
        self.sex = sex
        self.capital_gain = capital_gain
        self.capital_loss = capital_loss
        self.hours_per_week = hours_per_week
        self.native_country = native_country
        self.salary = salary
        self.userSet = None
        self.initialize_sets()
        
    def initialize_sets(self):
        if self.userSet and self.count == 1:
            return
        if self:
            self.userSet = set([self])
            self.count = 1

def read_raw_data(file_path):
    with open(file_path) as file:
        if not file:
            print("no file")
            exit(1)
        users = []
        for user_data in file:
            user_info_list = user_data.split(",")
            if not len(user_info_list) == 15: # incomplete data
                # print("Incomplete data detected.")
                pass
            else:
                # missimg value generalized to the top of the hierarchy "*"
                for i in range(len(user_info_list)):
                    user_info = user_info_list[i].strip()
                    if user_info == "?":
                        user_info_list[i] = "*"
                user = User(*user_info_list) # create user object
                users.append(user)
        return users

def filter_age(users):
    filtered_users = [user for user in users if int(user.age) > 25]
    for user in filtered_users:
        user.age = int(user.age)
    return filtered_users

def calculate_average_age(users):
    total_age = sum(int(user.age) for user in users)
    average_age = total_age / len(users) if users else 0
    return average_age

def find_frequent_education(users):
    educations = [user.education for user in users]
    education_counter = Counter(educations)
    most_frequent_education, count = education_counter.most_common(1)[0]
    return most_frequent_education.strip(), count

def get_global_sensitivity(average_age, age_data):
    original_mean = average_age
    max_difference = float('-inf')
    for i, age in enumerate(age_data):
        remaining_mean = (sum(age_data) - age) / (len(age_data) - 1)
        difference = abs(original_mean - remaining_mean)
        if difference > max_difference:
            max_difference = difference
    return max_difference

def get_variance(b):
    return 2 * pow(b, 2)

# main function:
def mechanism(mechanism, ε):
    print(ε,"- Differential Privacy")
    raw_users_list = read_raw_data("./adultdata/adult.data")
    
    if mechanism == "laplace":
        filtered_users = filter_age(raw_users_list)
        average_age = calculate_average_age(filtered_users)
        age_data = [user.age for user in filtered_users]
        sensitivity = get_global_sensitivity(average_age, age_data)
        μ = 0
        b = sensitivity/ε
        variance = get_variance(b)
        laplace = np.random.laplace(μ, b)
        result = average_age + laplace

        print("Number of users:", len(filtered_users))
        print("Average age:", average_age)
        print("Global Sensitivity:", sensitivity)
        print("Variance:", variance)
        print("Laplace:", laplace)
        print("Result:", result)
        print("\n")
    
    elif mechanism == "exponential":
        most_frequent_education, count = find_frequent_education(raw_users_list)
        sensitivity = 1 # because of counting query
        # getVariance()
        # exponential()
        
        print("Most frequent education:", most_frequent_education)
        print("Number of users:", count)
        print("Global Sensitivity:", sensitivity)
        # print("Variance:")
        # print("Result:", result)
    return



