from typing import Counter, List, Optional
import os
# import numpy as np

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

    def basicStr(self) -> str:
        ans = ""
        for idx, c in self.groupedOccupations.items():
            for _ in range(c):
                if c:
                    ans += f"{idx}, "
                    ans += f"{self.age.get_value()}, "
                    ans += f"{self.education.get_value()}, "
                    ans += f"{self.marital_status.get_value()}, "
                    ans += f"{self.race.get_value()}\n"
        ans = ans.removesuffix("\n")
        return ans

    def _oriStr(self) -> str:
        ans = ""
        ans += f"\t{self.occupation}, "
        ans += f"{self.age.value}, "
        ans += f"{self.education.value}, "
        ans += f"{self.marital_status.value}, "
        ans += f"{self.race.value}\n"
        return ans

    def oriStr(self):
        userSet = list(self.userSet)
        fnl = ""

        userSet.sort(key=lambda x: x.occupation)

        for usr in userSet:
            if usr:
                fnl += usr._oriStr()
        return fnl.removesuffix("\n")

# dest = "dest"
# def ensureDest(prefix):
#     if dest and not os.path.isdir(dest):
#         os.mkdir(dest)
#     subPath = os.path.join(dest, prefix)
#     if not subPath:
#         exit(1)
#     if not os.path.isdir(subPath):
#         os.mkdir(subPath)
#     else:
#         None
#     return subPath

# def print_users_to_files(prefix: str, raw: List[User], final: List[User]):
#     path = ensureDest(prefix)
#     print_raw_users(prefix, raw, path)
#     print_final_users(prefix, final, path)

#     user_count = getUserCount(final)
#     print(f"Final Total users: {user_count}")
#     print(f"Final Total blocks: {len(final)}")
#     total_users = len(raw)
#     percentage = round((100 * user_count) / total_users, 2)
#     print(f"\nUser utility: {user_count}/{total_users} : {percentage}%")

# def print_raw_users(prefix: str, raw: List[User], path: str):
#     output = []
#     for user in raw:
#         if user:
#             output.append(user.oriStr())
#     filepath = os.path.join(path, f"{prefix}_input.data")
#     with open(filepath, "w") as f:
#         if not f:
#             exit(1)
#         f.write("\n".join(output))

# def print_final_users(prefix: str, final: List[User], path: str):
#     output = []
#     for user in final:
#         if not user:
#             exit(1)
#         output.append(user.basicStr())
#     filepath = os.path.join(path, f"{prefix}_out.data")
#     with open(filepath, "w") as f:
#         if not f:
#             exit(1)
#         f.write("\n".join(output))

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

# def laplace(x, μ, b):
#     return 1 / (2 * b) * np.exp(-np.abs(x - μ) / b)

# main function:
def mechanism(name, ε):
    print(ε,"- Differential Privacy")
    raw_users_list = read_raw_data("./adultdata/adult.data")
    if name == "laplace":
        filtered_users = filter_age(raw_users_list)
        average_age = calculate_average_age(filtered_users)
        print("Number of users:", len(filtered_users))
        print("Average age:", round(average_age,2))
        # getGlobalSensitivity()
        print("Global Sensitivity:")
        # laplace()
        # getVariance()
        print("Variance:")
        print("\n")
    
    elif name == "exponential":
        most_frequent_education, count = find_frequent_education(raw_users_list)
        print("Most frequent education:", most_frequent_education)
        print("Number of users:", count)
        # getGlobalSensitivity()
        print("Global Sensitivity:")
        # exponential()
        # getVariance()
        print("Variance:")
        

    # print_users_to_files(name, raw_users_list, final_users_list)
    return



