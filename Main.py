import copy
from math import exp
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

def get_education_data(users):
    user_education_data = [user.education.strip() for user in users]
    return user_education_data

def compute_utility_scores(user_education_data):
    education_counter = Counter(user_education_data)
    utility_scores_object = {}
    possible_outputs = []
    utility_scores = []
    for education, count in education_counter.items():
        utility_scores_object[education] = count
        possible_outputs.append(education)
        utility_scores.append(count)
    return utility_scores_object, possible_outputs, utility_scores

def genD(dataset, output):
    result = []
    new_dataset = copy.deepcopy(dataset)
    new_dataset[output] -= 1
    for key in dataset.keys():
        if key != output:
            new_other_dataset = copy.deepcopy(new_dataset)
            new_other_dataset[key] += 1
            result.append(new_other_dataset)
    return result


def get_global_sensitivity2(utility_scores_object, possible_outputs):
    max_score = float("-inf")
    for r in possible_outputs:
        # print(r)
        d2 = genD(utility_scores_object, r)
        for d in d2:
            # print(d)
            score = abs(d[r] - utility_scores_object[r])
            # print(score, max_score)
            max_score = max(score, max_score)
    return max_score

def normalize_scores(scores):
    max_score = max(scores)
    normalized_scores = []
    for score in scores:
        normalized_score = score / max_score
        normalized_scores.append(normalized_score)
    return normalized_scores


# main function:
def mechanism(mechanism, ε):
    print(ε,"- Differential Privacy")
    raw_users_list = read_raw_data("./adultdata/adult.data")
    
    if mechanism == "laplace":
        filtered_users = filter_age(raw_users_list)
        print("Number of users:", len(filtered_users))
        average_age = calculate_average_age(filtered_users)
        print("Average age:", average_age)
        age_data = [user.age for user in filtered_users]
        sensitivity = get_global_sensitivity(average_age, age_data)
        print("Global Sensitivity:", sensitivity)
        
        μ = 0
        b = sensitivity/ε
        variance = get_variance(b)
        print("Variance:", variance)
        laplace = np.random.laplace(μ, b)
        print("Laplace:", laplace)
        result = average_age + laplace
        print("Result:", result)

        print("\n")
    
    elif mechanism == "exponential":
        real_frequent_education, count = find_frequent_education(raw_users_list)
        user_education_data = get_education_data(raw_users_list)
        utility_scores_object, possible_outputs, utility_scores = compute_utility_scores(user_education_data)
        # print("utility_scores_object:", utility_scores_object)
        # print("possible_outputs:", possible_outputs)
        # print("utility_scores:", utility_scores)

        sensitivity = get_global_sensitivity2(utility_scores_object, possible_outputs)
        print("Global Sensitivity:", sensitivity)

        scaled_scores = np.array(utility_scores) * ε
        # print("scaled_scores:")
        # for score, output in zip(scaled_scores, possible_outputs):
        #     print(f"{output:<15}: {score}")

        normalized_scaled_scores = normalize_scores(scaled_scores)
        # print("normalized_scaled_scores:")
        # for score, output in zip(normalized_scaled_scores, possible_outputs):
            # print(f"{output:<15}: {score}")

        exp_scaled_scores = np.exp(np.array(normalized_scaled_scores) / (2 * sensitivity))
        # print("exp_scaled_scores:")
        # for score, output in zip(exp_scaled_scores, possible_outputs):
            # print(f"{output:<15}: {score}")

        probabilities = exp_scaled_scores / np.sum(exp_scaled_scores)
        print("probabilities:")
        for score, output in zip(probabilities, possible_outputs):
            print(f"{output:<15}: {score}")
        
        selected_output = np.random.choice(possible_outputs, p=probabilities)
        print("selected_output:", selected_output)

        print("real_frequent_education:", real_frequent_education)

        print("\n")
    return



