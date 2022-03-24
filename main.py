import json
import random
from dataclasses import dataclass
from typing import Dict, Any, Tuple, List
from uuid import uuid4

PERSON_TO_PERSON_SIM_MAX = 42
COURSE_TO_PERSON_SIM_MAX = 34


@dataclass
class Individual:
    name: str
    background: str
    profession: str
    gender: str
    age: str
    language: List[str]
    preferred_learning_style: List[str]

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(self.background) ^ hash(self.profession) ^ hash(self.gender) ^ hash(self.age)


@dataclass
class Course:
    name: str
    topic: str
    available_languages: List[str]
    appealing_learning_styles: List[str]

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(self.topic)


@dataclass
class Provider:
    name: str
    available_courses: List[Course]
    past_participants: Dict[Course, List[Individual]]


def read_data(filepath: str) -> Tuple[Dict[str, Any], Dict[str, Any], List[str]]:
    """

    :param filepath:
    :return:
    """
    with open(filepath, "r") as fp:
        data = json.load(fp)

    individual_specs = data["IndividualSpces"]
    course_specs = data["CourseSpecs"]
    providers = data["Providers"]

    return individual_specs, course_specs, providers


def generate_data(individual_specs: Dict[str, Any],
                  course_specs: Dict[str, Any],
                  providers_data: List[str]) -> List[Provider]:
    """

    :param individual_specs:
    :param course_specs:
    :param providers_data:
    :return:
    """
    topics = course_specs["Topics"]
    learning_styles = course_specs["LearningStyles"]
    backgrounds = individual_specs["Backgrounds"]
    professions = individual_specs["Professions"]
    genders = individual_specs["Gender"]
    age_ranges = individual_specs["Age"]
    languages = individual_specs["Language"]

    providers = list()

    for provider_name in providers_data:
        available_courses = []
        past_participants = {}
        for course_topic in set(random.choices(topics)):
            course = Course(name=f"{course_topic} {str(uuid4())[:4]}",
                            topic=course_topic,
                            available_languages=list(
                                set(random.choices(languages, k=random.randint(1, len(languages))))),
                            appealing_learning_styles=list(
                                set(random.choices(learning_styles, k=random.randint(1, 3)))))

            available_courses.append(
                course
            )

            users_for_course = list()

            for _ in range(random.randint(0, 4)):
                users_for_course.append(
                    Individual(
                        name=str(uuid4())[5:12],
                        background=random.choice(backgrounds),
                        profession=random.choice(professions),
                        gender=random.choice(genders),
                        age=random.choice(age_ranges),
                        language=list(set(random.choices(languages, k=random.randint(1, 2)))),
                        preferred_learning_style=list(set(random.choices(learning_styles, k=random.randint(1, 3))))
                    )
                )

            past_participants[course] = users_for_course

        providers.append(
            Provider(name=provider_name, available_courses=available_courses, past_participants=past_participants)
        )

    return providers


def course_to_user_matching_score(course: Course, user: Individual) -> float:
    """

    :param course:
    :param user:
    :return:
    """
    language_overlap = len(set(user.language).intersection(set(course.available_languages)))

    if language_overlap > 0:
        score = language_overlap

        learning_style_overlap = len(
            set(user.preferred_learning_style).intersection(set(course.appealing_learning_styles)))

        score += learning_style_overlap * 5

        return score / COURSE_TO_PERSON_SIM_MAX

    return 0.0


def person_to_person_matching_score(user_x: Individual, user_y: Individual) -> float:
    """

    :param user_x:
    :param user_y:
    :return:
    """
    learning_style_overlap = len(
        set(user_x.preferred_learning_style).intersection(set(user_y.preferred_learning_style)))

    background_check = float(user_x.background == user_y.background)
    profession_check = float(user_x.profession == user_y.profession)
    gender_check = float(user_x.gender == user_y.gender)
    age_range_check = float(user_x.age == user_y.age)

    total_similarity = learning_style_overlap * 5 + background_check * 4 +\
                       profession_check * 4 + gender_check * 1 + age_range_check * 3

    return total_similarity / PERSON_TO_PERSON_SIM_MAX


def get_courses_by_topic(query_topic: str, providers: List[Provider]) -> Tuple[List[int], Dict[str, Course]]:
    """

    :param query_topic:
    :param providers:
    :return:
    """
    possible_courses = dict()
    provider_ids = set()

    for provider_id, provider in enumerate(providers):
        for course in provider.available_courses:
            if query_topic == course.topic:
                possible_courses[provider.name] = course
                provider_ids.add(provider_id)

    return list(provider_ids), possible_courses


def main():
    data_path = "data.json"
    individual_specs, course_specs, providers = read_data(data_path)
    providers = generate_data(individual_specs, course_specs, providers)

    print("\n**************************************************************\n")
    for provider in providers:
        print(provider)
        print("\nAvailable Courses : ")
        for course in provider.available_courses:
            print(course)
        print("\nPast Participants : ")
        for course, participants in provider.past_participants.items():
            print(f"\nCourse :  {course.name} Topic : {course.topic}")
            print("Participants : ")
            for participant in participants:
                print(participant)
            print("\n-------------------------------------------------\n")
        print("\n**************************************************************\n")


if __name__ == '__main__':
    main()
