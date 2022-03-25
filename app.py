import json
from statistics import mean

from modules import Individual
from utils import read_data, generate_data, get_courses_by_topic, course_to_user_matching_score, \
    person_to_person_matching_score, save_data, retrieve_data


def main():
    data_path = "data/data.json"
    individual_specs, course_specs, providers = read_data(data_path)
    providers = generate_data(individual_specs, course_specs, providers)

    with open("data/query.json", "r") as fp:
        query_data = json.load(fp)

    query_user = Individual(**query_data["user_info"])
    query_topic = query_data["query_topic"]

    provider_ids, courses = get_courses_by_topic(query_topic=query_topic, providers=providers)

    for provider_id in provider_ids:
        for course in providers[provider_id].available_courses:
            if course.topic == query_topic:
                c2u_score = course_to_user_matching_score(course, query_user)

                if len(course.course_rates.values()) == 0:
                    average_rating = 1.0
                else:
                    average_rating = mean(course.course_rates.values()) / 10

                print(f"[COURSE2USER] Provider -> {providers[provider_id].name} Course -> {course.name}\n"
                      f"Course to User Score : {c2u_score}\nAverage Rating : {average_rating}\n")

        print("------------------------------------------------------------------")

        for course, past_participants in providers[provider_id].past_participants.items():
            if course.topic == query_topic:
                for past_user in past_participants:
                    p2p_score = person_to_person_matching_score(past_user, query_user)
                    print(
                        f"[USER2USER]Provider -> {providers[provider_id].name} Course -> {course.name}\n"
                        f"Participant : {past_user}\n"
                        f"User to User Score : {p2p_score}\n")

    save_data(providers)
    providers = retrieve_data("data/saved_data.json")


if __name__ == '__main__':
    main()
