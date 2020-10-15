import csv
import os
from permutationGenerator import get_variations_list

if __name__ == "__main__":

    print(os.getcwd())
    print("---SCRIPT-START---")

    with open('data.csv', 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open("output.csv", "w") as outputCsv_file:
            fieldnames = ["post_title", "post_link", "post_category", "tag_string"]
            csv_writer = csv.DictWriter(outputCsv_file, lineterminator="\n", fieldnames=fieldnames)

            csv_writer.writeheader()

            for index, post in enumerate(csv_reader, 1):
                titleVariations = get_variations_list(post["post_title"])
                postVariations = get_variations_list(post["post_category"])
                totalVariations = titleVariations + postVariations

                csv_writer.writerow({"post_title": post["post_title"],
                                     "post_link": post["post_link"],
                                     "post_category": post["post_category"],
                                     "tag_string": "".join(list(set(totalVariations)))})

    print("---SCRIPT-COMPLETE---")
    print(f"---POSTS-PROCESSED: {index}---")
