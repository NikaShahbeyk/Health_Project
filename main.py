import json
from pdf2image import convert_from_path
import cv2
import easyocr
import os
import csv


class PDFTextExtractor:
  def extract(self, pdf_paths):
    # Initialize an empty list to store extracted text
    for pdf_path in pdf_paths:
        desired_data = []
        desired_data2 = []
        # Load the PDF image pages
        images = convert_from_path(pdf_path, 500, poppler_path=r'C:\poppler-21.11.0\Library\bin')

        # Process each image using EasyOCR and OpenCV
        for i, img in enumerate(images):
            # Save the image to a file
            image_path = f'/Users/Nika/Downloads_{i}.jpg'
            img.save(image_path, 'JPEG')

            # Load the saved image
            img = cv2.imread(image_path)

            # Convert the image to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply binary thresholding
            _, threshold = cv2.threshold(gray_img, 225, 255, cv2.THRESH_BINARY)

            # Initialize EasyOCR reader
            reader = easyocr.Reader(['en'])

            # Read text from the threshold
            result = reader.readtext(threshold)

            # Extract and store the recognized text
            for text_info in result:

                #First_Data.append(text_info[1])
                print(text_info[1])

                extracted_one = text_info[1]

                desired_data2.append(extracted_one)

                # save the text into a json file
                with open(pdf_path + 'first_text.json', 'w', encoding='utf-8') as json_file:
                   json.dump(desired_data2, json_file, ensure_ascii=False, indent=4)

                extracted_text = text_info[1].lower().replace(".", "").replace("(", "-")
                # we use it for save all the alphabets and digits and spaces
                cleaned_text = ''.join(c for c in extracted_text if c.isalpha() or c.isdigit() or c.isspace())
                # Now want to save it in desired_data
                desired_data.append(cleaned_text)
                # And then we print cleaned text
                # print(cleaned_text)
                # Save the changed extracted text to a JSON file
                with open(pdf_path + 'extracted_text.json', 'w', encoding='utf-8') as json_file:
                   json.dump(desired_data, json_file, ensure_ascii=False, indent=4)
        print("========================")


def search_and_print(data: list, target_string):
    # we use a flag
    find = False
    # try:
    #     with open(json_file_path, 'r') as json_file:json_file
    #         data = json.load(json_file)
    target_string = target_string.lower()
    for line in data:
        if target_string in line.lower():
            next_line = data[data.index(line) + 1]
            if next_line.isdigit():
                return next_line
                find = True
            else:
                next_line = data[data.index(line) + 2]
                if next_line.isdigit():
                    return next_line
                    find = True
                else:
                    return None

    return None
    # error exception
    # except FileNotFoundError:
    #     print(f"File '{json_file_path}' not found.")

def extract_lab_values(data: list) -> list:
    with open('/Users/Nika/Desktop/Lab/vital_signs.json', 'r') as json_file:
      target_list = json.load(json_file)

    # target_string = 'fbs'
    output = []
    for target_string in target_list:
        target_value = search_and_print(data, target_string)
        if target_value is not None:
            output.append({"item": target_string, "value": target_value})
    return output

# list and specific word
def count_occurrences(lst, target):
    return lst.count(target)
# Example usage
# if file run as a program
if __name__ == "__main__":
    j = 1
    i = 1
    pdf_paths = []
    while i < 100:
        pdf_paths.append(f'/Users/Nika/Desktop/Lab/{i}.pdf')
        i = i + 1

    # pdf_paths = [
    #     "/Users/Nika/Desktop/Lab/1.pdf",
    #     "/Users/Nika/Desktop/Lab/2.pdf",
    #     "/Users/Nika/Desktop/Lab/3.pdf",
    #     "/Users/Nika/Desktop/Lab/4.pdf",
    #     "/Users/Nika/Desktop/Lab/5.pdf",
    # ]

    all_strings = []


    def count_occurrences(strings_list, string):
        return strings_list.count(string)


    for pdf_path in pdf_paths:
        print('we are processing ', pdf_path)
        print('============================')
        json_file_path = pdf_path + 'extracted_text.json'
        # if we have the json file
        if os.path.exists(json_file_path):
            print("The Json File Exists")
            # loading json file
            # r means read mode
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                # first we make an empty list
                # first check that a value is a string or not
                for value in data:
                    if isinstance(value, str):
                        # use for splitting the string into words
                        strings = value.split()
                        # extending the list
                        all_strings.extend(strings)
                        with open('string.csv', 'w', newline='') as file:
                           unique_strings = set(all_strings)
                           writer = csv.writer(file)
                           for string in unique_strings:
                              occurrences = count_occurrences(all_strings, string)
                              print(f"'{string}' Time: {occurrences}")
                             # write the string and number in the csv file
                              writer.writerow([string, occurrences])
        else:
            pdf_extractor = PDFTextExtractor()
            pdf_extractor.extract(pdf_paths)

print("do you want to continue and search for specific words?")
print("1.yes")
print("2.No")
answer = input()